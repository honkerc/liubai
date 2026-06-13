<template>
    <aside class="app-sidebar" :class="{ open: open }">
        <div class="app-sidebar-header">
            <SiteBrandLink />
            <div class="app-sidebar-header-actions">
                <router-link to="/topics" class="app-sidebar-icon-btn" title="话题">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                        <line x1="7" y1="7" x2="7.01" y2="7"></line>
                    </svg>
                </router-link>
                <router-link to="/search" class="app-sidebar-icon-btn" title="搜索">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="7"></circle>
                        <line x1="20" y1="20" x2="16.5" y2="16.5"></line>
                    </svg>
                </router-link>
                <button class="app-sidebar-icon-btn" title="写文章" @click="createNewArticle">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                </button>
                <button v-if="!isLoggedIn" class="app-sidebar-icon-btn" @click="$emit('login-required')" title="登录">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                        <polyline points="10 17 15 12 10 7"></polyline>
                        <line x1="15" y1="12" x2="3" y2="12"></line>
                    </svg>
                </button>
                <button v-else class="app-sidebar-icon-btn" @click="logout" title="退出">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                </button>
            </div>
        </div>
        <div class="app-sidebar-list">
            <SkeletonSidebarList v-if="loading" />
            <ErrorState
                v-else-if="error"
                compact
                align="left"
                title="加载失败"
                description="文章列表未能加载"
                @retry="loadArticles({ force: true })"
            />
            <template v-else>
                <div
                    v-for="a in displayArticles"
                    :key="a.id"
                    class="app-sidebar-item"
                    :class="{ active: isItemActive(a) }"
                    @click="selectArticle(a)"
                >
                    <div class="app-sidebar-item-main">
                        <div class="app-sidebar-item-row">
                            <span
                                class="app-sidebar-status-dot"
                                :class="statusClass(a)"
                            ></span>
                            <span class="app-sidebar-item-title">{{ a.title }}</span>
                        </div>
                        <span class="app-sidebar-item-date">{{ formatDate(a.created_at) }}</span>
                    </div>
                    <div
                        v-if="showItemActions(a)"
                        class="app-sidebar-item-actions"
                    >
                        <button
                            v-if="isLoggedIn || a.is_pinned"
                            class="app-sidebar-item-action"
                            :class="{ 'is-pinned': a.is_pinned, 'is-readonly': !isLoggedIn }"
                            :title="isLoggedIn ? (a.is_pinned ? '取消置顶' : '置顶') : '置顶'"
                            :disabled="!isLoggedIn || pinningId === a.id"
                            @click.stop="togglePin(a)"
                        >
                            <svg
                                width="13"
                                height="13"
                                viewBox="0 0 24 24"
                                :fill="a.is_pinned ? 'currentColor' : 'none'"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path d="M16 12V4h1V2H7v2h1v8l-2 2v2h5v6l1 1 1-1v-6h5v-2l-2-2z"></path>
                            </svg>
                        </button>
                        <button
                            v-if="isLoggedIn"
                            class="app-sidebar-item-action app-sidebar-item-action--danger"
                            title="删除"
                            @click.stop="deleteArticle(a)"
                        >
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                        </button>
                    </div>
                </div>
                <EmptyState
                    v-if="displayArticles.length === 0"
                    compact
                    align="left"
                    :show-icon="false"
                    title="暂无文章"
                    :description="isLoggedIn ? '点击上方 + 开始写作' : ''"
                />
            </template>
        </div>
    </aside>
</template>

<script>
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'
import SkeletonSidebarList from '@/components/state/SkeletonSidebarList.vue'
import { articleApi } from '@/api'
import { routeTitleParam, toArticleRoute, toNewArticleRoute, isNewArticleRoute } from '@/utils/articleRoute'
import {
    clearEditorState,
    displayEditorTitle,
    editorState,
    getArticleStatusClass,
} from '@/utils/articleEditorState'
import { clearLocalDraft, hasLocalDraft } from '@/utils/editorDraft'
import SiteBrandLink from '@/components/SiteBrandLink.vue'

