<template>
    <div class="skeleton-article-toc" aria-hidden="true">
        <div class="skeleton-article-toc-head">
            <span class="skeleton-block skeleton-article-toc-head-bar"></span>
            <SkeletonBlock width="100%" height="1px" radius="1px" />
        </div>
        <div class="skeleton-article-toc-nav">
            <div
                v-for="(item, i) in items"
                :key="i"
                class="skeleton-article-toc-item"
                :class="`level-${item.level}`"
            >
                <span
                    v-if="item.level === 1"
                    class="skeleton-block skeleton-article-toc-level1-bar"
                ></span>
                <span
                    v-else
                    class="skeleton-block"
                    :class="item.level === 2 ? 'skeleton-article-toc-node-2' : 'skeleton-article-toc-node-3'"
                ></span>
                <SkeletonBlock :width="item.width" height="13px" />
            </div>
        </div>
    </div>
</template>

<script>
import SkeletonBlock from './SkeletonBlock.vue'

export default {
    name: 'SkeletonArticleToc',
    components: { SkeletonBlock },
    data() {
        return {
            items: [
                { level: 1, width: '72%' },
                { level: 2, width: '58%' },
                { level: 2, width: '64%' },
                { level: 1, width: '68%' },
                { level: 3, width: '52%' },
                { level: 2, width: '60%' },
            ],
        }
    },
}
</script>

<style scoped>
.skeleton-article-toc {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
    padding: 8px 0 12px;
}

.skeleton-article-toc-head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px 12px;
    flex-shrink: 0;
}

.skeleton-article-toc-head-bar {
    width: 3px;
    height: 14px;
    border-radius: 999px;
    flex-shrink: 0;
}

.skeleton-article-toc-nav {
    flex: 1;
    padding: 0 10px 8px;
}

.skeleton-article-toc-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    margin-top: 4px;
}

.skeleton-article-toc-item.level-1 {
    margin-top: 10px;
    padding: 10px 12px;
}

.skeleton-article-toc-item.level-1:first-child {
    margin-top: 0;
}

.skeleton-article-toc-level1-bar {
    width: 3px;
    height: 16px;
    border-radius: 999px;
    flex-shrink: 0;
}

.skeleton-article-toc-item.level-2 {
    padding-left: 6px;
}

.skeleton-article-toc-item.level-3 {
    padding-left: 20px;
}

.skeleton-article-toc-node-2 {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    flex-shrink: 0;
    transform: rotate(45deg);
}

.skeleton-article-toc-node-3 {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}
</style>
