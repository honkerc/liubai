<template>
    <div class="search-page page">
        <PageListHeader>
            <template v-if="searched && keyword.trim()">
                搜索到 <em>{{ resultCount }}</em> 篇与
                <span class="page-list-kw">{{ keyword.trim() }}</span>
                的结果
            </template>
            <template v-else>
                搜索站内文章
            </template>
        </PageListHeader>

        <form class="page-search" @submit.prevent="handleSearch">
            <svg class="page-search__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input
                type="text"
                v-model="keyword"
                placeholder="输入关键词搜索…"
                class="page-search__input"
                ref="searchInput"
                @keyup.enter="handleSearch"
            />
        </form>

        <EmptyState
            v-if="!searched && !loading"
            title="输入关键词开始搜索"
            description="支持按标题和正文搜索"
            :show-icon="false"
        />

        <SkeletonArticleList v-else-if="loading" :count="4" numbered />

        <ErrorState
            v-else-if="error"
            @retry="handleSearch(false)"
        />

        <div class="article-list" v-else-if="results.length > 0">
            <ArticleListItem
                v-for="(item, idx) in results"
                :key="item.id"
                :index="idx + 1"
                :desc="itemSnippet(item)"
                :date="formatDate(item.created_at)"
                @click="goArticle(item)"
            >
                <span v-html="highlightTitle(item.title)"></span>
            </ArticleListItem>
        </div>

        <EmptyState
            v-else-if="searched"
            title="未找到相关文章"
            description="试试其他关键词"
            :show-icon="false"
        />
    </div>
</template>

<script>
import { articleApi } from '@/api'
import { toArticleRoute } from '@/utils/articleRoute'
import { highlightKeyword, buildSearchSnippet } from '@/utils/searchHighlight'
import PageListHeader from '@/components/PageListHeader.vue'
import ArticleListItem from '@/components/ArticleListItem.vue'
import SkeletonArticleList from '@/components/state/SkeletonArticleList.vue'
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'

export default {
    components: { PageListHeader, ArticleListItem, SkeletonArticleList, EmptyState, ErrorState },
    data() {
        return {
            keyword: '',
            results: [],
            loading: false,
            searched: false,
            error: false,
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
            if (val && val !== this.keyword) {
                this.keyword = val
                this.handleSearch(false)
            }
        },
    },
    methods: {
        async handleSearch(updateQuery = true) {
            if (!this.keyword.trim()) {
                this.$toast.info('请输入搜索关键词')
                return
            }
            if (updateQuery) {
                this.$router.replace({ name: 'search', query: { q: this.keyword.trim() } })
            }
            this.loading = true
            this.searched = true
            this.error = false
            try {
                const data = await articleApi.list({ search: this.keyword.trim() })
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
.article-list {
    display: flex;
    flex-direction: column;
}
</style>
