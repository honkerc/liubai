<template>
    <div class="skeleton-sidebar-list">
        <div v-for="i in count" :key="i" class="skeleton-sidebar-item">
            <span class="skeleton-dot skeleton-block"></span>
            <div class="skeleton-sidebar-text">
                <SkeletonBlock width="85%" height="13px" />
                <SkeletonBlock width="50%" height="11px" />
            </div>
        </div>
    </div>
</template>

<script>
import SkeletonBlock from './SkeletonBlock.vue'

export default {
    name: 'SkeletonSidebarList',
    components: { SkeletonBlock },
    props: {
        count: { type: Number, default: 5 },
    },
}
</script>

<style scoped>
.skeleton-sidebar-list {
    padding: 4px 0;
}

.skeleton-sidebar-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 10px 12px;
}

.skeleton-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 4px;
}

.skeleton-sidebar-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-width: 0;
}
</style>
