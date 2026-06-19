<template>
    <div
        class="post-view"
        :class="{ 'post-view--editing': showBottomBar }"
    >
        <input
            ref="fileInput"
            type="file"
            class="hidden-input"
            :accept="uploadAccept"
            @change="onFileSelected"
        >

        <div
            v-if="uploading"
            class="upload-status"
            role="status"
            aria-live="polite"
        >
            <div class="upload-status-head">
                <span class="upload-status-name" :title="uploadFileName">{{ uploadFileName }}</span>
                <span class="upload-status-meta">{{ uploadStatusMeta }}</span>
            </div>
            <div class="upload-status-track" :class="{ 'is-indeterminate': uploadIndeterminate }">
                <div
                    class="upload-status-bar"
                    :style="uploadIndeterminate ? undefined : { width: uploadProgress + '%' }"
                ></div>
            </div>
        </div>

        <div
            v-if="showBottomBar && showSaveStatus"
            class="save-status"
            :class="'is-' + saveStatusDisplay"
        >
            <span class="save-status-dot"></span>
            <span class="save-status-text">{{ saveStatusLabel }}</span>
        </div>

        <div ref="detailWrapper" class="detail-wrapper page">
            <SkeletonArticleDetail v-if="showArticleDetailLoading" />

            <!-- 登录用户：直接编辑 -->
            <template v-else-if="isEditablePage">
                <div class="detail-container detail-container--edit">
                    <article :key="articleId || routeArticleTitle" class="detail-article">
                        <div class="detail-header">
                            <h1
                                ref="titleEl"
                                class="detail-title detail-editable"
                                :class="{ 'is-placeholder': !title.trim() && activeEditField !== 'title' }"
                                :contenteditable="activeEditField === 'title'"
                                data-placeholder="请输入标题"
                                @dblclick="onTitleClick"
                                @input="onTitleEditableInput"
                                @paste="onTitlePaste"
                                @blur="leaveEdit('title')"
                                @keydown.enter.prevent="onTitleEnter"
                            ></h1>

                            <div class="detail-subtitle detail-editable">
                                <router-link
                                    v-if="activeEditField !== 'topic' && topic"
                                    :to="toTopicRoute(topic)"
                                    class="detail-topic-tag"
                                    title="查看话题，双击编辑"
                                    @dblclick.prevent="onTopicClick"
                                >#{{ topic }}</router-link>
                                <span
                                    v-else-if="activeEditField !== 'topic'"
                                    class="detail-topic-placeholder"
                                    @dblclick.prevent="onTopicClick"
                                >#添加话题（可选）</span>
                                <span v-else class="detail-topic-edit">
                                    <span class="detail-topic-hash">#</span>
                                    <input
                                        ref="topicInput"
                                        v-model="topic"
                                        type="text"
                                        class="detail-topic-tag detail-topic-field"
                                        placeholder="添加话题（可选）"
                                        maxlength="50"
                                        @input="scheduleSave"
                                        @blur="leaveEdit('topic')"
                                        @keydown.enter.prevent="$refs.topicInput?.blur()"
                                    />
                                </span>
                            </div>
                        </div>

                        <div
                            v-if="bodyEditMode"
                            class="detail-content markdown-body detail-body-edit"
                        >
                            <textarea
                                ref="textarea"
                                v-model="rawContent"
                                class="detail-editor-textarea"
                                placeholder="开始写作… (Ctrl+S 保存)"
                                spellcheck="false"
                                @input="onContentInput"
                                @keydown="onTextareaKeydown"
                                @paste="onTextareaPaste"
                            ></textarea>
                        </div>

                        <div
                            v-else
                            class="detail-content markdown-body detail-content-preview detail-content-preview--clickable"
                            v-html="renderedHtml || emptyContentHtml"
                            title="双击正文进入编辑"
                            @dblclick="onPreviewClick"
                        ></div>
                    </article>
                </div>
            </template>

            <!-- 未登录：只读详情 -->
            <template v-else>
                <div class="detail-container" v-if="article">
                    <article class="detail-article">
                        <div class="detail-header">
                            <h1 class="detail-title">{{ article.title }}</h1>
                            <p v-if="article.topic" class="detail-subtitle">
                                <router-link
                                    :to="toTopicRoute(article.topic)"
                                    class="detail-topic-tag"
                                >#{{ article.topic }}</router-link>
                            </p>
                        </div>
                        <div class="detail-content markdown-body" v-html="renderedContent"></div>
                    </article>
                </div>
                <EmptyState
                    v-else-if="loadError === 'notfound'"
                    title="文章不存在"
                    description="该文章可能已被删除或链接有误"
                >
                    <router-link :to="{ name: 'portal-home' }">返回首页</router-link>
                </EmptyState>
                <ErrorState
                    v-else-if="loadError === 'network'"
                    @retry="retryLoadArticle"
                />
            </template>
        </div>

        <div v-if="showBottomBar" class="editor-toolbar">
            <div class="editor-toolbar-pill">
                <button
                    class="toolbar-btn"
                    :class="{ active: !bodyEditMode }"
                    @click="togglePreview"
                    title="预览 / 编辑"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                </button>
                <button class="toolbar-btn" @click="insertCodeBlock" title="插入代码块">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <polyline points="16 18 22 12 16 6"></polyline>
                        <polyline points="8 6 2 12 8 18"></polyline>
                    </svg>
                </button>
                <button class="toolbar-btn" @click="insertTable" title="插入 3×3 表格">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                        <line x1="3" y1="9" x2="21" y2="9"></line>
                        <line x1="3" y1="15" x2="21" y2="15"></line>
                        <line x1="9" y1="3" x2="9" y2="21"></line>
                    </svg>
                </button>
                <button class="toolbar-btn" @click="insertBulletList" title="插入 3 项无序列表">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <line x1="9" y1="6" x2="20" y2="6"></line>
                        <line x1="9" y1="12" x2="20" y2="12"></line>
                        <line x1="9" y1="18" x2="20" y2="18"></line>
                        <circle cx="5" cy="6" r="1.5" fill="currentColor" stroke="none"></circle>
                        <circle cx="5" cy="12" r="1.5" fill="currentColor" stroke="none"></circle>
                        <circle cx="5" cy="18" r="1.5" fill="currentColor" stroke="none"></circle>
                    </svg>
                </button>
                <button class="toolbar-btn" @click="insertOrderedList" title="插入 3 项数字列表">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <line x1="10" y1="6" x2="20" y2="6"></line>
                        <line x1="10" y1="12" x2="20" y2="12"></line>
                        <line x1="10" y1="18" x2="20" y2="18"></line>
                        <path d="M4 5h2v4H4zm0 6h2v4H4z" stroke="none" fill="currentColor"></path>
                    </svg>
                </button>
                <button class="toolbar-btn" @click="insertTaskList" title="插入 3 项任务列表">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="3" y="3" width="6" height="6" rx="1"></rect>
                        <rect x="3" y="10" width="6" height="6" rx="1"></rect>
                        <rect x="3" y="17" width="6" height="6" rx="1"></rect>
                        <line x1="13" y1="6" x2="21" y2="6"></line>
                        <line x1="13" y1="13" x2="21" y2="13"></line>
                        <line x1="13" y1="20" x2="21" y2="20"></line>
                    </svg>
                </button>
                <button class="toolbar-btn" @click="triggerFileUpload" title="上传文件 / 图片 (支持粘贴)" :disabled="uploading">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="17 8 12 3 7 8"></polyline>
                        <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                </button>
                <span v-if="articleId" class="toolbar-divider"></span>
                <button
                    v-if="articleId && isPublished"
                    class="toolbar-btn"
                    @click="unpublishArticle"
                    title="转为草稿"
                    :disabled="saving"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                        <polyline points="17 21 17 13 7 13 7 21"></polyline>
                        <polyline points="7 3 7 8 15 8"></polyline>
                    </svg>
                </button>
                <button
                    v-if="articleId"
                    class="toolbar-btn toolbar-btn-pin"
                    :class="{ active: isPinned }"
                    @click.stop="togglePin"
                    :title="isPinned ? '取消置顶' : '置顶'"
                    :disabled="pinning"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" :fill="isPinned ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5">
                        <path d="M16 12V4h1V2H7v2h1v8l-2 2v2h5v6l1 1 1-1v-6h5v-2l-2-2z"></path>
                    </svg>
                </button>
                <button
                    v-if="articleId"
                    class="toolbar-btn toolbar-btn-danger"
                    @click.stop="deleteArticle"
                    title="删除"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
                <button
                    v-if="!isPublished"
                    class="toolbar-btn toolbar-btn-publish"
                    @click="publishArticle"
                    :disabled="publishing"
                    title="发布 (Ctrl+S 保存)"
                >
                    <svg v-if="!publishing" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                    <span v-else class="toolbar-btn-loading"></span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { articleApi } from '@/api'
