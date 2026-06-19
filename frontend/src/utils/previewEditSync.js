function caretRangeFromPoint(x, y) {
    if (document.caretRangeFromPoint) {
        return document.caretRangeFromPoint(x, y)
    }
    if (document.caretPositionFromPoint) {
        const pos = document.caretPositionFromPoint(x, y)
        if (!pos) return null
        const range = document.createRange()
        range.setStart(pos.offsetNode, pos.offset)
        range.collapse(true)
        return range
    }
    return null
}

/** 预览 DOM 中点击位置对应的纯文本偏移（与 Range.toString 一致） */
export function getPreviewTextOffset(previewEl, x, y) {
    if (!previewEl) return null
    const range = caretRangeFromPoint(x, y)
    if (!range || !previewEl.contains(range.startContainer)) return null
    const pre = document.createRange()
    pre.selectNodeContents(previewEl)
    pre.setEnd(range.startContainer, range.startOffset)
    return pre.toString().length
}

function emitPlainCharsFromLine(line, plainTarget, plainSoFar) {
    let li = 0
    let plain = plainSoFar
    while (li < line.length && plain < plainTarget) {
        const rest = line.slice(li)
        const img = rest.match(/^!\[[^\]]*]\([^)]*\)/)
        if (img) {
            li += img[0].length
            continue
        }
        const link = rest.match(/^\[([^\]]*)]\([^)]*\)/)
        if (link) {
            for (let c = 0; c < link[1].length && plain < plainTarget; c += 1) {
                plain += 1
            }
            li += link[0].length
            continue
        }
        if (rest.startsWith('**') || rest.startsWith('__')) {
            li += 2
            continue
        }
        if (rest[0] === '*' || rest[0] === '_' || rest[0] === '`') {
            li += 1
            continue
        }
        plain += 1
        li += 1
    }
    return { plain, li }
}

/** 将预览纯文本偏移映射回 Markdown 源码索引（近似，足够定位光标） */
export function markdownIndexFromPlainOffset(markdown, plainOffset) {
    const target = Math.max(0, plainOffset)
    let plain = 0
    let i = 0

    while (i < markdown.length && plain < target) {
        if (markdown.startsWith('```', i)) {
            const close = markdown.indexOf('```', i + 3)
            if (close === -1) return markdown.length
            i = close + 3
            while (i < markdown.length && markdown[i] === '\n') {
                if (plain >= target) return i
                plain += 1
                i += 1
            }
            continue
        }

        const lineEnd = markdown.indexOf('\n', i)
        const lineEndIdx = lineEnd === -1 ? markdown.length : lineEnd
        const line = markdown.slice(i, lineEndIdx)
        const heading = line.match(/^(#{1,6}\s+)/)
        const prefixLen = heading ? heading[1].length : 0
        const content = line.slice(prefixLen)

        const { plain: nextPlain, li } = emitPlainCharsFromLine(content, target, plain)
        if (nextPlain >= target) {
            return i + prefixLen + li
        }
        plain = nextPlain

        if (lineEndIdx >= markdown.length) {
            return markdown.length
        }

        plain += 1
        i = lineEndIdx + 1
    }

    return markdown.length
}

export function syncEditorScrollFromPreview(wrapper, textarea, previewScrollTop) {
    if (!wrapper || !textarea || wrapper.scrollHeight <= 0) return
    const scale = textarea.scrollHeight / wrapper.scrollHeight
    const maxScroll = Math.max(0, textarea.scrollHeight - textarea.clientHeight)
    textarea.scrollTop = Math.min(maxScroll, Math.max(0, previewScrollTop * scale))
}
