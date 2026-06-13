import { Marked, Renderer } from 'marked'
import hljs from 'highlight.js'

const renderer = new Renderer()
renderer.code = function ({ text, lang }) {
    const language = lang || ''
    let highlighted
    if (language && hljs.getLanguage(language)) {
        try {
            highlighted = hljs.highlight(text, { language }).value
        } catch {
            highlighted = text
        }
    } else {
        try {
            highlighted = hljs.highlightAuto(text).value
        } catch {
            highlighted = text
        }
    }
    const langAttr = language ? ` data-language="${language}"` : ''
    return `<pre${langAttr}><code class="hljs language-${language}">${highlighted}</code></pre>`
}

export const marked = new Marked({
    renderer,
    breaks: true,
    gfm: true,
})

export function parseMarkdown(content) {
    if (!content || !content.trim()) return ''
    try {
        let html = marked.parse(content)
        html = html.replace(/<(h[1-6])(.*?)>(.*?)<\/\1>/g, (match, tag, attrs, text) => {
            const id = text.replace(/<[^>]*>/g, '').toLowerCase().replace(/[^\w\u4e00-\u9fa5]+/g, '-').replace(/(^-|-$)/g, '')
            return `<${tag}${attrs} id="${id}">${text}</${tag}>`
        })
        return html
    } catch {
        return content
    }
}

function stripTags(html) {
    return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
}

export function htmlToMarkdown(html) {
    if (!html) return ''
    let text = html
        .replace(/<br\s*\/?>/gi, '\n')
        .replace(/<\/p>\s*<p[^>]*>/gi, '\n\n')
        .replace(/<\/div>\s*<div[^>]*>/gi, '\n\n')

    text = text.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, (_, c) => `# ${stripTags(c)}\n\n`)
    text = text.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, (_, c) => `## ${stripTags(c)}\n\n`)
    text = text.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, (_, c) => `### ${stripTags(c)}\n\n`)
    text = text.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, (_, c) => `#### ${stripTags(c)}\n\n`)
    text = text.replace(/<strong>([\s\S]*?)<\/strong>/gi, '**$1**')
    text = text.replace(/<b>([\s\S]*?)<\/b>/gi, '**$1**')
    text = text.replace(/<em>([\s\S]*?)<\/em>/gi, '*$1*')
    text = text.replace(/<i>([\s\S]*?)<\/i>/gi, '*$1*')
    text = text.replace(/<del>([\s\S]*?)<\/del>/gi, '~~$1~~')
    text = text.replace(/<s>([\s\S]*?)<\/s>/gi, '~~$1~~')
    text = text.replace(/<strike>([\s\S]*?)<\/strike>/gi, '~~$1~~')
    text = text.replace(/<code>([\s\S]*?)<\/code>/gi, '`$1`')
    text = text.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)')
    text = text.replace(/<li>([\s\S]*?)<\/li>/gi, '- $1\n')
    text = text.replace(/<blockquote[^>]*>([\s\S]*?)<\/blockquote>/gi, (_, c) => {
        const lines = stripTags(c).split('\n').filter(Boolean)
        return lines.map(l => `> ${l}`).join('\n') + '\n\n'
    })
    text = text.replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, '```\n$1\n```\n\n')
    text = text.replace(/<hr\s*\/?>/gi, '\n---\n\n')
    text = text.replace(/<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>/gi, '![$2]($1)')
    text = text.replace(/<img[^>]*src="([^"]*)"[^>]*>/gi, '![]($1)')
    text = text.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '$1\n\n')
    text = text.replace(/<div[^>]*>([\s\S]*?)<\/div>/gi, '$1\n\n')
    text = text.replace(/<[^>]*>/g, '')
    text = text.replace(/\n{3,}/g, '\n\n')
    return text.trim()
}
