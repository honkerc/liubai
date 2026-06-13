import { request } from './request'

export const uploadApi = {
    upload(file) {
        const form = new FormData()
        form.append('file', file)
        return request('/api/upload', {
            method: 'POST',
            body: form,
            headers: {},
        })
    },
}

export { resolveAssetUrl, resolveMarkdownHtml } from '@/utils/resolveMarkdownHtml'
