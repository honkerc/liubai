/** @returns {'notfound' | 'network'} */
export function classifyLoadError(err) {
    const msg = err?.message || ''
    if (
        msg.includes('不存在')
        || msg.includes('404')
        || msg.startsWith('HTTP 404')
    ) {
        return 'notfound'
    }
    return 'network'
}
