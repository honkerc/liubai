const STORAGE_KEY = 'liubai-article-comments'
const VISITOR_NAME_KEY = 'liubai-visitor-name'
const SEEDED_KEY = 'liubai-article-comments-seeded'

function readStore() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
    } catch {
        return {}
    }
}

function writeStore(store) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store))
}

function readSeeded() {
    try {
        return JSON.parse(localStorage.getItem(SEEDED_KEY) || '{}')
    } catch {
        return {}
    }
}

function markSeeded(key) {
    const seeded = readSeeded()
    seeded[key] = true
    localStorage.setItem(SEEDED_KEY, JSON.stringify(seeded))
}

export function getArticleCommentKey(article) {
    if (!article) return ''
    if (article.id) return `id:${article.id}`
    if (article.title) return `title:${article.title}`
    return ''
}

export function getVisitorName() {
    const saved = localStorage.getItem(VISITOR_NAME_KEY)
    if (saved?.trim()) return saved.trim()
    localStorage.setItem(VISITOR_NAME_KEY, '路人甲')
    return '路人甲'
}

export function setVisitorName(name) {
    const next = String(name || '').trim() || '路人甲'
    localStorage.setItem(VISITOR_NAME_KEY, next)
    return next
}

function createComment(author, content, offsetMinutes = 0) {
    return {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        author,
        content: String(content || '').trim(),
        createdAt: new Date(Date.now() - offsetMinutes * 60 * 1000).toISOString(),
    }
}

function buildSeedComments() {
    return [
        createComment('路人乙', '这篇写得很清楚，收藏了。', 26),
        createComment('路人丙', '有个细节想确认一下，后面会更新吗？', 12),
        createComment('路人甲', '同问，蹲一个后续～', 4),
    ]
}

export function loadComments(articleKey) {
    if (!articleKey) return []
    const store = readStore()
    if (Array.isArray(store[articleKey]) && store[articleKey].length > 0) {
        return store[articleKey]
    }

    const seeded = readSeeded()
    if (!seeded[articleKey]) {
        const mock = buildSeedComments()
        store[articleKey] = mock
        writeStore(store)
        markSeeded(articleKey)
        return mock
    }

    return store[articleKey] || []
}

export function addComment(articleKey, { author, content }) {
    if (!articleKey) return []
    const text = String(content || '').trim()
    if (!text) return loadComments(articleKey)

    const store = readStore()
    const list = Array.isArray(store[articleKey]) ? [...store[articleKey]] : []
    list.push(createComment(author || getVisitorName(), text, 0))
    store[articleKey] = list
    writeStore(store)
    return list
}

export function formatCommentTime(iso) {
    if (!iso) return ''
    const d = new Date(iso)
    if (Number.isNaN(d.getTime())) return ''

    const now = new Date()
    const diffMs = now.getTime() - d.getTime()
    const diffMin = Math.floor(diffMs / 60000)

    if (diffMin < 1) return '刚刚'
    if (diffMin < 60) return `${diffMin} 分钟前`

    const pad = (n) => String(n).padStart(2, '0')
    const time = `${pad(d.getHours())}:${pad(d.getMinutes())}`

    const isSameDay = (a, b) =>
        a.getFullYear() === b.getFullYear()
        && a.getMonth() === b.getMonth()
        && a.getDate() === b.getDate()

    if (isSameDay(d, now)) return `今天 ${time}`

    const yesterday = new Date(now)
    yesterday.setDate(now.getDate() - 1)
    if (isSameDay(d, yesterday)) return `昨天 ${time}`

    return `${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${time}`
}

export function avatarColor(name) {
    const palette = ['#4f6ef7', '#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    let hash = 0
    const text = String(name || '路人')
    for (let i = 0; i < text.length; i++) {
        hash = text.charCodeAt(i) + ((hash << 5) - hash)
    }
    return palette[Math.abs(hash) % palette.length]
}
