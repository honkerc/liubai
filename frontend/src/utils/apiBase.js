/** API 根地址：开发走 devServer 代理，生产默认同源 */
export function getApiBase() {
    if (process.env.NODE_ENV === 'development') {
        return ''
    }
    const configured = process.env.VUE_APP_API_BASE
    if (configured !== undefined && configured !== null && String(configured).trim() !== '') {
        return String(configured).replace(/\/$/, '')
    }
    return ''
}
