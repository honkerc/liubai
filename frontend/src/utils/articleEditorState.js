import { reactive } from 'vue'

export const editorState = reactive({
    inEditor: false,
    articleId: null,
    title: '',
    isPublished: false,
    isPinned: false,
    saveStatus: 'saved',
    createdAt: null,
})

export function syncEditorState(payload) {
    Object.assign(editorState, payload)
}

export function clearEditorState() {
    editorState.inEditor = false
    editorState.articleId = null
    editorState.title = ''
    editorState.isPublished = false
    editorState.isPinned = false
    editorState.saveStatus = 'saved'
    editorState.createdAt = null
}

export function displayEditorTitle(title) {
    return (title || '').trim() || '未命名'
}

/** 绿=已发布 红=编辑未保存 灰=草稿 */
export function getArticleStatusClass(article, { isActive, saveStatus }) {
    if (isActive && (saveStatus === 'unsaved' || saveStatus === 'saving')) {
        return 'editing-unsaved'
    }
    if (article.is_published) return 'published'
    return 'draft'
}

export function notifySidebarRefresh() {
    window.dispatchEvent(new CustomEvent('sidebar-articles-refresh'))
}