export default {
    name: 'AppSidebar',
    components: { EmptyState, ErrorState, SkeletonSidebarList, SiteBrandLink },
    props: {
        open: { type: Boolean, default: true },
    },
    emits: ['close', 'login-required'],
    data() {
        return {
            articles: [],
            loading: true,
            error: false,
            loaded: false,
            authMode: null,
            _loadInFlight: null,
            pinningId: null,
            activeTitle: null,
        }
    },
    computed: {
        isLoggedIn() {
            return !!localStorage.getItem('token')
        },
        displayArticles() {
            const articles = this.articles.map(a => ({ ...a }))
            if (!this.isLoggedIn || !editorState.inEditor) return articles

            const liveTitle = displayEditorTitle(editorState.title)
            const livePublished = editorState.isPublished
            const livePinned = editorState.isPinned
            const liveCreatedAt = editorState.createdAt

            if (editorState.articleId) {
                const idx = articles.findIndex(a => a.id === editorState.articleId)
                if (idx >= 0) {
                    articles[idx] = {
                        ...articles[idx],
                        title: liveTitle,
                        is_published: livePublished,
                        is_pinned: livePinned,
                        created_at: articles[idx].created_at || liveCreatedAt,
                    }
                } else {
                    articles.unshift({
                        id: editorState.articleId,
                        title: liveTitle,
                        is_published: livePublished,
                        is_pinned: livePinned,
                        created_at: liveCreatedAt,
                    })
                }
                return this.sortArticles(articles)
            }

            articles.unshift({
                id: '__current__',
                title: liveTitle,
                is_published: livePublished,
                is_pinned: livePinned,
                created_at: liveCreatedAt,
            })
            return this.sortArticles(articles)
        },
    },
    watch: {
        '$route'() {
            this.syncActiveTitle()
        },
    },
    mounted() {
        this.loadArticles()
        this.syncActiveTitle()
        this._onRefresh = () => this.loadArticles({ force: true, silent: true })
        window.addEventListener('sidebar-articles-refresh', this._onRefresh)
    },
    beforeUnmount() {
        window.removeEventListener('sidebar-articles-refresh', this._onRefresh)
    },
    methods: {
        onAuthChange() {
            this.loaded = false
            this.authMode = null
            this.loadArticles({ force: true, silent: true })
        },
        syncActiveTitle() {
            this.activeTitle = routeTitleParam(this.$route) || null
        },
        sortArticles(list) {
            return [...list].sort((a, b) => {
                if (a.is_pinned !== b.is_pinned) return Number(b.is_pinned) - Number(a.is_pinned)
                return new Date(b.created_at) - new Date(a.created_at)
            })
        },
        async loadArticles({ force = false, silent = false } = {}) {
            const authMode = this.isLoggedIn ? 'logged-in' : 'guest'
            if (!force && this.loaded && this.authMode === authMode) {
                return
            }
            if (this._loadInFlight) {
                return this._loadInFlight
            }

            const showSkeleton = !silent && !this.loaded
            if (showSkeleton) {
                this.loading = true
            }
            this.error = false

            this._loadInFlight = (async () => {
                try {
                    const data = this.isLoggedIn
                        ? await articleApi.listAll()
                        : await articleApi.list({ page: 1, page_size: 50 })
                    this.articles = data.items || data
                    this.loaded = true
                    this.authMode = authMode
                } catch (e) {
                    console.error('Failed to load sidebar articles:', e)
                    if (!this.loaded) {
                        this.articles = []
                    }
                    this.error = true
                } finally {
                    this.loading = false
                    this._loadInFlight = null
                }
            })()

            return this._loadInFlight
        },
        isRealArticle(a) {
            return a.id && a.id !== '__current__'
        },
        showItemActions(a) {
            if (!this.isRealArticle(a)) return false
            if (a.is_pinned) return true
            return this.isLoggedIn
        },
        isItemActive(a) {
            if (editorState.inEditor) {
                if (editorState.articleId) return a.id === editorState.articleId
                if (a.id === '__current__') return true
            }
            const routeTitle = routeTitleParam(this.$route)
            if (routeTitle) return a.title === routeTitle
            return a.title === this.activeTitle
        },
        statusClass(a) {
            const isActive = this.isItemActive(a)
            const saveStatus = isActive && editorState.inEditor ? editorState.saveStatus : 'saved'
            return getArticleStatusClass(a, { isActive, saveStatus })
        },
        selectArticle(a) {
            if (a.id === '__current__') {
                this.$router.push(toNewArticleRoute())
                this.$emit('close')
                return
            }
            this.activeTitle = a.title
            this.$router.push(toArticleRoute(a.title))
            this.$emit('close')
        },
        async togglePin(a) {
            if (!this.isLoggedIn || !this.isRealArticle(a)) return
            if (this.pinningId === a.id) return

            const next = !a.is_pinned
            this.pinningId = a.id
            try {
                await articleApi.update(a.id, { is_pinned: next })
                const idx = this.articles.findIndex(x => x.id === a.id)
                if (idx >= 0) {
                    this.articles[idx] = { ...this.articles[idx], is_pinned: next }
                    this.articles = this.sortArticles(this.articles)
                }
                if (editorState.articleId === a.id) {
                    editorState.isPinned = next
                }
                window.dispatchEvent(new CustomEvent('article-field-updated', {
                    detail: { id: a.id, is_pinned: next },
                }))
                this.$toast.success(next ? '已置顶' : '已取消置顶')
            } catch (e) {
                console.error('Failed to toggle pin:', e)
                this.$toast.error('操作失败: ' + (e.message || '未知错误'))
            } finally {
                this.pinningId = null
            }
        },
        async deleteArticle(a) {
            if (!this.isLoggedIn || !this.isRealArticle(a)) return
            if (!confirm(`确定要删除「${a.title}」吗？`)) return

            const deletingActive = this.isItemActive(a)
            try {
                await articleApi.delete(a.id)
                await this.loadArticles({ force: true, silent: true })
                this.$toast.success('已删除')

                if (!deletingActive) return

                clearEditorState()
                const remaining = this.displayArticles
                if (remaining.length > 0) {
                    this.selectArticle(remaining[0])
                } else {
                    this.$router.push({ name: 'portal-home' })
                }
            } catch (e) {
                console.error('Failed to delete article:', e)
                this.$toast.error('删除失败: ' + (e.message || '未知错误'))
            }
        },
        createNewArticle() {
            if (!this.isLoggedIn) {
                this.$emit('login-required')
                return
            }
            if (hasLocalDraft()) {
                const ok = confirm('本地有未保存的草稿内容，新建文章将清空这些内容，是否继续？')
                if (!ok) return
            }
            clearLocalDraft()
            if (this.$route.name === 'new-article') {
                this.$router.replace(toNewArticleRoute({ fresh: true }))
            } else {
                this.$router.push(toNewArticleRoute({ fresh: true }))
            }
        },
        logout() {
            localStorage.removeItem('token')
            this.onAuthChange()
            this.$router.push('/')
        },
        formatDate(dateStr) {
            if (!dateStr) return ''
            const d = new Date(dateStr)
            const pad = (n) => String(n).padStart(2, '0')
            return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
        },
    },
}
</script>

