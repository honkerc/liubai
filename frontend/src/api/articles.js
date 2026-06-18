import { request } from './request'

/** 兼容数组或 { items, total, has_more } 分页响应 */
export function normalizeListResponse(data) {
    if (Array.isArray(data)) {
        return { items: data, total: data.length, page: 1, page_size: data.length, has_more: false }
    }
    return {
        items: data.items || [],
        total: data.total ?? (data.items?.length ?? 0),
        page: data.page ?? 1,
        page_size: data.page_size ?? (data.items?.length ?? 0),
        has_more: !!data.has_more,
    }
}

export const articleApi = {
    list(params = {}) {
        const qs = new URLSearchParams()
        if (params.search) qs.set('search', params.search)
        if (params.topic) qs.set('topic', params.topic)
        if (params.page) qs.set('page', params.page)
        if (params.page_size) qs.set('page_size', params.page_size)
        const query = qs.toString()
        return request(`/api/articles${query ? '?' + query : ''}`)
    },

    listAll() {
        return request('/api/articles/all')
    },

    get(title) {
        return request(`/api/articles/by-title/${encodeURIComponent(title)}`)
    },

    getByTitle(title) {
        return this.get(title)
    },

    create(data) {
        return request('/api/articles', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },

    update(id, data) {
        return request(`/api/articles/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },

    delete(id) {
        return request(`/api/articles/${id}`, {
            method: 'DELETE',
        })
    },

    topics() {
        return request('/api/topics')
    },
}

export async function fetchAllPublishedArticles(params = {}) {
    const all = []
    let page = 1
    const page_size = 100
    while (true) {
        const data = await articleApi.list({ ...params, page, page_size })
        const { items, has_more } = normalizeListResponse(data)
        all.push(...items)
        if (!has_more) break
        page += 1
    }
    return all
}
