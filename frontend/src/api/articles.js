import { request } from './request'

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
