import { reactive } from 'vue'
import { extractHeadingsFromMarkdown } from '@/utils/extractHeadings'
import { applyHeadingHighlight } from '@/utils/articleTocNav'

export const articleViewState = reactive({
    /** 用户在详情页主动切回文章列表时为 true */
    tocSuppressed: false,
    /** 文章目录正在加载（正文未就绪） */
    tocLoading: false,
    title: '',
    headings: [],
    activeHeadingId: '',
})

export function syncArticleHeadings(content, title = '') {
    if (title) articleViewState.title = title
    articleViewState.headings = extractHeadingsFromMarkdown(content || '')
    articleViewState.tocLoading = false
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
    articleViewState.tocLoading = true
    applyHeadingHighlight('')
}

export function clearArticleView() {
    articleViewState.tocSuppressed = false
    articleViewState.tocLoading = false
    articleViewState.title = ''
    articleViewState.headings = []
    articleViewState.activeHeadingId = ''
    applyHeadingHighlight('')
}

export function setActiveHeading(id) {
    articleViewState.activeHeadingId = id || ''
    applyHeadingHighlight(id)
}
