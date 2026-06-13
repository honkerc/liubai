<template>
    <div class="topic-page page">
        <PageListHeader icon="tag" v-if="topicName">
            以下是
            <span class="page-list-kw">{{ topicName }}</span>
            相关的文章
            <span v-if="!loading && !error" class="page-list-muted">（共 <em class="page-list-num">{{ articles.length }}</em> 篇）</span>
        </PageListHeader>

        <EmptyState
            v-if="!topicName"
            title="话题不存在"
            description="请从话题列表选择一个有效话题"
            :show-icon="false"
        >
            <router-link :to="{ name: 'topics' }">浏览话题</router-link>
        </EmptyState>

        <template v-else>
            <SkeletonArticleList v-if="loading" :count="4" numbered />
            <ErrorState v-else-if="error" @retry="loadArticles" />
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
                title="该话题下暂无文章"
                :description="`「${topicName}」下还没有发布文章`"
                :show-icon="false"
            />
        </template>
    </div>
</template>

<script>
import { articleApi } from '@/api'
import { routeTopicParam, toArticleRoute } from '@/utils/articleRoute'
import PageListHeader from '@/components/PageListHeader.vue'
import ArticleListItem from '@/components/ArticleListItem.vue'
import SkeletonArticleList from '@/components/state/SkeletonArticleList.vue'
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'

export default {
    name: 'TopicView',
    components: { PageListHeader, ArticleListItem, SkeletonArticleList, EmptyState, ErrorState },
    data() {
        return {
            articles: [],
            loading: true,
            error: false,
        }
    },
    computed: {
        topicName() {
            return routeTopicParam(this.$route)
        },
    },
    watch: {
        '$route.params.topic'() {
            this.loadArticles()
        },
    },
    mounted() {
        this.loadArticles()
    },
    methods: {
        async loadArticles() {
            const topic = this.topicName
            if (!topic) {
                this.articles = []
                this.loading = false
                this.error = false
                return
            }
            this.loading = true
            this.error = false
            try {
                const data = await articleApi.list({ topic, page: 1, page_size: 50 })
                this.articles = data.items || data
            } catch (e) {
                console.error('Failed to load topic articles:', e)
                this.articles = []
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
.article-list {
    display: flex;
    flex-direction: column;
}
</style>
