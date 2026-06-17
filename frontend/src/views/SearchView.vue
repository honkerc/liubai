<template>
    <div class="search-page page">
        <header class="search-page__head">
            <h1 class="search-page__title">搜索</h1>
            <p class="search-page__desc">按标题或正文搜索站内文章</p>
        </header>

        <form class="search-form" @submit.prevent="handleSearch">
            <div class="search-field">
                <svg class="search-field__icon" width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"
                    aria-hidden="true">
                    <circle cx="11" cy="11" r="7"></circle>
                    <path d="M20 20L16.5 16.5"></path>
                </svg>
                <input
                    ref="searchInput"
                    v-model="keyword"
                    type="search"
                    enterkeyhint="search"
                    placeholder="输入关键词…"
                    class="search-field__input"
                    autocomplete="off"
                    @keydown.esc.prevent="clearSearch"
                />
                <button
                    v-if="keyword"
                    type="button"
                    class="search-field__clear"
                    title="清空"
                    aria-label="清空"
                    @click="clearSearch"
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>
            <button type="submit" class="search-submit" :disabled="loading || !keyword.trim()">
                {{ loading ? '搜索中' : '搜索' }}
            </button>
        </form>

        <div v-if="!searched && !loading" class="search-hints">
            <span class="search-hints__label">试试</span>
            <button
                v-for="hint in searchHints"
                :key="hint"
                type="button"
                class="search-hints__item"
                @click="applyHint(hint)"
            >
                {{ hint }}
            </button>
        </div>

        <p v-if="searched && !loading && !error" class="search-meta">
            <template v-if="keyword.trim() && results.length">
                找到 <em>{{ resultCount }}</em> 篇与
                <span class="search-meta__kw">{{ keyword.trim() }}</span>
                相关的文章
            </template>
            <template v-else-if="keyword.trim()">
                未找到与
                <span class="search-meta__kw">{{ keyword.trim() }}</span>
                相关的文章
            </template>
        </p>

        <SkeletonArticleList v-if="loading" :count="4" numbered />

        <ErrorState v-else-if="error" @retry="handleSearch(false)" />

        <div v-else-if="results.length" class="search-results">
            <ArticleListItem
                v-for="(item, idx) in results"
                :key="item.id"
                :index="idx + 1"
                :topic="item.topic"
                :desc="itemSnippet(item)"
                :date="formatDate(item.created_at)"
                @click="goArticle(item)"
            >
                <span v-html="highlightTitle(item.title)"></span>
            </ArticleListItem>
        </div>

        <EmptyState
            v-else-if="searched"
            align="left"
            compact
            title="没有匹配的结果"
            description="换个关键词试试，或检查是否有拼写错误"
            :show-icon="false"
        />

        <EmptyState
            v-else
            align="left"
            compact
            title="输入关键词开始搜索"
            description="支持搜索文章标题与正文内容"
            :show-icon="false"
        />
    </div>
</template>

<script>
import { articleApi } from '@/api'
import { toArticleRoute } from '@/utils/articleRoute'
import { highlightKeyword, buildSearchSnippet } from '@/utils/searchHighlight'
import ArticleListItem from '@/components/ArticleListItem.vue'
import SkeletonArticleList from '@/components/state/SkeletonArticleList.vue'
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'

