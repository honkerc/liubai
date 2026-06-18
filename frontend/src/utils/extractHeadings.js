/** 与 editorMarkdown parseMarkdown 中标题 id 规则一致 */
export function headingSlug(text) {
    return (text || '')
        .replace(/<[^>]*>/g, '')
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
        .replace(/(^-|-$)/g, '')
}

/** 为同名标题追加 -2、-3 后缀，保证 id 唯一 */
export function assignUniqueHeadingIds(headings) {
    const used = {}
    return headings.map((h) => {
        let base = headingSlug(h.text) || 'section'
        let id = base
        let n = 2
        while (used[id]) {
            id = `${base}-${n++}`
        }
        used[id] = true
        return { ...h, id }
    })
}

/** 从 Markdown 正文提取 h1–h6 目录 */
export function extractHeadingsFromMarkdown(content) {
    if (!content || !content.trim()) return []
    const headings = []
    for (const line of content.split('\n')) {
        const m = line.match(/^(#{1,6})\s+(.+)$/)
        if (!m) continue
        const level = m[1].length
        const text = m[2].trim()
        if (!text) continue
        headings.push({ level, text, id: headingSlug(text) })
    }
    return assignUniqueHeadingIds(headings)
}