import { uploadApi, formatFileSize } from '@/api/upload'
import { resolveMarkdownHtml } from '@/utils/resolveMarkdownHtml'
import { parseMarkdown } from '@/utils/editorMarkdown'
import { insertBlock, MD_SNIPPETS, TABLE_3X3, LIST_BULLET_3, LIST_ORDERED_3, LIST_TASK_3, LIST_CURSOR_OFFSET } from '@/utils/markdownInsert'
import { routeTitleParam, toArticleRoute, toTopicRoute, isNewArticleRoute } from '@/utils/articleRoute'
import { clearLocalDraft, readLocalDraft, writeLocalDraft } from '@/utils/editorDraft'
import {
    clearEditorState,
    notifySidebarRefresh,
    syncEditorState,
} from '@/utils/articleEditorState'
import { clearArticleView, resetArticleHeadings, syncArticleHeadings, setActiveHeading } from '@/utils/articleViewState'
import { scrollToArticleHeading } from '@/utils/articleTocNav'
import { authState, isAuthenticated } from '@/utils/authSession'
import { buildUploadMarkdown, UPLOAD_ACCEPT } from '@/utils/uploadMarkdown'
import { enhanceMarkdownVideos } from '@/utils/enhanceMarkdownVideos'
import { classifyLoadError } from '@/utils/apiError'
import SkeletonArticleDetail from '@/components/state/SkeletonArticleDetail.vue'
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'

