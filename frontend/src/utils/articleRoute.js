/** 从路由中解析文章标题（已 decode） */

export function routeTitleParam(route) {
    const raw = route?.params?.title
    if (!raw) return ''
    try {
        return decodeURIComponent(raw)
    } catch {
        return raw
    }
}

export function routeTopicParam(route) {
    const raw = route?.params?.topic
    if (!raw) return ''
    try {
        return decodeURIComponent(raw)
    } catch {
        return raw
    }
}

export function isNewArticleRoute(route) {
    return route?.name === 'new-article'
}

export function toArticleRoute(title) {
    return { name: 'public-article', params: { title } }
}

export function toNewArticleRoute({ fresh = false } = {}) {
    if (fresh) {
        return { name: 'new-article', query: { fresh: String(Date.now()) } }
    }
    return { name: 'new-article' }
}

/** @deprecated 使用 toArticleRoute */
export function toEditorRoute(title) {
    return toArticleRoute(title)
}

export function toTopicRoute(topic) {
    return { name: 'topic', params: { topic } }
}

export function toTopicsRoute() {
    return { name: 'topics' }
}
