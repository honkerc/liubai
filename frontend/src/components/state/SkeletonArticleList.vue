<template>
    <div class="skeleton-article-list" :class="{ compact, numbered }">
        <div v-for="i in count" :key="i" class="skeleton-article-item">
            <SkeletonBlock v-if="numbered" width="18px" height="14px" />
            <SkeletonBlock width="55%" height="15px" />
            <SkeletonBlock width="72px" height="12px" />
        </div>
    </div>
</template>

<script>
import SkeletonBlock from './SkeletonBlock.vue'

export default {
    name: 'SkeletonArticleList',
    components: { SkeletonBlock },
    props: {
        count: { type: Number, default: 5 },
        compact: { type: Boolean, default: false },
        numbered: { type: Boolean, default: false },
    },
}
</script>

<style scoped>
.skeleton-article-list {
    display: flex;
    flex-direction: column;
}

.skeleton-article-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
}

.skeleton-article-item :deep(.skeleton-block:last-child) {
    margin-left: auto;
}

.skeleton-article-list.compact .skeleton-article-item {
    padding: 10px 0;
    gap: 10px;
}
</style>
