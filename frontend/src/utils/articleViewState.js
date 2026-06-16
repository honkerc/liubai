import { reactive } from 'vue'
import { extractHeadingsFromMarkdown } from '@/utils/extractHeadings'
import { applyHeadingHighlight } from '@/utils/articleTocNav'

export const articleViewState = reactive({
    /** 用户在详情页主动切回文章列表时为 true */
    tocSuppressed: false,
    title: '',
    headings: [],
    activeHeadingId: '',
})

export function syncArticleHeadings(content, title = '') {
    if (title) articleViewState.title = title
    articleViewState.headings = extractHeadingsFromMarkdown(content || '')
}

export function showArticleTocMode() {
    articleViewState.tocSuppressed = false
}

export function hideArticleToc() {
    articleViewState.tocSuppressed = true
    applyHeadingHighlight('')
}

export function resetArticleHeadings() {
    articleViewState.headings = []
    articleViewState.activeHeadingId = ''
    applyHeadingHighlight('')
}

export function clearArticleView() {
    articleViewState.tocSuppressed = false
    articleViewState.title = ''
    articleViewState.headings = []
    articleViewState.activeHeadingId = ''
    applyHeadingHighlight('')
}

export function setActiveHeading(id) {
    articleViewState.activeHeadingId = id || ''
    applyHeadingHighlight(id)
}
