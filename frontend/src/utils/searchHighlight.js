/** 转义 HTML，避免 v-html 注入 */
export function escapeHtml(text) {
    return String(text ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
}

/** 高亮关键词，返回可安全用于 v-html 的字符串 */
export function highlightKeyword(text, keyword) {
    const raw = String(text ?? '')
    const kw = keyword?.trim()
    if (!raw || !kw) return escapeHtml(raw)

    const escaped = escapeHtml(raw)
    const pattern = kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    return escaped.replace(new RegExp(`(${pattern})`, 'gi'), '<mark class="search-hl">$1</mark>')
}

/** 从 Markdown 提取纯文本 */
export function markdownToPlain(text) {
    return String(text ?? '')
        .replace(/```[\s\S]*?```/g, ' ')
        .replace(/`[^`]+`/g, ' ')
        .replace(/!\[[^\]]*]\([^)]+\)/g, ' ')
        .replace(/\[([^\]]+)]\([^)]+\)/g, '$1')
        .replace(/[#>*_\-\[\]()!|~]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
}

/** 分词并记录原文位置（中文按字，英文按词） */
function tokenizeWithPositions(text) {
    const tokens = []
    let i = 0
    while (i < text.length) {
        if (/\s/.test(text[i])) {
            i++
            continue
        }
        const start = i
        if (/[\u4e00-\u9fff]/.test(text[i])) {
            tokens.push({ start, end: start + 1 })
            i++
            continue
        }
        while (i < text.length && !/\s/.test(text[i]) && !/[\u4e00-\u9fff]/.test(text[i])) {
            i++
        }
        tokens.push({ start, end: i })
    }
    return tokens
}

/** 截取包含关键词的正文摘要（匹配处前后各 wordRadius 个词） */
export function buildSearchSnippet(content, keyword, wordRadius = 50) {
    const text = markdownToPlain(content)
    const kw = keyword?.trim()
    if (!text || !kw) return ''

    const lower = text.toLowerCase()
    const kwLower = kw.toLowerCase()
    const matchStart = lower.indexOf(kwLower)
    if (matchStart === -1) return ''

    const matchEnd = matchStart + kw.length
    const tokens = tokenizeWithPositions(text)
    if (!tokens.length) return ''

    let firstToken = 0
    for (let i = 0; i < tokens.length; i++) {
        if (tokens[i].end > matchStart) {
            firstToken = i
            break
        }
    }

    let lastToken = firstToken
    for (let i = firstToken; i < tokens.length; i++) {
        if (tokens[i].start < matchEnd) lastToken = i
    }

    const from = Math.max(0, firstToken - wordRadius)
    const to = Math.min(tokens.length, lastToken + 1 + wordRadius)

    let snippet = text.slice(tokens[from].start, tokens[to - 1].end)
    if (from > 0) snippet = `…${snippet}`
    if (to < tokens.length) snippet = `${snippet}…`
    return snippet
}
