<template>
    <aside class="app-sidebar" :class="{ open: open }">
        <div class="app-sidebar-header">
            <SiteBrandLink />
            <div class="app-sidebar-header-actions">
                <button
                    v-if="isLoggedIn"
                    class="app-sidebar-icon-btn"
                    title="写文章"
                    @click="createNewArticle"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                </button>
                <button
                    v-if="showReturnToToc"
                    type="button"
                    class="app-sidebar-icon-btn"
                    title="文章目录"
                    @click="returnToArticleToc"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </button>
                <button
                    v-if="showArticleToc"
                    type="button"
                    class="app-sidebar-icon-btn"
                    title="文章列表"
                    @click="goArticleList"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="15 18 9 12 15 6"></polyline>
                    </svg>
                </button>
                <div class="app-sidebar-menu" v-click-outside="closeHeaderMenu">
                    <button
                        class="app-sidebar-icon-btn"
                        title="更多"
                        :aria-expanded="headerMenuOpen"
                        @click="headerMenuOpen = !headerMenuOpen"
                    >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="5" cy="12" r="1.25" fill="currentColor" stroke="none"></circle>
                            <circle cx="12" cy="12" r="1.25" fill="currentColor" stroke="none"></circle>
                            <circle cx="19" cy="12" r="1.25" fill="currentColor" stroke="none"></circle>
                        </svg>
                    </button>
                    <div v-if="headerMenuOpen" class="app-sidebar-menu-panel">
                        <router-link :to="{ name: 'portal-home' }" class="app-sidebar-menu-item" @click="closeHeaderMenu">
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M3 10.5L12 3L21 10.5"></path>
                                    <path d="M5 10V20H19V10"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">首页</span>
                        </router-link>
                        <router-link to="/search" class="app-sidebar-menu-item" @click="closeHeaderMenu">
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="11" cy="11" r="7"></circle>
                                    <path d="M20 20L16.5 16.5"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">搜索</span>
                        </router-link>
                        <router-link to="/topics" class="app-sidebar-menu-item" @click="closeHeaderMenu">
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M4 9H20"></path>
                                    <path d="M4 15H14"></path>
                                    <path d="M4 5H20"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">话题</span>
                        </router-link>
                        <router-link :to="{ name: 'about' }" class="app-sidebar-menu-item" @click="closeHeaderMenu">
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="12" cy="12" r="9"></circle>
                                    <path d="M12 10V16"></path>
                                    <path d="M12 7H12.01"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">关于</span>
                        </router-link>
                        <router-link :to="{ name: 'links' }" class="app-sidebar-menu-item" @click="closeHeaderMenu">
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">链接</span>
                        </router-link>
                        <div class="app-sidebar-menu-divider"></div>
                        <button
                            v-if="!isLoggedIn"
                            type="button"
                            class="app-sidebar-menu-item"
                            @click="onLoginClick"
                        >
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M15 3H19C20.1 3 21 3.9 21 5V19C21 20.1 20.1 21 19 21H15"></path>
                                    <path d="M10 17L15 12L10 7"></path>
                                    <path d="M15 12H3"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">登录</span>
                        </button>
                        <button
                            v-else
                            type="button"
                            class="app-sidebar-menu-item app-sidebar-menu-item--danger"
                            @click="onLogoutClick"
                        >
                            <span class="app-sidebar-menu-icon" aria-hidden="true">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M9 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H9"></path>
                                    <path d="M16 17L21 12L16 7"></path>
                                    <path d="M21 12H9"></path>
                                </svg>
                            </span>
                            <span class="app-sidebar-menu-label">退出登录</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-sidebar-list">
            <SkeletonArticleToc v-if="showArticleToc && articleViewState.tocLoading" />
            <ArticleToc
                v-else-if="showArticleToc"
                :headings="articleViewState.headings"
                :active-id="articleViewState.activeHeadingId"
                @select="scrollToHeading"
            />
            <template v-else>
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
            </template>
        </div>
    </aside>
</template>

<script>
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'
import SkeletonSidebarList from '@/components/state/SkeletonSidebarList.vue'
import SkeletonArticleToc from '@/components/state/SkeletonArticleToc.vue'
import ArticleToc from '@/components/ArticleToc.vue'
import { articleApi } from '@/api'
import { routeTitleParam, toArticleRoute, toNewArticleRoute, isNewArticleRoute } from '@/utils/articleRoute'
import {
    clearEditorState,
    displayEditorTitle,
    editorState,
    getArticleStatusClass,
} from '@/utils/articleEditorState'
import { articleViewState, hideArticleToc, setActiveHeading, showArticleTocMode } from '@/utils/articleViewState'
import { applyHeadingHighlight, createHeadingObserver, scrollToArticleHeading } from '@/utils/articleTocNav'
import { authState, clearSession, isAuthenticated } from '@/utils/authSession'
import { clearLocalDraft, hasLocalDraft } from '@/utils/editorDraft'
import SiteBrandLink from '@/components/SiteBrandLink.vue'

