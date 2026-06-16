import { getApiBase } from '@/utils/apiBase'
import { getToken, handleUnauthorized, tryRefreshSession } from '@/utils/authSession'

export function formatFileSize(bytes) {
    if (!bytes || bytes <= 0) return '0 B'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`
}

function parseErrorResponse(xhr) {
    try {
        const err = JSON.parse(xhr.responseText)
        const detail = err.detail
        if (typeof detail === 'string') return detail
        if (Array.isArray(detail)) return detail.map(d => d.msg || d).join(', ')
    } catch {
        // ignore
    }
    return xhr.statusText || `HTTP ${xhr.status}`
}

/**
 * 带进度回调的文件上传（XMLHttpRequest）
 * onProgress({ loaded, total, percent }) — percent 为 -1 表示总大小未知
 */
export function uploadWithProgress(file, onProgress) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest()
        const form = new FormData()
        form.append('file', file)

        xhr.upload.addEventListener('progress', (event) => {
            if (!onProgress) return
            if (event.lengthComputable) {
                const percent = event.total
                    ? Math.min(99, Math.round((event.loaded / event.total) * 100))
                    : -1
                onProgress({
                    loaded: event.loaded,
                    total: event.total,
                    percent,
                })
            } else {
                onProgress({ loaded: event.loaded, total: 0, percent: -1 })
            }
        })

        xhr.addEventListener('load', async () => {
            if (xhr.status === 401) {
                const ok = await tryRefreshSession()
                if (!ok) {
                    handleUnauthorized()
                    reject(new Error('登录已过期，请重新登录'))
                } else {
                    reject(new Error('登录已刷新，请重试上传'))
                }
                return
            }
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    resolve(JSON.parse(xhr.responseText))
                } catch {
                    reject(new Error('响应解析失败'))
                }
                return
            }
            reject(new Error(parseErrorResponse(xhr)))
        })

        xhr.addEventListener('error', () => reject(new Error('网络错误，上传失败')))
        xhr.addEventListener('abort', () => reject(new Error('上传已取消')))

        const token = getToken()
        xhr.open('POST', `${getApiBase()}/api/upload`)
        if (token) {
            xhr.setRequestHeader('Authorization', `Bearer ${token}`)
        }
        xhr.send(form)
    })
}

export const uploadApi = {
    uploadWithProgress,
}

export { resolveAssetUrl, resolveMarkdownHtml } from '@/utils/resolveMarkdownHtml'
