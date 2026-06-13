import { handleUnauthorized } from '@/utils/authSession'
import { getApiBase } from '@/utils/apiBase'

const API_BASE = getApiBase()

export async function request(url, options = {}) {
    const token = localStorage.getItem('token')
    const isFormData = options.body instanceof FormData
    const headers = {
        ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
        ...options.headers,
    }
    if (token) {
        headers['Authorization'] = `Bearer ${token}`
    }

    const res = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers,
    })

    if (res.status === 401) {
        handleUnauthorized()
        throw new Error('登录已过期，请重新登录')
    }

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        const detail = err.detail
        const message = typeof detail === 'string'
            ? detail
            : Array.isArray(detail)
                ? detail.map(d => d.msg || d).join(', ')
                : `HTTP ${res.status}`
        throw new Error(message || `HTTP ${res.status}`)
    }

    return res.json()
}