export default {
    name: 'AppSidebar',
    components: { EmptyState, ErrorState, SkeletonSidebarList, SkeletonArticleToc, ArticleToc, SiteBrandLink },
    directives: {
        clickOutside: {
            mounted(el, binding) {
                el._clickOutside = (e) => {
                    if (!el.contains(e.target)) binding.value()
                }
                document.addEventListener('click', el._clickOutside)
            },
            unmounted(el) {
                document.removeEventListener('click', el._clickOutside)
            },
        },
    },
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
            articleViewState,
            headerMenuOpen: false,
        }
    },
    computed: {
        showArticleToc() {
            return (
                this.$route.name === 'public-article'
                && !articleViewState.tocSuppressed
            )
        },
        showReturnToToc() {
            return (
                this.$route.name === 'public-article'
                && articleViewState.tocSuppressed
            )
        },
        isLoggedIn() {
            void authState.token
            return isAuthenticated()
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
        '$route'(to, from) {
            this.syncActiveTitle()
            this.headerMenuOpen = false
            if (to.name === 'public-article') {
                const toTitle = routeTitleParam(to)
                const fromTitle = from ? routeTitleParam(from) : null
                // 仅从非文章页进入时默认展示目录；文章间切换保留列表/目录状态
                if (toTitle !== fromTitle && from?.name !== 'public-article') {
                    showArticleTocMode()
                }
            }
        },
        showArticleToc(val) {
            if (val) {
                this.$nextTick(() => this.bindHeadingObserver())
            } else {
                this.unbindHeadingObserver()
                applyHeadingHighlight('')
            }
        },
        'articleViewState.headings'() {
            if (this.showArticleToc) {
                this.$nextTick(() => this.bindHeadingObserver())
            }
        },
    },
    mounted() {
        this.loadArticles()
        this.syncActiveTitle()
        this._onRefresh = () => this.loadArticles({ force: true, silent: true })
        window.addEventListener('sidebar-articles-refresh', this._onRefresh)
        this._onAuthChanged = () => this.onAuthChange()
        window.addEventListener('auth-changed', this._onAuthChanged)
    },
    beforeUnmount() {
        window.removeEventListener('sidebar-articles-refresh', this._onRefresh)
        window.removeEventListener('auth-changed', this._onAuthChanged)
        this.unbindHeadingObserver()
        applyHeadingHighlight('')
    },
    methods: {
        closeHeaderMenu() {
            this.headerMenuOpen = false
        },
        onLoginClick() {
            this.closeHeaderMenu()
            this.$emit('login-required')
        },
        onLogoutClick() {
            this.closeHeaderMenu()
            this.logout()
        },
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
            if (routeTitleParam(this.$route) === a.title) {
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
            clearSession()
            this.onAuthChange()
            this.$router.push('/')
        },
        goArticleList() {
            hideArticleToc()
        },
        returnToArticleToc() {
            showArticleTocMode()
        },
        bindHeadingObserver() {
            this.unbindHeadingObserver()
            this._headingObserver = createHeadingObserver((id) => {
                setActiveHeading(id)
            })
        },
        unbindHeadingObserver() {
            if (this._headingObserver) {
                this._headingObserver.disconnect()
                this._headingObserver = null
            }
        },
        scrollToHeading(id) {
            if (!id) return
            if (scrollToArticleHeading(id)) {
                setActiveHeading(id)
            }
            if (window.matchMedia('(max-width: 768px)').matches) {
                this.$emit('close')
            }
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
    gap: 6px;
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
    flex-shrink: 0;
}

.app-sidebar-menu {
    position: relative;
}

.app-sidebar-menu-panel {
    position: absolute;
    top: calc(100% + 6px);
    right: 0;
    z-index: 30;
    min-width: 140px;
    max-height: min(70vh, 420px);
    overflow-y: auto;
    padding: 5px;
    border-radius: 8px;
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
}

.app-sidebar-menu-divider {
    height: 1px;
    margin: 3px 4px;
    background: var(--border-subtle);
}

.app-sidebar-menu-item {
    display: flex;
    align-items: center;
    gap: 9px;
    width: 100%;
    padding: 8px 10px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--text-primary);
    font-size: 13px;
    text-align: left;
    text-decoration: none;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s ease, color 0.15s ease;
}

.app-sidebar-menu-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 16px;
    height: 16px;
    color: var(--text-tertiary);
    transition: color 0.15s ease;
}

.app-sidebar-menu-label {
    flex: 1;
    min-width: 0;
    line-height: 1.35;
}

.app-sidebar-menu-item:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

.app-sidebar-menu-item:hover .app-sidebar-menu-icon {
    color: var(--primary);
}

.app-sidebar-menu-item--danger {
    color: #dc2626;
}

.app-sidebar-menu-item--danger .app-sidebar-menu-icon {
    color: #dc2626;
}

.app-sidebar-menu-item--danger:hover {
    background: #fef2f2;
    color: #b91c1c;
}

.app-sidebar-menu-item--danger:hover .app-sidebar-menu-icon {
    color: #b91c1c;
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

.app-sidebar-icon-btn[aria-expanded="true"] {
    background: var(--primary-light);
    color: var(--primary);
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
