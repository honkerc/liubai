<template>
    <div class="portal-home page">
        <div class="main-header">
            <h1 class="main-title">首页</h1>
            <p class="main-desc">{{ siteTagline }}</p>
        </div>

        <section v-if="topics.length" class="portal-block">
            <div class="block-head">
                <h2 class="block-title">话题</h2>
                <router-link :to="{ name: 'topics' }" class="block-more">全部</router-link>
            </div>
            <div class="topic-tags">
                <router-link
                    v-for="item in topics.slice(0, 10)"
                    :key="item.name"
                    :to="toTopicRoute(item.name)"
                    class="topic-tag"
                >{{ item.name }}</router-link>
            </div>
        </section>

        <section class="portal-block">
            <h2 class="block-title">最近发布</h2>
            <SkeletonArticleList v-if="loading" :count="5" numbered />
            <ErrorState
                v-else-if="error"
                align="left"
                @retry="loadData"
            />
            <div v-else-if="articles.length" class="article-list">
                <ArticleListItem
                    v-for="(a, idx) in articles"
                    :key="a.id"
                    :index="idx + 1"
                    :title="a.title"
                    :date="formatDate(a.created_at)"
                    @click="goArticle(a)"
                />
            </div>
            <EmptyState
                v-else
                align="left"
                title="暂无已发布文章"
                description="发布第一篇文章后，会出现在这里"
            />
        </section>
    </div>
</template>

<script>
import { articleApi } from '@/api'
import { toArticleRoute, toTopicRoute } from '@/utils/articleRoute'
import { SITE_TAGLINE } from '@/constants/brand'
import ArticleListItem from '@/components/ArticleListItem.vue'
import SkeletonArticleList from '@/components/state/SkeletonArticleList.vue'
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'

export default {
    name: 'PortalHomeView',
    components: { ArticleListItem, SkeletonArticleList, EmptyState, ErrorState },
    data() {
        return {
            articles: [],
            topics: [],
            loading: true,
            error: false,
        }
    },
    mounted() {
        this.loadData()
    },
    computed: {
        siteTagline() {
            return SITE_TAGLINE
        },
    },
    methods: {
        toTopicRoute,
        async loadData() {
            this.loading = true
            this.error = false
            try {
                const [articles, topicNames] = await Promise.all([
                    articleApi.list({ page: 1, page_size: 12 }),
                    articleApi.topics(),
                ])
                this.articles = articles.items || articles
                this.topics = topicNames.map(name => ({ name }))
            } catch (e) {
                console.error('Failed to load portal home:', e)
                this.articles = []
                this.topics = []
                this.error = true
            } finally {
                this.loading = false
            }
        },
        goArticle(a) {
            this.$router.push(toArticleRoute(a.title))
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
.main-header {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
}

.main-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 4px;
}

.main-desc {
    font-size: 14px;
    color: var(--text-tertiary);
    margin: 0;
}

.portal-block {
    margin-bottom: 28px;
}

.block-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.block-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    margin: 0 0 12px;
}

.block-head .block-title {
    margin-bottom: 0;
}

.block-more {
    font-size: 13px;
    color: var(--text-tertiary);
    text-decoration: none;
}

.block-more:hover {
    color: var(--primary);
}

.topic-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.topic-tag {
    padding: 4px 10px;
    font-size: 13px;
    color: var(--primary);
    text-decoration: none;
    background: var(--primary-light);
    border-radius: 6px;
    transition: opacity 0.15s;
}

.topic-tag:hover {
    opacity: 0.85;
}

.article-list {
    display: flex;
    flex-direction: column;
}
</style>