export default {
    name: 'PostView',
    components: { SkeletonArticleDetail, EmptyState, ErrorState },
    data() {
        return {
            uploadAccept: UPLOAD_ACCEPT,
            article: null,
            loading: false,
            loadError: null,
            articleId: null,
            title: '',
            topic: '',
            rawContent: '',
            activeEditField: null,
            bodyEditMode: true,
            lastKnownUpdatedAt: null,
            saveTimer: null,
            saveStatus: 'saved',
            saving: false,
            publishing: false,
            pinning: false,
            uploading: false,
            uploadFileName: '',
            uploadProgress: 0,
            uploadBytesLoaded: 0,
            uploadBytesTotal: 0,
            uploadPhase: 'idle',
            draftCreatedAt: null,
            saveSavedFlash: false,
            saveSavedFlashTimer: null,
            _routeLoadSeq: 0,
            _autoSaveSeq: 0,
            _loadedRouteTitle: '',
        }
    },
    computed: {
        isNewArticle() {
            return isNewArticleRoute(this.$route)
        },
        isLoggedIn() {
            void authState.token
            return isAuthenticated()
        },
        isEditablePage() {
            if (this.isNewArticle) return this.isLoggedIn
            return this.isLoggedIn && this.$route.name === 'public-article' && !!this.article
        },
        showBottomBar() {
            return this.isEditablePage
        },
        showArticleDetailLoading() {
            return this.$route.name === 'public-article' && this.loading
        },
        isPublished() {
            return this.article?.is_published ?? false
        },
        isPinned() {
            return this.article?.is_pinned ?? false
        },
        emptyContentHtml() {
            return '<p class="detail-content-empty">暂无正文</p>'
        },
        showSaveStatus() {
            return this.saveStatus !== 'saved' || this.saveSavedFlash
        },
        saveStatusDisplay() {
            if (this.saveStatus === 'saving') return 'saving'
            if (this.saveStatus === 'unsaved') return 'unsaved'
            if (this.saveSavedFlash) return 'saved'
            return 'saved'
        },
        saveStatusLabel() {
            if (this.saveStatus === 'saving') return '保存中'
            if (this.saveStatus === 'unsaved') return '待保存'
            if (this.saveSavedFlash) return '已保存'
            return ''
        },
        uploadIndeterminate() {
            return this.uploadPhase === 'uploading' && this.uploadProgress < 0
        },
        uploadStatusMeta() {
            if (this.uploadPhase === 'processing') return '处理中…'
            if (this.uploadBytesTotal > 0) {
                const size = `${formatFileSize(this.uploadBytesLoaded)} / ${formatFileSize(this.uploadBytesTotal)}`
                if (this.uploadProgress >= 0) return `${this.uploadProgress}% · ${size}`
                return size
            }
            if (this.uploadProgress >= 0) return `${this.uploadProgress}%`
            return '上传中…'
        },
        renderedContent() {
            if (!this.article || !this.articleMatchesRoute) return ''
            if (!this.article.content) return ''
            return resolveMarkdownHtml(this.renderMarkdown(this.article.content))
        },
        renderedHtml() {
            if (!this.rawContent.trim()) return ''
            return resolveMarkdownHtml(this.renderMarkdown(this.rawContent))
        },
        routeArticleTitle() {
            return routeTitleParam(this.$route)
        },
        articleMatchesRoute() {
            if (this.$route.name !== 'public-article') return true
            if (!this.article) return false
            const routeTitle = this.routeArticleTitle
            return this.article.title === routeTitle || this._loadedRouteTitle === routeTitle
        },
    },
    beforeRouteLeave(to, from, next) {
        if (!this.isEditablePage) {
            next()
            return
        }
        this.flushPendingSaveAsync().finally(() => next())
    },
    beforeRouteUpdate(to, from, next) {
        if (to.name === 'public-article' && from.name === 'public-article') {
            const toTitle = routeTitleParam(to)
            const fromTitle = routeTitleParam(from)
            if (toTitle && toTitle !== fromTitle) {
                this.flushPendingSaveAsync().finally(() => {
                    next()
                    this.loadArticleForRoute(toTitle)
                })
                return
            }
        }
        next()
    },
    async mounted() {
        this._onResize = () => {
            if (this.isEditablePage && this.bodyEditMode) this.syncTextareaHeight()
        }
        window.addEventListener('resize', this._onResize)
        this._onArticleFieldUpdated = (e) => {
            const { id, is_pinned: isPinned } = e.detail || {}
            if (this.articleId !== id || isPinned === undefined) return
            if (this.article) {
                this.article = { ...this.article, is_pinned: isPinned }
            }
        }
        window.addEventListener('article-field-updated', this._onArticleFieldUpdated)
        this._onTocNavigate = (e) => this.onTocNavigate(e.detail?.id)
        window.addEventListener('article-toc-navigate', this._onTocNavigate)
        this._onBeforeUnload = (e) => {
            if (this.isEditablePage && (this.saveStatus === 'unsaved' || this.saving)) {
                writeLocalDraft({
                    title: this.title,
                    content: this.rawContent,
                    topic: this.topic,
                })
                e.preventDefault()
                e.returnValue = ''
            }
        }
        window.addEventListener('beforeunload', this._onBeforeUnload)
        await this.initFromRoute()
        this.$nextTick(() => {
            this.updateTitleDisplay()
            if (this.isEditablePage && this.bodyEditMode) this.syncTextareaHeight()
            this.enhanceVideos()
        })
    },
    beforeUnmount() {
        window.removeEventListener('resize', this._onResize)
        window.removeEventListener('article-field-updated', this._onArticleFieldUpdated)
        window.removeEventListener('article-toc-navigate', this._onTocNavigate)
        window.removeEventListener('beforeunload', this._onBeforeUnload)
        if (this.saveTimer) clearTimeout(this.saveTimer)
        this.clearSaveSavedFlash()
        clearEditorState()
    },
    watch: {
        '$route'(to, from) {
            if (from?.name === 'public-article' && to.name !== 'public-article') {
                clearArticleView()
                this._loadedRouteTitle = ''
            }
            if (isNewArticleRoute(to) && to.query.fresh && to.query.fresh !== from?.query?.fresh) {
                if (from?.name === 'public-article' && this.articleId) {
                    this.captureActiveFieldValues()
                    this.prepareLeaveArticle()
                }
                this.resetNewArticle()
                return
            }
            if (to.name === 'public-article' && from?.name === 'public-article') {
                return
            }
            this.initFromRoute()
        },
        bodyEditMode(val) {
            if (val) this.syncTextareaHeight()
            this.$nextTick(this.enhanceVideos)
            if (!val) {
                this.$nextTick(() => {
                    window.dispatchEvent(new CustomEvent('article-toc-rebind'))
                })
            }
        },
        activeEditField(val, oldVal) {
            if (oldVal === 'title') this.updateTitleDisplay()
        },
        title() {
            this.syncEditorStateToSidebar()
            this.updateTitleDisplay()
        },
        saveStatus() {
            this.syncEditorStateToSidebar()
        },
        articleId() {
            this.syncEditorStateToSidebar()
        },
        isEditablePage(val) {
            if (val) {
                this.syncEditorStateToSidebar()
                this.$nextTick(() => {
                    if (this.bodyEditMode) this.syncTextareaHeight()
                })
            } else {
                clearEditorState()
            }
        },
        'article.is_published'() {
            this.syncEditorStateToSidebar()
        },
        'article.is_pinned'() {
            this.syncEditorStateToSidebar()
        },
        renderedContent() {
            this.$nextTick(this.enhanceVideos)
        },
        renderedHtml() {
            this.$nextTick(this.enhanceVideos)
        },
        rawContent() {
            this.syncArticleViewFromPost()
        },
    },
    methods: {
        toTopicRoute,
        enhanceVideos() {
            enhanceMarkdownVideos(this.$refs.detailWrapper)
        },
        getTextarea() {
            return this.$refs.textarea || null
        },
        buildSavePayload(extra = {}, options = {}) {
            const payload = {
                title: this.resolveSaveTitle(),
                content: this.rawContent,
                topic: this.topic.trim() || '',
                is_published: this.article?.is_published ?? false,
                is_pinned: this.article?.is_pinned ?? false,
                ...extra,
            }
            if (this.articleId && this.lastKnownUpdatedAt && !options.force) {
                payload.expected_updated_at = this.lastKnownUpdatedAt
            }
            return payload
        },
        resolveSaveTitle() {
            const trimmed = this.title.trim()
            if (trimmed) return trimmed
            if (this.isNewArticle && !this.articleId) {
                return this.generateDefaultTitle()
            }
            return '未命名'
        },
        generateDefaultTitle() {
            const now = new Date()
            const pad = (n) => String(n).padStart(2, '0')
            return `未命名 ${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`
        },
        applySaveResult(res, saveCtx = null) {
            if (!res) return
            if (saveCtx) {
                if (saveCtx.seq !== this._autoSaveSeq) return
                if (saveCtx.articleId && this.articleId !== saveCtx.articleId) return
                if (saveCtx.routeTitle !== routeTitleParam(this.$route)) return
            }
            this.article = res
            this.articleId = res.id
            if (res.updated_at) this.lastKnownUpdatedAt = res.updated_at
        },
        isSaveConflictError(err) {
            const msg = err?.message || ''
            return msg.includes('其他窗口') || msg.includes('其他标签')
        },
        handleSaveConflict(options, retryFn) {
            this.saving = false
            this.saveStatus = 'unsaved'
            const overwrite = confirm(
                '这篇文章已在其他标签页更新。\n\n确定 = 用当前内容覆盖\n取消 = 加载最新版本',
            )
            if (overwrite) {
                retryFn({ ...options, force: true })
            } else {
                this.reloadCurrentArticle()
            }
        },
        async reloadCurrentArticle() {
            const title = routeTitleParam(this.$route) || this.article?.title
            if (!title) return
            try {
                const data = await articleApi.getByTitle(title)
                this.article = data
                this.syncFormFromArticle(data)
                this.$toast.info('已加载最新版本')
            } catch (e) {
                console.error('Failed to reload article:', e)
                this.$toast.error('加载失败')
            }
        },
        onPreviewClick(e) {
            if (e.target.closest('a')) return
            this.enterBodyEdit()
        },
        onTextareaPaste(e) {
            const items = e.clipboardData?.items
            if (!items) return
            for (const item of items) {
                if (item.type.startsWith('image/')) {
                    e.preventDefault()
                    const file = item.getAsFile()
                    if (file) this.uploadFile(file)
                    return
                }
            }
        },
        renderMarkdown(content) {
            return parseMarkdown(content)
        },
        syncArticleViewFromPost() {
            if (this.$route.name !== 'public-article' || !this.article || !this.articleMatchesRoute) return
            const content = this.isLoggedIn ? this.rawContent : (this.article.content || '')
            syncArticleHeadings(content, this.article.title || this.title)
        },
        resetArticleLoadState() {
            this.article = null
            this.articleId = null
            this.title = ''
            this.topic = ''
            this.rawContent = ''
            this.lastKnownUpdatedAt = null
            this.loadError = null
            clearEditorState()
        },
        captureActiveFieldValues() {
            if (this.activeEditField !== 'title') return
            const el = this.$refs.titleEl
            if (!el) return
            const text = el.textContent.replace(/\n/g, '').slice(0, 200)
            this.title = text
        },
        prepareLeaveArticle() {
            return this.flushPendingSaveAsync()
        },
        syncEditorStateToSidebar() {
            if (!this.isEditablePage) {
                clearEditorState()
                return
            }
            syncEditorState({
                inEditor: true,
                articleId: this.articleId,
                title: this.title,
                isPublished: this.isPublished,
                isPinned: this.isPinned,
                saveStatus: this.saveStatus,
                createdAt: this.article?.created_at || this.draftCreatedAt || new Date().toISOString(),
            })
        },
        resetNewArticle() {
            this.flushPendingSave()
            this._autoSaveSeq += 1
            this._loadedRouteTitle = ''
            clearLocalDraft()
            this.activeEditField = null
            this.bodyEditMode = true
            this.articleId = null
            this.article = null
            this.lastKnownUpdatedAt = null
            this.title = ''
            this.topic = ''
            this.rawContent = ''
            this.saveStatus = 'saved'
            this.saving = false
            this.draftCreatedAt = new Date().toISOString()
            this.syncEditorStateToSidebar()
            this.$nextTick(() => {
                this.updateTitleDisplay()
                this.syncTextareaHeight()
            })
        },
        async initFromRoute() {
            if (this.isNewArticle) {
                this.activeEditField = null

                if (this.$route.query.fresh) {
                    this.resetNewArticle()
                    return
                }
                this.bodyEditMode = true
                if (!this.articleId) {
                    this.loadDraft()
                    if (!this.draftCreatedAt) {
                        this.draftCreatedAt = new Date().toISOString()
                    }
                }
                this.syncEditorStateToSidebar()
                this.$nextTick(() => {
                    this.updateTitleDisplay()
                    this.syncTextareaHeight()
                })
                return
            }

            if (this.$route.name !== 'public-article') return

            const title = routeTitleParam(this.$route)
            await this.loadArticleForRoute(title)
        },
        async loadArticleForRoute(title) {
            if (!title) {
                this.loadError = 'notfound'
                this.loading = false
                this._loadedRouteTitle = ''
                clearArticleView()
                return
            }

            if (!this.loading && this._loadedRouteTitle === title && this.article) {
                return
            }

            this.captureActiveFieldValues()
            this.activeEditField = null

            const loadSeq = ++this._routeLoadSeq

            resetArticleHeadings()
            this.resetArticleLoadState()
            this.bodyEditMode = false
            this.loading = true
            this.loadError = null

            try {
                const data = await articleApi.getByTitle(title)
                if (loadSeq !== this._routeLoadSeq) return
                if (routeTitleParam(this.$route) !== title) return

                this.article = data
                this._loadedRouteTitle = title
                if (this.isLoggedIn) {
                    this.syncFormFromArticle(data)
                }
                this.syncArticleViewFromPost()
            } catch (e) {
                if (loadSeq !== this._routeLoadSeq) return
                console.error('Failed to fetch article:', e)
                this.article = null
                this._loadedRouteTitle = ''
                this.loadError = classifyLoadError(e)
                clearArticleView()
            } finally {
                if (loadSeq === this._routeLoadSeq) {
                    this.loading = false
                    if (this.isEditablePage) {
                        this.syncEditorStateToSidebar()
                        this.$nextTick(() => {
                            this.updateTitleDisplay()
                            if (this.bodyEditMode) this.syncTextareaHeight()
                            this.enhanceVideos()
                        })
                    }
                }
            }
        },
        syncFormFromArticle(data) {
            this.articleId = data.id
            this.title = data.title || ''
            this.topic = data.topic || ''
            this.rawContent = data.content || ''
            this.lastKnownUpdatedAt = data.updated_at || null
            this.saveStatus = 'saved'
            this.draftCreatedAt = data.created_at || null
            this.$nextTick(() => {
                this.updateTitleDisplay()
                this.syncTextareaHeight()
            })
        },
        retryLoadArticle() {
            this._loadedRouteTitle = ''
            this.initFromRoute()
        },
        loadDraft() {
            if (this.articleId) return
            const draft = readLocalDraft()
            if (draft) {
                this.title = draft.title
                this.topic = draft.topic
                this.rawContent = draft.content
                if (draft.savedAt) {
                    this.draftCreatedAt = new Date(draft.savedAt).toISOString()
                }
                return
            }
            this.rawContent = ''
        },
        clearDraft() {
            clearLocalDraft()
        },
        syncRouteAfterTitleChange(newTitle) {
            const current = routeTitleParam(this.$route)
            if (!newTitle || newTitle === current) return
            this.$router.replace(toArticleRoute(newTitle))
        },
        async deleteArticle() {
            if (!this.articleId || !confirm('确定要删除这篇文章吗？')) return
            try {
                await articleApi.delete(this.articleId)
                notifySidebarRefresh()
                this.$toast.success('已删除')
                this.$router.push({ name: 'portal-home' })
            } catch (e) {
                console.error('Failed to delete article:', e)
                this.$toast.error('删除失败: ' + (e.message || '未知错误'))
            }
        },
        enterEdit(field) {
            this.activeEditField = field
            this.$nextTick(() => {
                if (field === 'title') this.focusTitleEditor()
                else if (field === 'topic') this.$refs.topicInput?.focus()
            })
        },
        flushActiveFields() {
            this.flushPendingSave()
            if (!this.activeEditField) return
            this.activeEditField = null
            this.updateTitleDisplay()
        },
        flushPendingSave() {
            if (this.saveTimer) {
                clearTimeout(this.saveTimer)
                this.saveTimer = null
            }
        },
        async flushPendingSaveAsync() {
            this.flushPendingSave()
            this.captureActiveFieldValues()
            this.activeEditField = null
            if (!this.isEditablePage) return null
            if (!this.title.trim() && !this.rawContent.trim()) return null
            return this.persistArticle({ silent: true })
        },
        onTocNavigate(id) {
            if (!id || !this.isEditablePage) return
            const scroll = () => {
                if (scrollToArticleHeading(id)) {
                    setActiveHeading(id)
                    window.dispatchEvent(new CustomEvent('article-toc-rebind'))
                }
            }
            if (this.bodyEditMode) {
                this.bodyEditMode = false
                this.$nextTick(() => {
                    this.enhanceVideos()
                    this.$nextTick(scroll)
                })
                return
            }
            scroll()
        },
        clearSaveSavedFlash() {
            if (this.saveSavedFlashTimer) {
                clearTimeout(this.saveSavedFlashTimer)
                this.saveSavedFlashTimer = null
            }
            this.saveSavedFlash = false
        },
        flashSaveSaved() {
            this.clearSaveSavedFlash()
            this.saveSavedFlash = true
            this.saveSavedFlashTimer = setTimeout(() => {
                this.saveSavedFlash = false
                this.saveSavedFlashTimer = null
            }, 1500)
        },
        updateTitleDisplay() {
            if (this.activeEditField === 'title') return
            const el = this.$refs.titleEl
            if (!el) return
            el.textContent = this.title.trim() || '请输入标题'
        },
        onTitleClick() {
            if (this.activeEditField !== 'title') this.enterEdit('title')
        },
        onTopicClick() {
            if (this.activeEditField !== 'topic') this.enterEdit('topic')
        },
        focusTitleEditor() {
            const el = this.$refs.titleEl
            if (!el) return
            el.textContent = this.title
            el.focus()
            const range = document.createRange()
            range.selectNodeContents(el)
            range.collapse(false)
            const sel = window.getSelection()
            sel?.removeAllRanges()
            sel?.addRange(range)
        },
        onTitleEditableInput(e) {
            const el = e.target
            const text = el.textContent.replace(/\n/g, '')
            if (text !== el.textContent) {
                el.textContent = text
                this.focusTitleEditor()
            }
            if (text.length > 200) {
                el.textContent = text.slice(0, 200)
                this.focusTitleEditor()
            }
            this.title = el.textContent
            this.onTitleInput()
        },
        onTitlePaste(e) {
            e.preventDefault()
            const text = e.clipboardData.getData('text/plain').replace(/\n/g, '').slice(0, 200)
            document.execCommand('insertText', false, text)
        },
        onTitleEnter(e) {
            e.target.blur()
        },
        togglePreview() {
            if (this.bodyEditMode) {
                this.enterPreview()
            } else {
                this.enterBodyEdit()
            }
        },
        enterPreview() {
            this.flushActiveFields()
            this.flushPendingSave()
            this.syncPreviewScrollFromEditor()
            this.bodyEditMode = false
            this.autoSave()
        },
        enterBodyEdit() {
            this.bodyEditMode = true
            this.$nextTick(() => {
                this.syncTextareaHeight()
                this.$refs.textarea?.focus()
            })
        },
        syncPreviewScrollFromEditor() {
            const ta = this.getTextarea()
            const wrapper = this.$refs.detailWrapper
            if (!ta || !wrapper || ta.scrollHeight <= 0) return

            const scale = wrapper.scrollHeight / ta.scrollHeight
            const maxWrapperScroll = Math.max(0, wrapper.scrollHeight - wrapper.clientHeight)
            wrapper.scrollTop = Math.min(maxWrapperScroll, Math.max(0, ta.scrollTop * scale))
        },
        leaveEdit(field) {
            if (this.activeEditField !== field) return
            this.flushPendingSave()
            this.activeEditField = null
            if (field === 'title') this.updateTitleDisplay()
            this.autoSave()
        },
        ensureBodyEdit() {
            if (!this.bodyEditMode) {
                this.bodyEditMode = true
            }
            return new Promise(resolve => {
                this.$nextTick(() => {
                    this.syncTextareaHeight()
                    this.$refs.textarea?.focus()
                    resolve()
                })
            })
        },
        onTitleInput() {
            this.clearSaveSavedFlash()
            this.saveStatus = 'unsaved'
            this.scheduleSave()
        },
        onContentInput() {
            this.clearSaveSavedFlash()
            this.saveStatus = 'unsaved'
            this.syncTextareaHeight()
            this.scheduleSave()
        },
        syncTextareaHeight(done) {
            this.$nextTick(() => {
                requestAnimationFrame(() => {
                    const ta = this.getTextarea()
                    const toolbar = this.$el?.querySelector('.editor-toolbar')
                    if (!ta || !toolbar) {
                        done?.()
                        return
                    }

                    const toolbarTop = toolbar.getBoundingClientRect().top
                    const taTop = ta.getBoundingClientRect().top
                    const minH = Math.max(240, toolbarTop - taTop - 16)

                    ta.style.minHeight = `${minH}px`
                    ta.style.height = 'auto'
                    ta.style.height = `${Math.max(minH, ta.scrollHeight)}px`
                    done?.()
                })
            })
        },
        onTextareaKeydown(e) {
            if ((e.metaKey || e.ctrlKey) && e.key === 's') {
                e.preventDefault()
                this.autoSave({ notify: true })
            }
            if (e.key === 'Tab') {
                e.preventDefault()
                const ta = this.getTextarea()
                if (!ta) return
                const start = ta.selectionStart
                const end = ta.selectionEnd
                const val = ta.value
                ta.value = val.substring(0, start) + '    ' + val.substring(end)
                ta.selectionStart = ta.selectionEnd = start + 4
                this.rawContent = ta.value
                this.onContentInput()
            }
        },
        async insertCodeBlock() {
            await this.ensureBodyEdit()
            const ta = this.getTextarea()
            if (!ta) return
            this.rawContent = insertBlock(ta, MD_SNIPPETS.codeBlock, 4)
            this.onContentInput()
        },
        async insertTable() {
            await this.ensureBodyEdit()
            const ta = this.getTextarea()
            if (!ta) return
            this.rawContent = insertBlock(ta, TABLE_3X3)
            this.onContentInput()
        },
        async insertBulletList() {
            await this.ensureBodyEdit()
            const ta = this.getTextarea()
            if (!ta) return
            this.rawContent = insertBlock(ta, LIST_BULLET_3, LIST_CURSOR_OFFSET.bullet)
            this.onContentInput()
        },
        async insertOrderedList() {
            await this.ensureBodyEdit()
            const ta = this.getTextarea()
            if (!ta) return
            this.rawContent = insertBlock(ta, LIST_ORDERED_3, LIST_CURSOR_OFFSET.ordered)
            this.onContentInput()
        },
        async insertTaskList() {
            await this.ensureBodyEdit()
            const ta = this.getTextarea()
            if (!ta) return
            this.rawContent = insertBlock(ta, LIST_TASK_3, LIST_CURSOR_OFFSET.task)
            this.onContentInput()
        },
        async triggerFileUpload() {
            await this.ensureBodyEdit()
            this.$refs.fileInput?.click()
        },
        async uploadFile(file) {
            this.uploading = true
            this.uploadFileName = file.name || '文件'
            this.uploadProgress = 0
            this.uploadBytesLoaded = 0
            this.uploadBytesTotal = file.size || 0
            this.uploadPhase = 'uploading'
            try {
                await this.ensureBodyEdit()
                const res = await uploadApi.uploadWithProgress(file, ({ loaded, total, percent }) => {
                    this.uploadBytesLoaded = loaded
                    if (total > 0) this.uploadBytesTotal = total
                    this.uploadProgress = percent
                })
                this.uploadPhase = 'processing'
                this.uploadProgress = 100
                const ta = this.getTextarea()
                if (!ta) return
                const md = buildUploadMarkdown(res, file.name)
                this.rawContent = insertBlock(ta, md)
                this.onContentInput()
                this.$toast.success('上传成功')
            } catch (err) {
                this.$toast.error('上传失败: ' + (err.message || '未知错误'))
            } finally {
                this.uploading = false
                this.uploadFileName = ''
                this.uploadProgress = 0
                this.uploadBytesLoaded = 0
                this.uploadBytesTotal = 0
                this.uploadPhase = 'idle'
            }
        },
        async onFileSelected(e) {
            const file = e.target.files?.[0]
            e.target.value = ''
            if (!file) return
            await this.uploadFile(file)
        },
        scheduleSave() {
            this.clearSaveSavedFlash()
            if (this.saveTimer) clearTimeout(this.saveTimer)
            this.saveTimer = setTimeout(() => this.autoSave(), 800)
        },
        persistArticle(options = {}) {
            if (!this.title.trim() && !this.rawContent.trim()) {
                return Promise.resolve(null)
            }

            const saveCtx = {
                seq: ++this._autoSaveSeq,
                articleId: this.articleId,
                routeTitle: routeTitleParam(this.$route),
            }

            this.saving = true
            this.saveStatus = 'saving'

            writeLocalDraft({
                title: this.title,
                content: this.rawContent,
                topic: this.topic,
            })

            const payload = this.buildSavePayload({}, options)

            const done = (res) => {
                if (saveCtx.seq !== this._autoSaveSeq) return res
                if (saveCtx.articleId && this.articleId !== saveCtx.articleId) return res
                if (saveCtx.routeTitle !== routeTitleParam(this.$route)) return res

                const wasCreate = !saveCtx.articleId && !!res?.id
                this.applySaveResult(res, saveCtx)
                this.saving = false
                this.saveStatus = 'saved'
                this.syncEditorStateToSidebar()
                notifySidebarRefresh()
                if (wasCreate) {
                    clearLocalDraft()
                }
                if (wasCreate && res?.title) {
                    if (this.isNewArticle) {
                        this.$router.replace(toArticleRoute(res.title))
                    } else {
                        this.syncRouteAfterTitleChange(res.title)
                    }
                }
                if (options.notify) {
                    this.$toast.success('已保存')
                } else if (!options.silent) {
                    this.flashSaveSaved()
                }
                return res
            }
            const fail = (err) => {
                if (saveCtx.seq !== this._autoSaveSeq) throw err
                if (this.isSaveConflictError(err)) {
                    this.handleSaveConflict(options, (next) => this.autoSave(next))
                    throw err
                }
                this.saving = false
                this.saveStatus = 'unsaved'
                if (options.notify) {
                    this.$toast.error('保存失败')
                } else if (!options.silent) {
                    this.$toast.error('自动保存失败')
                }
                throw err
            }

            if (this.articleId) {
                return articleApi.update(this.articleId, payload)
                    .then((res) => {
                        if (saveCtx.seq !== this._autoSaveSeq) return res
                        if (saveCtx.routeTitle !== routeTitleParam(this.$route)) return res
                        return done(res)
                    })
                    .catch(fail)
            }

            return articleApi.create(payload)
                .then((res) => {
                    if (saveCtx.seq !== this._autoSaveSeq) return res
                    if (saveCtx.routeTitle !== routeTitleParam(this.$route)) return res
                    return done(res)
                })
                .catch(fail)
        },
        autoSave(options = {}) {
            this.persistArticle(options).catch(() => {})
        },
        async publishArticle(options = {}) {
            if (!this.title.trim()) {
                this.$toast.info('请输入标题')
                this.enterEdit('title')
                return
            }
            if (!this.rawContent.trim()) {
                this.$toast.info('请输入正文内容')
                this.enterBodyEdit()
                return
            }
            this.flushActiveFields()
            if (!this.bodyEditMode) this.enterBodyEdit()
            this.publishing = true
            this.saveStatus = 'saving'
            const payload = this.buildSavePayload({ is_published: true }, options)
            try {
                let res
                if (this.articleId) {
                    res = await articleApi.update(this.articleId, payload)
                } else {
                    res = await articleApi.create(payload)
                }
                this.clearDraft()
                this.applySaveResult(res)
                this.saveStatus = 'saved'
                this.syncEditorStateToSidebar()
                notifySidebarRefresh()
                const publishedTitle = res.title || this.title.trim()
                if (this.$route.name !== 'public-article') {
                    this.$router.replace(toArticleRoute(publishedTitle))
                } else if (publishedTitle !== routeTitleParam(this.$route)) {
                    this.$router.replace(toArticleRoute(publishedTitle))
                }
                this.$toast.success('发布成功')
            } catch (e) {
                if (this.isSaveConflictError(e)) {
                    this.handleSaveConflict(options, (next) => this.publishArticle(next))
                    return
                }
                this.saveStatus = 'unsaved'
                this.$toast.error('发布失败: ' + (e.message || '未知错误'))
            } finally {
                this.publishing = false
            }
        },
        async unpublishArticle(options = {}) {
            if (!this.articleId) return
            this.saving = true
            this.saveStatus = 'saving'
            const payload = this.buildSavePayload({ is_published: false }, options)
            try {
                const res = await articleApi.update(this.articleId, payload)
                this.applySaveResult(res)
                this.saveStatus = 'saved'
                this.syncEditorStateToSidebar()
                notifySidebarRefresh()
                this.$toast.success('已转为草稿')
            } catch (e) {
                if (this.isSaveConflictError(e)) {
                    this.handleSaveConflict(options, (next) => this.unpublishArticle(next))
                    return
                }
                this.saveStatus = 'unsaved'
                this.$toast.error('操作失败: ' + (e.message || '未知错误'))
            } finally {
                this.saving = false
            }
        },
        async togglePin(options = {}) {
            if (!this.articleId) return
            this.pinning = true
            const next = !this.isPinned
            const payload = this.buildSavePayload({ is_pinned: next }, options)
            try {
                const res = await articleApi.update(this.articleId, payload)
                this.applySaveResult(res)
                this.syncEditorStateToSidebar()
                notifySidebarRefresh()
                this.$toast.success(next ? '已置顶' : '已取消置顶')
            } catch (e) {
                if (this.isSaveConflictError(e)) {
                    this.handleSaveConflict(options, (nextOpts) => this.togglePin(nextOpts))
                    return
                }
                this.$toast.error('操作失败: ' + (e.message || '未知错误'))
            } finally {
                this.pinning = false
            }
        },
    },
}
</script>