<style scoped>
.app-sidebar {
    width: 33.33%;
    min-width: 280px;
    max-width: 400px;
    border-radius: 8px;
    display: flex;
    padding: 6px;
    flex-direction: column;
    background: var(--bg-white);
    overflow: hidden;
    border: 1px solid var(--border-card);
}

.app-sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 10px 12px;
    flex-shrink: 0;
    min-width: 0;
}

.app-sidebar-header :deep(.site-brand) {
    flex: 1;
    min-width: 0;
}

.app-sidebar-header-actions {
    display: flex;
    align-items: center;
    gap: 4px;
}

.app-sidebar-icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border: none;
    border-radius: 4px;
    background: transparent;
    color: var(--text-tertiary);
    text-decoration: none;
    cursor: pointer;
    transition: color 0.15s, background 0.15s;
    font-family: inherit;
    padding: 0;
}

.app-sidebar-icon-btn:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

.app-sidebar-list {
    flex: 1;
    overflow-y: auto;
    scrollbar-width: none;
}

.app-sidebar-list::-webkit-scrollbar {
    display: none;
}

.app-sidebar-item {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 8px 6px 12px;
    cursor: pointer;
    transition: all 0.15s;
    margin: 3px 0;
    border-radius: 6px;
}

.app-sidebar-item-main {
    flex: 1;
    min-width: 0;
}