export default {
    components: { ArticleListItem, SkeletonArticleList, EmptyState, ErrorState },
    data() {
        return {
            keyword: '',
            results: [],
            loading: false,
            searched: false,
            error: false,
            searchHints: ['部署', 'Vue', 'Python', 'Markdown'],
        }
    },
    computed: {
        resultCount() {
            return this.results.length
        },
    },
    mounted() {
        const q = this.$route.query.q
        if (q) {
            this.keyword = q
            this.handleSearch(false)
        }
        this.$nextTick(() => {
            this.$refs.searchInput?.focus()
        })
    },
    watch: {
        '$route.query.q'(val) {
            if (!val) {
                this.keyword = ''
                this.results = []
                this.searched = false
                this.error = false
                return
            }
            if (val !== this.keyword) {
                this.keyword = val
                this.handleSearch(false)
            }
        },
    },
    methods: {
        applyHint(hint) {
            this.keyword = hint
            this.handleSearch()
        },
        clearSearch() {
            this.keyword = ''
            this.results = []
            this.searched = false
            this.error = false
            if (this.$route.query.q) {
                this.$router.replace({ name: 'search' })
            }
            this.$nextTick(() => {
                this.$refs.searchInput?.focus()
            })
        },
        async handleSearch(updateQuery = true) {
            const q = this.keyword.trim()
            if (!q) {
                this.$toast.info('请输入搜索关键词')
                return
            }
            if (updateQuery && this.$route.query.q !== q) {
                this.$router.replace({ name: 'search', query: { q } })
            }
            this.loading = true
            this.searched = true
            this.error = false
            try {
                const data = await articleApi.list({ search: q })
                this.results = data.items || data
            } catch (e) {
                console.error('Search failed:', e)
                this.results = []
                this.error = true
            } finally {
                this.loading = false
            }
        },
        goArticle(item) {
            this.$router.push(toArticleRoute(item.title))
        },
        formatDate(dateStr) {
            if (!dateStr) return ''
            const d = new Date(dateStr)
            const pad = (n) => String(n).padStart(2, '0')
            return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
        },
        highlightTitle(title) {
            return highlightKeyword(title, this.keyword)
        },
        itemSnippet(item) {
            const snippet = buildSearchSnippet(item.content, this.keyword)
            if (!snippet) return ''
            return highlightKeyword(snippet, this.keyword)
        },
    },
}
</script>

<style scoped>
.search-page__head {
    margin-bottom: 20px;
}

.search-page__title {
    margin: 0 0 4px;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.search-page__desc {
    margin: 0;
    font-size: 14px;
    color: var(--text-tertiary);
}

.search-form {
    display: flex;
    align-items: stretch;
    gap: 8px;
    margin-bottom: 16px;
}

.search-field {
    flex: 1;
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    height: 44px;
    padding: 0 12px 0 14px;
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.search-field:focus-within {
    border-color: rgba(79, 110, 247, 0.45);
    box-shadow: 0 0 0 3px var(--primary-light);
}

.search-field__icon {
    flex-shrink: 0;
    color: var(--text-tertiary);
}

.search-field__input {
    flex: 1;
    min-width: 0;
    border: none;
    outline: none;
    font-size: 15px;
    font-family: inherit;
    color: var(--text-primary);
    background: transparent;
}

.search-field__input::placeholder {
    color: var(--text-tertiary);
}

.search-field__input::-webkit-search-cancel-button {
    display: none;
}

.search-field__clear {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 26px;
    height: 26px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--text-tertiary);
    cursor: pointer;
    padding: 0;
    transition: color 0.15s, background 0.15s;
}

.search-field__clear:hover {
    color: var(--text-secondary);
    background: var(--bg-hover);
}

.search-submit {
    flex-shrink: 0;
    height: 44px;
    padding: 0 18px;
    border: none;
    border-radius: 10px;
    background: var(--primary);
    color: #fff;
    font-size: 14px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s, opacity 0.15s;
}

.search-submit:hover:not(:disabled) {
    background: var(--primary-hover);
}

.search-submit:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

.search-hints {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
}

.search-hints__label {
    font-size: 13px;
    color: var(--text-tertiary);
}

.search-hints__item {
    border: 1px solid var(--border-subtle);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 13px;
    font-family: inherit;
    color: var(--text-secondary);
    background: var(--bg-card);
    cursor: pointer;
    transition: color 0.15s, border-color 0.15s, background 0.15s;
}

.search-hints__item:hover {
    color: var(--primary);
    border-color: rgba(79, 110, 247, 0.25);
    background: var(--primary-light);
}

.search-meta {
    margin: 0 0 12px;
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.5;
}

.search-meta em {
    font-style: normal;
    font-weight: 600;
    color: var(--primary);
}

.search-meta__kw {
    font-weight: 500;
    color: var(--text-primary);
}

.search-results {
    display: flex;
    flex-direction: column;
}

.search-results :deep(.article-list-item__desc) {
    color: var(--text-secondary);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    white-space: normal;
}

.search-results :deep(.search-hl) {
    background: var(--primary-light);
    color: var(--primary);
    padding: 0 2px;
    border-radius: 3px;
    font-weight: 600;
}

@media (max-width: 768px) {
    .search-form {
        flex-direction: column;
    }

    .search-submit {
        width: 100%;
    }
}
</style>