<style scoped>
.post-view {
    width: 100%;
    min-height: 100%;
}

.post-view--editing {
    position: relative;
    height: 100%;
    overflow: hidden;
}

.hidden-input {
    display: none;
}

.detail-wrapper {
    position: relative;
    width: 100%;
    min-height: 100%;
}

.post-view--editing .detail-wrapper {
    height: 100%;
    min-height: 0;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 80px;
    box-sizing: border-box;
}

.detail-header {
    margin-bottom: 28px;
}

.detail-title {
    font-size: 32px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 4px;
    letter-spacing: -0.02em;
    line-height: 1.3;
}

.detail-title.detail-editable {
    padding: 4px 8px;
    margin: 0 -8px;
    min-height: 44px;
    box-sizing: border-box;
}

.detail-subtitle.detail-editable {
    display: block;
    width: 100%;
    padding: 4px 8px;
    margin: 0 -8px;
    min-height: 32px;
    box-sizing: border-box;
}

.detail-title[contenteditable="true"] {
    outline: none;
    cursor: text;
}

.detail-title[contenteditable="true"]:empty::before {
    content: attr(data-placeholder);
    color: var(--text-tertiary);
    font-weight: 600;
}

.detail-editable {
    cursor: text;
}

.detail-title.is-placeholder {
    color: var(--text-tertiary);
    font-weight: 600;
}

