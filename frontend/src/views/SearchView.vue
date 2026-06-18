<template>
    <div class="search-page page">
        <form class="page-search" @submit.prevent="handleSearch">
            <svg class="page-search__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input
                ref="searchInput"
                v-model="keyword"
                type="text"
                placeholder="搜索文章…"
                class="page-search__input"
                autocomplete="off"
                @keyup.enter="handleSearch"
            />
        </form>

        <p v-if="searched && !loading && !error && keyword.trim()" class="search-meta">
            <template v-if="results.length">
                {{ resultCount }} 篇结果<template v-if="hasMore">（仅显示前 {{ results.length }} 篇）</template>
            </template>
            <template v-else>
                无结果
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
            title="未找到相关文章"
            :show-icon="false"
        />
    </div>
</template>

<script>
import { articleApi, normalizeListResponse } from '@/api'
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
            hasMore: false,
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
        async handleSearch(updateQuery = true) {
            const q = this.keyword.trim()
            if (!q) {
                this.results = []
                this.searched = false
                if (this.$route.query.q) {
                    this.$router.replace({ name: 'search' })
                }
                return
            }
            if (updateQuery && this.$route.query.q !== q) {
                this.$router.replace({ name: 'search', query: { q } })
            }
            this.loading = true
            this.searched = true
            this.error = false
            try {
                const data = await articleApi.list({ search: q, page_size: 100 })
                const { items, has_more } = normalizeListResponse(data)
                this.results = items
                this.hasMore = has_more
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
            const raw = item.snippet || buildSearchSnippet(item.content, this.keyword)
            if (!raw) return ''
            return highlightKeyword(raw, this.keyword)
        },
    },
}
</script>

<style scoped>
.search-meta {
    margin: -8px 0 16px;
    font-size: 13px;
    color: var(--text-tertiary);
}

.search-results {
    display: flex;
    flex-direction: column;
}

.search-results :deep(.article-list-item__desc) {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    white-space: normal;
}
</style>
