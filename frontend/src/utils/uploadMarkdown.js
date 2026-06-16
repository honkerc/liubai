/** 根据上传结果生成 Markdown / HTML 片段 */
export function buildUploadMarkdown(res, filename = '') {
    const url = (res.compressed_url || res.url || '').replace(/\/+$/, '')
    const name = filename || res.filename || '文件'
    const base = name.replace(/\.[^.]+$/, '') || name

    switch (res.type) {
        case 'image':
            return `![${base}](${url})`
        case 'video':
            return `<video src="${url}" controls playsinline class="markdown-video"></video>`
        case 'audio':
            return `<audio src="${url}" controls></audio>`
        default:
            return `[${name}](${url})`
    }
}

export const UPLOAD_ACCEPT = [
    'image/*',
    'video/*',
    'audio/*',
    '.zip,.rar,.7z,.tar,.gz,.bz2',
    '.pdf,.md,.txt',
    '.doc,.docx,.xls,.xlsx,.ppt,.pptx',
].join(',')