.detail-topic-placeholder {
    color: var(--text-tertiary);
}

.detail-topic-edit {
    display: inline-flex;
    align-items: center;
    gap: 0;
}

.detail-topic-hash {
    color: var(--text-secondary);
    font-weight: 500;
    font-size: inherit;
    line-height: inherit;
    user-select: none;
}

.detail-content :deep(.detail-content-empty) {
    color: var(--text-tertiary);
    font-size: 16px;
    line-height: 1.85;
}

.detail-content-preview {
    cursor: default;
}

.detail-content-preview--clickable {
    cursor: default;
}

.detail-subtitle {
    font-size: 14px;
    color: var(--text-tertiary);
    margin: 0;
    letter-spacing: 1px;
}

.detail-topic-field {
    border: none;
    outline: none;
    background: transparent;
    padding: 0;
    margin: 0;
    font-size: inherit;
    font-family: inherit;
    color: var(--primary);
    font-weight: 500;
    letter-spacing: 1px;
    min-width: 6em;
    width: auto;
    field-sizing: content;
}

.detail-topic-field::placeholder {
    color: var(--text-tertiary);
    font-weight: 400;
}

.detail-topic-tag {
    color: var(--text-secondary);
    font-weight: 500;
    text-decoration: none;
    transition: color 0.15s;
}

