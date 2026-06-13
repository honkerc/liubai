/** 在 textarea 光标处插入或包裹 Markdown */
export function insertMarkdown(textarea, before, after = '', placeholder = '') {
    if (!textarea) return ''
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const selected = textarea.value.substring(start, end) || placeholder
    const inserted = before + selected + after
    const value = textarea.value.substring(0, start) + inserted + textarea.value.substring(end)
    textarea.value = value
    const cursor = start + before.length + selected.length
    textarea.selectionStart = textarea.selectionEnd = cursor
    textarea.focus()
    return value
}

/** 在当前行首插入前缀（如 ## 、- 、> ） */
export function insertLinePrefix(textarea, prefix) {
    if (!textarea) return ''
    const start = textarea.selectionStart
    const value = textarea.value
    const lineStart = value.lastIndexOf('\n', start - 1) + 1
    const lineEnd = value.indexOf('\n', start)
    const end = lineEnd === -1 ? value.length : lineEnd
    const line = value.substring(lineStart, end)
    const stripped = line.replace(/^#{1,6}\s|^[-*+]\s|^>\s|^\d+\.\s|^- \[[ xX]\]\s/, '')
    const newLine = prefix + stripped
    const newValue = value.substring(0, lineStart) + newLine + value.substring(end)
    textarea.value = newValue
    const cursor = lineStart + prefix.length + (start - lineStart)
    textarea.selectionStart = textarea.selectionEnd = Math.min(cursor, lineStart + newLine.length)
    textarea.focus()
    return newValue
}

/**
 * 插入整块 Markdown（代码块、表格等）
 * @param {number|null} cursorOffsetInBlock 光标落在块内相对 block 开头的偏移
 */
export function insertBlock(textarea, block, cursorOffsetInBlock = null) {
    if (!textarea) return ''
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const value = textarea.value
    const needNewlineBefore = start > 0 && value[start - 1] !== '\n'
    const prefix = needNewlineBefore ? '\n\n' : ''
    const inserted = prefix + block + '\n'
    const newValue = value.substring(0, start) + inserted + value.substring(end)
    textarea.value = newValue
    const blockStart = start + prefix.length
    const cursor = cursorOffsetInBlock != null
        ? blockStart + cursorOffsetInBlock
        : blockStart + block.length
    textarea.selectionStart = textarea.selectionEnd = cursor
    textarea.focus()
    return newValue
}

export function makeTable(cols, dataRows = 2) {
    const row = () => `| ${Array(cols).fill(' ').join(' | ')} |`
    const sep = `| ${Array(cols).fill('---').join(' | ')} |`
    return [row(), sep, ...Array(dataRows).fill(0).map(row)].join('\n')
}

export const MD_SNIPPETS = {
    codeBlock: '```\n\n```',
    quote: '> 引用内容',
    divider: '---',
    link: '[链接文字](https://)',
    image: '![图片描述](https://)',
}

/** 3 列 × 3 行数据（含表头共 4 行） */
export const TABLE_3X3 = makeTable(3, 3)

export function makeList(type, count = 3) {
    switch (type) {
        case 'bullet':
            return Array(count).fill('- ').join('\n')
        case 'ordered':
            return Array.from({ length: count }, (_, i) => `${i + 1}. `).join('\n')
        case 'task':
            return Array(count).fill('- [ ] ').join('\n')
        default:
            return ''
    }
}

/** 各类型列表首行前缀长度，用于光标定位 */
export const LIST_CURSOR_OFFSET = {
    bullet: 2,
    ordered: 3,
    task: 6,
}

export const LIST_BULLET_3 = makeList('bullet', 3)
export const LIST_ORDERED_3 = makeList('ordered', 3)
export const LIST_TASK_3 = makeList('task', 3)
