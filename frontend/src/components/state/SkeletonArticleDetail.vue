<template>
    <div class="skeleton-article-detail">
        <SkeletonBlock width="65%" height="28px" radius="8px" />
        <SkeletonBlock width="80px" height="22px" radius="6px" />
        <div class="skeleton-body">
            <SkeletonBlock width="100%" height="14px" />
            <SkeletonBlock width="96%" height="14px" />
            <SkeletonBlock width="92%" height="14px" />
            <SkeletonBlock width="88%" height="14px" />
            <SkeletonBlock width="72%" height="14px" />
            <SkeletonBlock class="skeleton-media" width="58%" height="160px" radius="8px" />
            <SkeletonBlock width="100%" height="14px" />
            <SkeletonBlock width="94%" height="14px" />
            <SkeletonBlock width="86%" height="14px" />
            <SkeletonBlock width="78%" height="14px" />
            <SkeletonBlock width="64%" height="14px" />
        </div>
    </div>
</template>

<script>
import SkeletonBlock from './SkeletonBlock.vue'

export default {
    name: 'SkeletonArticleDetail',
    components: { SkeletonBlock },
}
</script>

<style scoped>
.skeleton-article-detail {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.skeleton-body {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 12px;
}

.skeleton-media {
    margin: 6px 0 4px;
}
</style>
