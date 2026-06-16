import { reactive } from 'vue'
import { extractHeadingsFromMarkdown } from '@/utils/extractHeadings'
import { applyHeadingHighlight } from '@/utils/articleTocNav'

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
    applyHeadingHighlight('')
}

export function clearArticleView() {
    articleViewState.inDetail = false
    articleViewState.title = ''
    articleViewState.headings = []
    articleViewState.activeHeadingId = ''
    applyHeadingHighlight('')
}

export function setActiveHeading(id) {
    articleViewState.activeHeadingId = id || ''
    applyHeadingHighlight(id)
}
