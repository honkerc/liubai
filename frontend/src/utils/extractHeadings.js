/** 与 editorMarkdown parseMarkdown 中标题 id 规则一致 */
export function headingSlug(text) {
    return (text || '')
        .replace(/<[^>]*>/g, '')
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
        .replace(/(^-|-$)/g, '')
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
    return headings
}