.app-sidebar-item-actions {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 2px;
}

.app-sidebar-item-action {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--icon-color);
    cursor: pointer;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s, background 0.15s, color 0.15s;
    padding: 0;
    font-family: inherit;
}

.app-sidebar-item-action:disabled {
    opacity: 0.5;
    cursor: wait;
    pointer-events: none;
}

.app-sidebar-item-action.is-pinned {
    color: var(--primary);
    opacity: 1;
    pointer-events: auto;
}

.app-sidebar-item-action.is-readonly {
    cursor: default;
    pointer-events: none;
}

.app-sidebar-item-action.is-readonly.is-pinned:hover {
    background: transparent;
}

.app-sidebar-item:hover .app-sidebar-item-action {
    opacity: 1;
    pointer-events: auto;
}

.app-sidebar-item-action.is-readonly {
    pointer-events: none;
}

.app-sidebar-item:hover .app-sidebar-item-action.is-readonly {
    pointer-events: none;
}

.app-sidebar-item-action:hover:not(:disabled):not(.is-readonly):not(.app-sidebar-item-action--danger) {
    background: var(--bg-hover);
    color: var(--text-secondary);
}

.app-sidebar-item-action.is-pinned:hover:not(:disabled):not(.is-readonly) {
    color: var(--primary);
    background: var(--primary-light);
}

.app-sidebar-item-action.app-sidebar-item-action--danger:hover:not(:disabled) {
    background: #fef2f2;
    color: #dc2626;
}

.app-sidebar-item:hover {
    background: var(--bg-hover);
}

.app-sidebar-item.active {
    background: rgb(231 237 253);
}

.app-sidebar-item-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
}

.app-sidebar-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

.app-sidebar-status-dot.published {
    background: #22c55e;
}

.app-sidebar-status-dot.draft {
    background: #9ca3af;
}

.app-sidebar-status-dot.editing-unsaved {
    background: #ef4444;
}

.app-sidebar-item-title {
    font-size: 14px;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    min-width: 0;
}

.app-sidebar-item-date {
    display: block;
    font-size: 12px;
    color: var(--text-tertiary);
}

@media (max-width: 992px) {
    .app-sidebar {
        min-width: 240px;
    }
}

@media (max-width: 768px) {
    .app-sidebar {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        z-index: 150;
        width: min(88vw, 320px);
        min-width: 0;
        max-width: none;
        max-height: none;
        border-radius: 0;
        padding-top: env(safe-area-inset-top, 0px);
        transform: translateX(-105%);
        transition: transform 0.22s ease;
        box-shadow: none;
    }

    .app-sidebar.open {
        transform: translateX(0);
        box-shadow: var(--shadow-md);
    }

    .app-sidebar-item-action {
        opacity: 1;
        pointer-events: auto;
    }

    .app-sidebar-item-action.is-readonly {
        pointer-events: none;
    }
}

@media (hover: none) and (pointer: coarse) {
    .app-sidebar-item-action {
        opacity: 1;
        pointer-events: auto;
    }

    .app-sidebar-item-action.is-readonly {
        pointer-events: none;
    }
}
</style>
