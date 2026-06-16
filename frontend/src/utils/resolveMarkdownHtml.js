import { getApiBase } from '@/utils/apiBase'

const API_BASE = getApiBase()

/** 去掉资源路径末尾误加的 /（如 /uploads/foo.webp/） */
function normalizeAssetPath(path) {
    if (!path || !path.startsWith('/')) return path
    return path.replace(/(\.[\w+-]+)\/+$/i, '$1')
}

/** 将 Markdown 渲染 HTML 中的静态资源地址补全 */
export function resolveAssetUrl(url) {
    if (!url) return url
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
        return url
    }
    let path = normalizeAssetPath(url)
    if (path.startsWith('/') && !path.startsWith('/uploads/')) {
        if (/^\/(images|videos|audio|files)\//.test(path)) {
            path = `/uploads${path}`
        }
    }
    if (path.startsWith('/')) {
        return `${API_BASE}${path}`
    }
    return path
}

export function resolveMarkdownHtml(html) {
    if (!html) return ''
    return html
        .replace(/src="(\/[^"]+)"/g, (_, url) => `src="${resolveAssetUrl(url)}"`)
        .replace(/href="(\/[^"]+)"/g, (_, url) => `href="${resolveAssetUrl(url)}"`)
}
