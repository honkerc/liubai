/** 正文标题距滚动容器顶部的留白（px） */
export const ARTICLE_HEADING_SCROLL_OFFSET = 72

/** 编辑态正文在 .detail-wrapper 内滚动，只读态在 .layout-right-body */
export function getArticleScrollRoot() {
    const editingWrapper = document.querySelector('.post-view--editing .detail-wrapper')
    if (editingWrapper) return editingWrapper
    return document.querySelector('.layout-right-body')
}

export function applyHeadingHighlight(activeId) {
    const root = getArticleScrollRoot()
    if (!root) return
    root.querySelectorAll('.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6')
        .forEach((el) => el.classList.remove('detail-heading-active'))
    if (!activeId) return
    root.querySelector(`#${CSS.escape(activeId)}`)?.classList.add('detail-heading-active')
}

export function scrollToArticleHeading(id, offset = ARTICLE_HEADING_SCROLL_OFFSET) {
    const root = getArticleScrollRoot()
    const el = root?.querySelector(`#${CSS.escape(id)}`)
    if (!root || !el) return false
    const top = el.getBoundingClientRect().top - root.getBoundingClientRect().top + root.scrollTop - offset
    root.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
    return true
}

export function createHeadingObserver(onActiveId) {
    const root = getArticleScrollRoot()
    if (!root) return null

    const headings = root.querySelectorAll('.markdown-body h1[id], .markdown-body h2[id], .markdown-body h3[id], .markdown-body h4[id], .markdown-body h5[id], .markdown-body h6[id]')
    if (!headings.length) return null

    const marginTop = -ARTICLE_HEADING_SCROLL_OFFSET
    const observer = new IntersectionObserver(
        (entries) => {
            const visible = entries
                .filter((e) => e.isIntersecting)
                .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
            if (visible.length > 0) {
                onActiveId(visible[0].target.id)
            }
        },
        {
            root,
            rootMargin: `${marginTop}px 0px -70% 0px`,
            threshold: 0,
        },
    )

    headings.forEach((h) => observer.observe(h))
    return observer
}