a.detail-topic-tag:hover {
    color: var(--primary);
}

.detail-body-edit {
    width: 100%;
}

.detail-editor-textarea {
    width: 100%;
    display: block;
    border: none;
    outline: none;
    resize: none;
    padding: 0;
    margin: 0;
    background: transparent;
    tab-size: 4;
    box-sizing: border-box;
    overflow: hidden;
    font: inherit;
    color: inherit;
    letter-spacing: inherit;
    word-break: break-word;
    caret-color: var(--text-primary);
}

.detail-editor-textarea::placeholder {
    color: var(--text-tertiary);
    font-weight: 400;
}

.detail-loading,
.detail-error {
    padding: 60px 48px;
    text-align: center;
    color: var(--text-tertiary);
    font-size: 15px;
}

.detail-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.error-icon {
    color: var(--text-tertiary);
    opacity: 0.4;
    margin-bottom: 4px;
}

.error-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-secondary);
}

.error-desc {
    font-size: 14px;
    color: var(--text-tertiary);
    opacity: 0.7;
}

.editor-toolbar {
    position: absolute;
    left: 50%;
    bottom: 16px;
    transform: translateX(-50%);
    z-index: 20;
    max-width: calc(100% - 32px);
}

.save-status {
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 15;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    pointer-events: none;
    user-select: none;
}

