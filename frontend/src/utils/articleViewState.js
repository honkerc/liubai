import { reactive } from 'vue'
import { extractHeadingsFromMarkdown } from '@/utils/extractHeadings'

export const articleViewState = reactive({
    inDetail: false,
    title: '',
    headings: [],
    activeHeadingId: '',
})

export function syncArticleHeadings(content, title = '') {
    articleViewState.inDetail = true
    if (title) articleViewState.title = title
    articleViewState.headings = extractHeadingsFromMarkdown(content || '')
}

export function hideArticleToc() {
    articleViewState.inDetail = false
}

export function clearArticleView() {
    articleViewState.inDetail = false
    articleViewState.title = ''
    articleViewState.headings = []
    articleViewState.activeHeadingId = ''
}

export function setActiveHeading(id) {
    articleViewState.activeHeadingId = id || ''
}
