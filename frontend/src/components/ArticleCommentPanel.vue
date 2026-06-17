<template>
    <section class="article-comments" aria-label="文章评论">
        <div class="article-comments__panel">
            <header class="article-comments__head">
                <div class="article-comments__head-main">
                    <svg class="article-comments__head-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <h2 class="article-comments__title">评论</h2>
                    <span v-if="comments.length" class="article-comments__count">{{ comments.length }}</span>
                </div>
            </header>

            <div ref="listEl" class="article-comments__list">
                <div v-if="!comments.length" class="article-comments__empty">
                    <span class="article-comments__empty-icon" aria-hidden="true">💬</span>
                    <p>还没有评论，来抢沙发吧</p>
                </div>

                <div
                    v-for="(item, index) in comments"
                    :key="item.id"
                    class="article-comments__item"
                    :class="{
                        'is-own': isOwn(item),
                        'is-grouped': isGrouped(index),
                    }"
                >
                    <div class="article-comments__avatar-col">
                        <span
                            v-if="!isGrouped(index)"
                            class="article-comments__avatar"
                            :style="{ background: avatarColor(item.author) }"
                            aria-hidden="true"
                        >{{ avatarText(item.author) }}</span>
                    </div>

                    <div class="article-comments__body">
                        <div v-if="!isGrouped(index)" class="article-comments__meta">
                            <span class="article-comments__author">{{ item.author }}</span>
                            <time class="article-comments__time">{{ formatTime(item.createdAt) }}</time>
                        </div>
                        <div class="article-comments__bubble">{{ item.content }}</div>
                    </div>
                </div>
            </div>

            <form class="article-comments__composer" @submit.prevent="submitComment">
                <div class="article-comments__composer-box" :class="{ 'is-focused': composerFocused }">
                    <span
                        class="article-comments__composer-avatar"
                        :style="{ background: avatarColor(nickname) }"
                        aria-hidden="true"
                    >{{ avatarText(nickname) }}</span>

                    <div class="article-comments__composer-main">
                        <textarea
                            ref="inputEl"
                            v-model="draft"
                            rows="1"
                            class="article-comments__input"
                            placeholder="输入评论，Enter 发送"
                            @focus="composerFocused = true"
                            @blur="onComposerBlur"
                            @input="syncInputHeight"
                            @keydown.enter.exact.prevent="submitComment"
                        ></textarea>

                        <div class="article-comments__composer-foot">
                            <span class="article-comments__identity">
                                以
                                <button
                                    v-if="!editingNickname"
                                    type="button"
                                    class="article-comments__identity-name"
                                    @click="startEditNickname"
                                >{{ nickname }}</button>
                                <input
                                    v-else
                                    ref="nicknameInput"
                                    v-model="nicknameDraft"
                                    type="text"
                                    maxlength="20"
                                    class="article-comments__identity-input"
                                    @blur="finishEditNickname"
                                    @keydown.enter.prevent="finishEditNickname"
                                    @keydown.esc.prevent="cancelEditNickname"
                                />
                                发言
                            </span>

                            <button
                                type="submit"
                                class="article-comments__send"
                                :disabled="!draft.trim()"
                                aria-label="发送评论"
                            >
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                    <line x1="22" y1="2" x2="11" y2="13"></line>
                                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
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
            nicknameDraft: '',
            editingNickname: false,
            composerFocused: false,
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
        isOwn(item) {
            return item.author === this.nickname
        },
        isGrouped(index) {
            if (index <= 0) return false
            const prev = this.comments[index - 1]
            const curr = this.comments[index]
            return prev.author === curr.author
        },
        reloadComments(key) {
            this.comments = key ? loadComments(key) : []
            this.$nextTick(() => {
                this.scrollToBottom()
                this.syncInputHeight()
            })
        },
        scrollToBottom() {
            const el = this.$refs.listEl
            if (el) el.scrollTop = el.scrollHeight
        },
        syncInputHeight() {
            this.$nextTick(() => {
                const ta = this.$refs.inputEl
                if (!ta) return
                ta.style.height = 'auto'
                ta.style.height = `${Math.min(120, Math.max(22, ta.scrollHeight))}px`
            })
        },
        onComposerBlur() {
            this.composerFocused = false
            if (!this.editingNickname) return
            this.finishEditNickname()
        },
        startEditNickname() {
            this.nicknameDraft = this.nickname
            this.editingNickname = true
            this.$nextTick(() => this.$refs.nicknameInput?.focus())
        },
        finishEditNickname() {
            this.nickname = setVisitorName(this.nicknameDraft)
            this.editingNickname = false
        },
        cancelEditNickname() {
            this.editingNickname = false
            this.nicknameDraft = this.nickname
        },
        submitComment() {
            const content = this.draft.trim()
            if (!content || !this.articleKey) return

            const author = setVisitorName(this.nickname)
            this.nickname = author
            this.comments = addComment(this.articleKey, { author, content })
            this.draft = ''
            this.$nextTick(() => {
                this.syncInputHeight()
                this.scrollToBottom()
            })
        },
    },
}
</script>

<style scoped>
.article-comments {
    margin-top: 48px;
}

.article-comments__panel {
    border-radius: 12px;
    background: var(--bg-white);
    box-shadow: var(--shadow-card);
    overflow: hidden;
}

.article-comments__head {
    padding: 14px 18px;
    border-bottom: 1px solid var(--border-subtle);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.6) 0%, var(--bg-white) 100%);
}

.article-comments__head-main {
    display: flex;
    align-items: center;
    gap: 8px;
}

.article-comments__head-icon {
    flex-shrink: 0;
    color: var(--text-tertiary);
}