.upload-status {
    position: absolute;
    top: 12px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 16;
    width: min(420px, calc(100% - 32px));
    padding: 10px 12px;
    border-radius: 8px;
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    pointer-events: none;
    user-select: none;
}

.upload-status-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
    min-width: 0;
}

.upload-status-name {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
}

.upload-status-meta {
    flex-shrink: 0;
    font-size: 12px;
    color: var(--text-secondary);
    font-variant-numeric: tabular-nums;
}

.upload-status-track {
    height: 4px;
    border-radius: 999px;
    background: var(--bg-hover);
    overflow: hidden;
}

.upload-status-bar {
    height: 100%;
    border-radius: inherit;
    background: var(--primary);
    transition: width 0.15s ease;
}

.upload-status-track.is-indeterminate .upload-status-bar {
    width: 35% !important;
    animation: upload-indeterminate 1.2s ease-in-out infinite;
}

@keyframes upload-indeterminate {
    0% { transform: translateX(-120%); }
    100% { transform: translateX(320%); }
}

.save-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

.save-status-text {
    font-size: 12px;
    line-height: 1;
    color: var(--text-tertiary);
}

.save-status.is-unsaved .save-status-dot {
    background: #ef4444;
}

.save-status.is-unsaved .save-status-text {
    color: #dc2626;
}

