import { reactive } from 'vue'

const TOKEN_KEY = 'token'
/** 到期前多少毫秒内自动续期 */
const REFRESH_BEFORE_MS = 24 * 60 * 60 * 1000
/** 过期后仍允许续期的宽限（毫秒） */
const REFRESH_GRACE_MS = 7 * 24 * 60 * 60 * 1000

export const authState = reactive({
    token: readToken(),
})

function readToken() {
    try {
        return localStorage.getItem(TOKEN_KEY) || ''
    } catch {
        return ''
    }
}

export function getToken() {
    return authState.token || readToken()
}

export function setToken(token) {
    authState.token = token || ''
    if (token) {
        localStorage.setItem(TOKEN_KEY, token)
    } else {
        localStorage.removeItem(TOKEN_KEY)
    }
    window.dispatchEvent(new CustomEvent('auth-changed'))
}

export function clearSession() {
    setToken('')
}

export function decodeJwtPayload(token) {
    if (!token) return null
    try {
        const part = token.split('.')[1]
        if (!part) return null
        const json = atob(part.replace(/-/g, '+').replace(/_/g, '/'))
        return JSON.parse(json)
    } catch {
        return null
    }
}

export function getTokenExpiryMs(token) {
    const payload = decodeJwtPayload(token)
    if (!payload?.exp) return null
    return payload.exp * 1000
}

export function isTokenExpired(token, leewayMs = 0) {
    const exp = getTokenExpiryMs(token)
    if (!exp) return true
    return Date.now() >= exp - leewayMs
}

/** 超出宽限期，必须重新登录 */
export function isTokenHardExpired(token) {
    const exp = getTokenExpiryMs(token)
    if (!exp) return true
    return Date.now() >= exp + REFRESH_GRACE_MS
}

export function isAuthenticated() {
    const token = getToken()
    if (!token) return false
    return !isTokenHardExpired(token)
}

let refreshPromise = null
let expiredRedirectTimer = null

async function fetchRefresh(token) {
    const { getApiBase } = await import('@/utils/apiBase')
    const res = await fetch(`${getApiBase()}/api/auth/refresh`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
    if (!res.ok) return null
    const data = await res.json()
    return data.access_token || null
}

/** 访问站点或发请求前续期 token */
export async function tryRefreshSession() {
    const token = getToken()
    if (!token) return false
    if (isTokenHardExpired(token)) {
        clearSession()
        return false
    }

    const exp = getTokenExpiryMs(token)
    const now = Date.now()
    const needsRefresh = !exp || exp - now < REFRESH_BEFORE_MS || now >= exp
    if (!needsRefresh) return true

    if (!refreshPromise) {
        refreshPromise = (async () => {
            try {
                const next = await fetchRefresh(token)
                if (next) {
                    setToken(next)
                    return true
                }
                if (isTokenHardExpired(token)) {
                    clearSession()
                }
                return false
            } finally {
                refreshPromise = null
            }
        })()
    }
    return refreshPromise
}

export async function initAuthSession() {
    const token = getToken()
    if (!token) return false
    if (isTokenHardExpired(token)) {
        clearSession()
        return false
    }
    return tryRefreshSession()
}

export function handleUnauthorized(options = {}) {
    clearSession()
    const path = window.location.pathname
    if (path.startsWith('/login')) return

    window.dispatchEvent(new CustomEvent('auth-expired'))

    if (options.immediate || options.redirect) {
        if (expiredRedirectTimer) clearTimeout(expiredRedirectTimer)
        expiredRedirectTimer = null
        const redirect = encodeURIComponent(path + window.location.search)
        window.location.href = `/login?redirect=${redirect}&expired=1`
    }
}
