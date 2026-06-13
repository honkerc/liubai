<template>
    <div class="not-found-page page">
        <EmptyState
            title="页面不存在"
            description="你访问的页面可能已被移除，或链接有误"
        >
            <router-link :to="{ name: 'portal-home' }">返回首页</router-link>
            <router-link :to="{ name: 'search' }" class="secondary-link">去搜索</router-link>
        </EmptyState>
    </div>
</template>

<script>
import EmptyState from '@/components/state/EmptyState.vue'

export default {
    name: 'NotFoundView',
    components: { EmptyState },
}
</script>

<style scoped>
.not-found-page :deep(.page-state-action) {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
}

.not-found-page :deep(.secondary-link) {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
}
</style>
