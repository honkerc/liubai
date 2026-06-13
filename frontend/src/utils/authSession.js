/** 401 时清除登录态并跳转登录页 */
export function handleUnauthorized() {
    localStorage.removeItem('token')
    const path = window.location.pathname
    if (path.startsWith('/login')) return
    const redirect = encodeURIComponent(path + window.location.search)
    window.location.href = `/login?redirect=${redirect}&expired=1`
}
