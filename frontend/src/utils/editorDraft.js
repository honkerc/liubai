const DRAFT_KEYS = {
    title: 'editor_draft_title',
    content: 'editor_draft_content',
    topic: 'editor_draft_topic',
    time: 'editor_draft_time',
}

const DRAFT_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000

export function hasLocalDraft() {
    try {
        const time = localStorage.getItem(DRAFT_KEYS.time)
        if (!time) return false
        if (Date.now() - parseInt(time, 10) > DRAFT_MAX_AGE_MS) return false
        const content = localStorage.getItem(DRAFT_KEYS.content)
        const title = localStorage.getItem(DRAFT_KEYS.title)
        return !!(content?.trim() || title?.trim())
    } catch {
        return false
    }
}

export function readLocalDraft() {
    try {
        const time = localStorage.getItem(DRAFT_KEYS.time)
        if (!time) return null
        if (Date.now() - parseInt(time, 10) > DRAFT_MAX_AGE_MS) {
            clearLocalDraft()
            return null
        }
        const content = localStorage.getItem(DRAFT_KEYS.content)
        if (!content) return null
        return {
            title: localStorage.getItem(DRAFT_KEYS.title) || '',
            topic: localStorage.getItem(DRAFT_KEYS.topic) || '',
            content,
            savedAt: parseInt(time, 10),
        }
    } catch {
        return null
    }
}

export function writeLocalDraft({ title, content, topic }) {
    try {
        localStorage.setItem(DRAFT_KEYS.title, title ?? '')
        localStorage.setItem(DRAFT_KEYS.content, content ?? '')
        localStorage.setItem(DRAFT_KEYS.topic, topic ?? '')
        localStorage.setItem(DRAFT_KEYS.time, String(Date.now()))
    } catch { /* ignore */ }
}

export function clearLocalDraft() {
    try {
        localStorage.removeItem(DRAFT_KEYS.title)
        localStorage.removeItem(DRAFT_KEYS.content)
        localStorage.removeItem(DRAFT_KEYS.topic)
        localStorage.removeItem(DRAFT_KEYS.time)
    } catch { /* ignore */ }
}