.save-status.is-saving .save-status-dot {
    background: #9ca3af;
    animation: status-pulse 1.2s ease-in-out infinite;
}

.save-status.is-saving .save-status-text {
    color: var(--text-secondary);
}

.save-status.is-saved .save-status-dot {
    background: #22c55e;
}

.save-status.is-saved .save-status-text {
    color: #16a34a;
}

@keyframes status-pulse {
    0%, 100% { opacity: 0.35; transform: scale(0.9); }
    50% { opacity: 1; transform: scale(1); }
}

.editor-toolbar-pill {
    display: flex;
    align-items: center;
    gap: 2px;
    padding: 4px 6px;
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    box-shadow: var(--shadow-sm);
}

.toolbar-divider {
    width: 1px;
    height: 16px;
    margin: 0 2px;
    background: var(--border-color);
    flex-shrink: 0;
}

.toolbar-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--icon-color);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    padding: 0;
    font-family: inherit;
    flex-shrink: 0;
}

.toolbar-btn:hover:not(:disabled) {
    background: var(--bg-hover);
    color: var(--text-secondary);
}

.toolbar-btn.active {
    color: var(--primary);
    background: var(--primary-light);
}

.toolbar-btn:disabled {
    opacity: 0.35;
    cursor: not-allowed;
}

.toolbar-btn-publish {
    color: var(--primary);
}

.toolbar-btn-publish:hover:not(:disabled) {
    background: var(--primary-light);
    color: var(--primary);
}

.toolbar-btn-pin.active,
.toolbar-btn-pin:hover:not(:disabled) {
    color: var(--primary);
    background: var(--primary-light);
}

.toolbar-btn-danger:hover:not(:disabled) {
    background: #fef2f2;
    color: #dc2626;
}

.toolbar-btn-loading {
    width: 12px;
    height: 12px;
    border: 2px solid var(--border-color);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
    .detail-header {
        margin-bottom: 20px;
    }

    .detail-title {
        font-size: 22px;
    }

    .detail-title.detail-editable,
    .detail-subtitle.detail-editable {
        margin-left: -4px;
        margin-right: -4px;
        padding-left: 4px;
        padding-right: 4px;
    }

    .detail-content :deep(.detail-content-empty) {
        font-size: 15px;
    }

    .detail-loading,
    .detail-error {
        padding: 24px 0;
    }

    .post-view--editing .detail-wrapper {
        padding-bottom: calc(64px + env(safe-area-inset-bottom, 0px));
    }

    .save-status {
        top: 8px;
        right: 8px;
    }

    .upload-status {
        top: 8px;
        width: calc(100% - 16px);
        padding: 8px 10px;
    }

    .editor-toolbar {
        bottom: calc(10px + env(safe-area-inset-bottom, 0px));
        max-width: calc(100% - 16px);
    }

    .editor-toolbar-pill {
        padding: 3px 4px;
        gap: 1px;
        border-radius: 8px;
        max-width: 100%;
        overflow-x: auto;
        overflow-y: hidden;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }

    .editor-toolbar-pill::-webkit-scrollbar {
        display: none;
    }

    .toolbar-divider {
        height: 14px;
    }

    .toolbar-btn {
        width: 28px;
        height: 28px;
        border-radius: 6px;
        flex-shrink: 0;
    }

    .toolbar-btn svg {
        width: 14px;
        height: 14px;
    }

    .toolbar-btn-loading {
        width: 10px;
        height: 10px;
    }

    .detail-editor-textarea {
        font-size: 16px;
    }
}
</style>
