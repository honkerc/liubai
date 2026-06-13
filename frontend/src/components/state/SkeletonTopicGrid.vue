<template>
    <div class="skeleton-topic-grid">
        <div v-for="i in count" :key="i" class="skeleton-topic-card skeleton-block"></div>
    </div>
</template>

<script>
export default {
    name: 'SkeletonTopicGrid',
    props: {
        count: { type: Number, default: 8 },
    },
}
</script>

<style scoped>
.skeleton-topic-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 8px;
}

.skeleton-topic-card {
    height: 44px;
    border-radius: 8px;
}
</style>
