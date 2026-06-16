<template>
    <div class="article-toc">
        <nav v-if="displayHeadings.length" class="article-toc-nav" aria-label="文章目录">
            <button
                v-for="h in displayHeadings"
                :key="h.id + h.text"
                type="button"
                class="article-toc-item"
                :class="[
                    `level-${h.level}`,
                    { active: h.id === activeId },
                ]"
                @click="$emit('select', h.id)"
            >
                {{ h.text }}
            </button>
        </nav>
        <p v-else class="article-toc-empty">使用 # 标题生成目录</p>
    </div>
</template>

<script>
export default {
    name: 'ArticleToc',
    props: {
        headings: { type: Array, default: () => [] },
        activeId: { type: String, default: '' },
    },
    emits: ['select'],
    computed: {
        /** 仅展示一级、二级标题，保持目录简约 */
        displayHeadings() {
            const primary = this.headings.filter((h) => h.level <= 2)
            if (primary.length > 0) return primary
            return this.headings.filter((h) => h.level <= 3)
        },
    },
}
</script>

<style scoped>
.article-toc {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
    padding: 8px 0 12px;
}

.article-toc-nav {
    flex: 1;
    overflow-y: auto;
    padding: 4px 12px 8px 8px;
    scrollbar-width: none;
}

.article-toc-nav::-webkit-scrollbar {
    display: none;
}

.article-toc-item {
    display: block;
    width: 100%;
    text-align: left;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-size: 15px;
    line-height: 1.5;
    padding: 10px 12px 10px 14px;
    margin: 2px 0;
    border-radius: 6px;
    border-left: 3px solid transparent;
    cursor: pointer;
    font-family: inherit;
    transition: color 0.15s, border-color 0.15s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.article-toc-item:hover {
    color: var(--text-primary);
}

.article-toc-item.active {
    color: var(--text-primary);
    font-weight: 500;
    border-left-color: var(--primary);
}

.article-toc-item.level-1 {
    padding-left: 14px;
}

.article-toc-item.level-2 {
    padding-left: 26px;
    font-size: 14px;
}

.article-toc-item.level-3 {
    padding-left: 38px;
    font-size: 14px;
}

.article-toc-empty {
    margin: 0;
    padding: 16px 20px;
    font-size: 14px;
    color: var(--text-tertiary);
    line-height: 1.6;
}
</style>
