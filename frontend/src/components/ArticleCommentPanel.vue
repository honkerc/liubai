<template>
    <section class="article-comments" aria-label="文章评论">
        <div class="article-comments__head">
            <h2 class="article-comments__title">评论</h2>
            <span class="article-comments__count">{{ comments.length }}</span>
        </div>

        <div ref="listEl" class="article-comments__list">
            <div
                v-for="item in comments"
                :key="item.id"
                class="article-comments__item"
            >
                <span
                    class="article-comments__avatar"
                    :style="{ background: avatarColor(item.author) }"
                    aria-hidden="true"
                >{{ avatarText(item.author) }}</span>
                <div class="article-comments__bubble-wrap">
                    <div class="article-comments__meta">
                        <span class="article-comments__author">{{ item.author }}</span>
                        <time class="article-comments__time">{{ formatTime(item.createdAt) }}</time>
                    </div>
                    <div class="article-comments__bubble">{{ item.content }}</div>
                </div>
            </div>
        </div>

        <form class="article-comments__composer" @submit.prevent="submitComment">
            <div class="article-comments__composer-top">
                <label class="article-comments__nickname">
                    <span class="article-comments__nickname-label">昵称</span>
                    <input
                        v-model="nickname"
                        type="text"
                        maxlength="20"
                        class="article-comments__nickname-input"
                        placeholder="路人甲"
                    />
                </label>
            </div>
            <div class="article-comments__composer-row">
                <textarea
                    ref="inputEl"
                    v-model="draft"
                    rows="1"
                    class="article-comments__input"
                    placeholder="说点什么…"
                    @keydown.enter.exact.prevent="submitComment"
                ></textarea>
                <button type="submit" class="article-comments__send" :disabled="!draft.trim()">
                    发送
                </button>
            </div>
        </form>
    </section>
</template>

<script>
import {
    addComment,
    avatarColor,
    formatCommentTime,
    getVisitorName,
    loadComments,
    setVisitorName,
} from '@/utils/articleComments'

export default {
    name: 'ArticleCommentPanel',
    props: {
        articleKey: { type: String, default: '' },
    },
    data() {
        return {
            comments: [],
            draft: '',
            nickname: getVisitorName(),
        }
    },
    watch: {
        articleKey: {
            immediate: true,
            handler(key) {
                this.reloadComments(key)
            },
        },
    },
    methods: {
        avatarColor,
        formatTime: formatCommentTime,
        avatarText(name) {
            return String(name || '路').slice(0, 1)
        },
        reloadComments(key) {
            this.comments = key ? loadComments(key) : []
            this.$nextTick(this.scrollToBottom)
        },
        scrollToBottom() {
            const el = this.$refs.listEl
            if (el) el.scrollTop = el.scrollHeight
        },
        submitComment() {
            const content = this.draft.trim()
            if (!content || !this.articleKey) return

            const author = setVisitorName(this.nickname)
            this.nickname = author
            this.comments = addComment(this.articleKey, { author, content })
            this.draft = ''
            this.$nextTick(this.scrollToBottom)
        },
    },
}
</script>

<style scoped>
.article-comments {
    margin-top: 40px;
    padding-top: 24px;
    border-top: 1px solid var(--border-color);
}

.article-comments__head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
}

.article-comments__title {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.article-comments__count {
    min-width: 20px;
    height: 20px;
    padding: 0 6px;
    border-radius: 999px;
    font-size: 12px;
    line-height: 20px;
    text-align: center;
    color: var(--text-secondary);
    background: var(--bg-card);
}

.article-comments__list {
    display: flex;
    flex-direction: column;
    gap: 14px;
    max-height: 360px;
    overflow-y: auto;
    margin-bottom: 16px;
    padding-right: 4px;
    scrollbar-width: thin;
}

.article-comments__item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.article-comments__avatar {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 600;
    color: #fff;
}

.article-comments__bubble-wrap {
    flex: 1;
    min-width: 0;
}

.article-comments__meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.article-comments__author {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
}

.article-comments__time {
    font-size: 12px;
    color: var(--text-tertiary);
}

.article-comments__bubble {
    display: inline-block;
    max-width: 100%;
    padding: 10px 12px;
    border-radius: 10px;
    border-top-left-radius: 4px;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-primary);
    white-space: pre-wrap;
    word-break: break-word;
}

.article-comments__composer {
    padding: 10px 12px;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    background: var(--bg-white);
    box-shadow: var(--shadow-sm);
}

.article-comments__composer-top {
    margin-bottom: 8px;
}

.article-comments__nickname {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.article-comments__nickname-label {
    font-size: 12px;
    color: var(--text-tertiary);
}

.article-comments__nickname-input {
    width: 100px;
    border: none;
    outline: none;
    background: transparent;
    font-size: 13px;
    font-family: inherit;
    color: var(--text-secondary);
    padding: 0;
}

.article-comments__composer-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
}

.article-comments__input {
    flex: 1;
    min-width: 0;
    min-height: 38px;
    max-height: 120px;
    resize: none;
    border: none;
    outline: none;
    background: transparent;
    font-size: 14px;
    line-height: 1.5;
    font-family: inherit;
    color: var(--text-primary);
    padding: 6px 0;
}

.article-comments__input::placeholder {
    color: var(--text-tertiary);
}

.article-comments__send {
    flex-shrink: 0;
    height: 32px;
    padding: 0 14px;
    border: none;
    border-radius: 8px;
    background: var(--primary);
    color: #fff;
    font-size: 13px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s, opacity 0.15s;
}

.article-comments__send:hover:not(:disabled) {
    background: var(--primary-hover);
}

.article-comments__send:disabled {
    opacity: 0.45;
    cursor: not-allowed;
}

@media (max-width: 768px) {
    .article-comments {
        margin-top: 28px;
        padding-top: 20px;
    }

    .article-comments__list {
        max-height: 280px;
    }
}
</style>