.article-comments__title {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.article-comments__count {
    min-width: 18px;
    height: 18px;
    padding: 0 6px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 500;
    line-height: 18px;
    text-align: center;
    color: var(--text-secondary);
    background: var(--bg-hover);
}

.article-comments__list {
    display: flex;
    flex-direction: column;
    gap: 2px;
    max-height: 420px;
    overflow-y: auto;
    padding: 16px 14px 12px;
    background:
        linear-gradient(var(--bg-white), var(--bg-white)) padding-box,
        linear-gradient(180deg, rgba(31, 35, 41, 0.02) 0%, transparent 48px) border-box;
}

.article-comments__empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 28px 16px 36px;
    color: var(--text-tertiary);
    font-size: 13px;
}

.article-comments__empty-icon {
    font-size: 28px;
    line-height: 1;
    opacity: 0.55;
}

.article-comments__item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 6px 4px;
    border-radius: 8px;
    transition: background 0.15s ease;
}

.article-comments__item:hover {
    background: rgba(31, 35, 41, 0.02);
}

.article-comments__item.is-grouped {
    padding-top: 2px;
}

.article-comments__item.is-own {
    flex-direction: row-reverse;
}

.article-comments__avatar-col {
    width: 36px;
    flex-shrink: 0;
}

.article-comments__avatar,
.article-comments__composer-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    font-size: 14px;
    font-weight: 600;
    color: #fff;
    box-shadow:
        0 0 0 1px rgba(255, 255, 255, 0.35) inset,
        0 1px 2px rgba(31, 35, 41, 0.08);
}

.article-comments__body {
    flex: 1;
    min-width: 0;
    max-width: min(78%, 560px);
}

.article-comments__item.is-own .article-comments__body {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.article-comments__meta {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 4px;
    padding: 0 2px;
}

.article-comments__item.is-own .article-comments__meta {
    flex-direction: row-reverse;
}

.article-comments__author {
    font-size: 12px;
    font-weight: 500;
    color: var(--text-secondary);
}

.article-comments__time {
    font-size: 11px;
    color: var(--text-tertiary);
    font-variant-numeric: tabular-nums;
    opacity: 0;
    transition: opacity 0.15s ease;
}

.article-comments__item:hover .article-comments__time {
    opacity: 1;
}

.article-comments__bubble {
    display: inline-block;
    max-width: 100%;
    padding: 9px 12px;
    border-radius: 12px;
    background: rgba(31, 35, 41, 0.05);
    font-size: 14px;
    line-height: 1.65;
    color: var(--text-primary);
    white-space: pre-wrap;
    word-break: break-word;
    transition: background 0.15s ease, box-shadow 0.15s ease;
}

.article-comments__item:not(.is-own) .article-comments__bubble {
    border-top-left-radius: 4px;
}

.article-comments__item.is-own .article-comments__bubble {
    background: linear-gradient(180deg, #5b7cff 0%, var(--primary) 100%);
    color: #fff;
    border-top-right-radius: 4px;
    box-shadow: 0 2px 8px rgba(79, 110, 247, 0.22);
}

.article-comments__composer {
    padding: 0 14px 14px;
    background: var(--bg-white);
}

.article-comments__composer-box {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    background: var(--bg-hover);
    transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}

.article-comments__composer-box.is-focused {
    border-color: rgba(79, 110, 247, 0.35);
    background: var(--bg-white);
    box-shadow: 0 0 0 3px var(--primary-light);
}

.article-comments__composer-main {
    flex: 1;
    min-width: 0;
}

.article-comments__input {
    display: block;
    width: 100%;
    min-height: 22px;
    max-height: 120px;
    resize: none;
    border: none;
    outline: none;
    background: transparent;
    font-size: 14px;
    line-height: 1.55;
    font-family: inherit;
    color: var(--text-primary);
    padding: 2px 0 0;
}

.article-comments__input::placeholder {
    color: var(--text-tertiary);
}

.article-comments__composer-foot {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--border-subtle);
}

.article-comments__identity {
    font-size: 12px;
    color: var(--text-tertiary);
    line-height: 1.4;
}

.article-comments__identity-name {
    border: none;
    background: none;
    padding: 0 2px;
    margin: 0 1px;
    font: inherit;
    font-weight: 500;
    color: var(--primary);
    cursor: pointer;
    border-radius: 4px;
    transition: background 0.15s ease;
}

.article-comments__identity-name:hover {
    background: var(--primary-light);
}

.article-comments__identity-input {
    width: 88px;
    margin: 0 2px;
    padding: 1px 6px;
    border: 1px solid rgba(79, 110, 247, 0.35);
    border-radius: 6px;
    outline: none;
    font-size: 12px;
    font-family: inherit;
    color: var(--text-primary);
    background: var(--bg-white);
    box-shadow: 0 0 0 2px var(--primary-light);
}

.article-comments__send {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;
    background: var(--primary);
    color: #fff;
    cursor: pointer;
    transition: transform 0.15s ease, background 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 2px 6px rgba(79, 110, 247, 0.28);
}

.article-comments__send:hover:not(:disabled) {
    background: var(--primary-hover);
    transform: translateY(-1px);
}

.article-comments__send:active:not(:disabled) {
    transform: translateY(0);
}

.article-comments__send:disabled {
    opacity: 0.35;
    cursor: not-allowed;
    box-shadow: none;
}

@media (max-width: 768px) {
    .article-comments {
        margin-top: 32px;
    }

    .article-comments__panel {
        border-radius: 10px;
    }

    .article-comments__list {
        max-height: 320px;
        padding-inline: 10px;
    }

    .article-comments__body {
        max-width: 86%;
    }

    .article-comments__time {
        opacity: 1;
    }

    .article-comments__composer {
        padding-inline: 10px;
    }
}
</style>
