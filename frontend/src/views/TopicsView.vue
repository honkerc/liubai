<template>
    <div class="topics-page page">
        <div class="main-header">
            <h1 class="page-title">话题</h1>
            <p class="page-desc">按话题浏览文章</p>
        </div>

        <SkeletonTopicGrid v-if="loading" />
        <ErrorState v-else-if="error" @retry="loadTopics" />
        <div v-else-if="topics.length" class="topics-grid">
            <router-link
                v-for="item in topics"
                :key="item.name"
                :to="toTopicRoute(item.name)"
                class="topic-card"
            >
                <span class="topic-name">{{ item.name }}</span>
                <span class="topic-count">{{ item.count }} 篇</span>
            </router-link>
        </div>
        <EmptyState
            v-else
            title="暂无话题"
            description="为文章添加话题后，会出现在这里"
            :show-icon="false"
        />
    </div>
</template>

<script>
import { articleApi } from '@/api'
import { toTopicRoute } from '@/utils/articleRoute'
import SkeletonTopicGrid from '@/components/state/SkeletonTopicGrid.vue'
import EmptyState from '@/components/state/EmptyState.vue'
import ErrorState from '@/components/state/ErrorState.vue'

export default {
    name: 'TopicsView',
    components: { SkeletonTopicGrid, EmptyState, ErrorState },
    data() {
        return {
            topics: [],
            loading: true,
            error: false,
        }
    },
    mounted() {
        this.loadTopics()
    },
    methods: {
        toTopicRoute,
        async loadTopics() {
            this.loading = true
            this.error = false
            try {
                const topicData = await articleApi.topics()
                this.topics = (topicData || [])
                    .map((item) => ({
                        name: item.name,
                        count: item.count ?? 0,
                    }))
                    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, 'zh-CN'))
            } catch (e) {
                console.error('Failed to load topics:', e)
                this.topics = []
                this.error = true
            } finally {
                this.loading = false
            }
        },
    },
}
</script>

<style scoped>
.topics-page {
    max-width: 720px;
}

.main-header {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
}

.page-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 4px;
}

.page-desc {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

.topics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
}

.topic-card {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-white);
    text-decoration: none;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.topic-card:hover {
    border-color: var(--primary);
    box-shadow: 0 2px 8px rgba(79, 110, 247, 0.08);
}

.topic-name {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
}

.topic-count {
    font-size: 13px;
    color: var(--text-tertiary);
}
</style>
