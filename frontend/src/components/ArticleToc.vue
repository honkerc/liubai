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
    padding: 4px 0 8px;
}

.article-toc-nav {
    flex: 1;
    overflow-y: auto;
    padding: 2px 10px 6px;
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
    font-size: 14px;
    line-height: 1.35;
    padding: 5px 8px;
    margin: 1px 0;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    transition: color 0.15s, background 0.15s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.article-toc-item:hover {
    color: var(--text-primary);
}

.article-toc-item.active {
    color: var(--primary);
    background: var(--primary-light);
    font-weight: 500;
}

.article-toc-item.level-1 {
    font-weight: 500;
    color: var(--text-primary);
}

.article-toc-item.level-2 {
    padding-left: 20px;
    font-size: 13px;
    font-weight: 400;
    color: var(--text-tertiary);
}

.article-toc-item.level-2:hover {
    color: var(--text-secondary);
}

.article-toc-item.level-2.active {
    color: var(--primary);
}

.article-toc-item.level-3 {
    padding-left: 32px;
    font-size: 13px;
    font-weight: 400;
    color: var(--text-tertiary);
}

.article-toc-empty {
    margin: 0;
    padding: 12px 16px;
    font-size: 13px;
    color: var(--text-tertiary);
    line-height: 1.5;
}
</style>
