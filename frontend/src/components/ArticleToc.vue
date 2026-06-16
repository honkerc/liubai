<template>
    <div class="article-toc">
        <div class="article-toc-head">
            <button type="button" class="article-toc-back" @click="$emit('back')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
                全部文章
            </button>
            <p v-if="title" class="article-toc-title" :title="title">{{ title }}</p>
        </div>
        <nav v-if="headings.length" class="article-toc-nav" aria-label="文章目录">
            <button
                v-for="h in headings"
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
        <p v-else class="article-toc-empty">暂无目录（使用 # 标题生成）</p>
    </div>
</template>

<script>
export default {
    name: 'ArticleToc',
    props: {
        title: { type: String, default: '' },
        headings: { type: Array, default: () => [] },
        activeId: { type: String, default: '' },
    },
    emits: ['back', 'select'],
}
</script>

<style scoped>
.article-toc {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
}

.article-toc-head {
    padding: 4px 8px 8px 12px;
    flex-shrink: 0;
}

.article-toc-back {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    padding: 4px 6px;
    margin: 0 0 6px -6px;
    border-radius: 4px;
    font-family: inherit;
}

.article-toc-back:hover {
    background: var(--toc-hover-bg);
    color: var(--toc-item-hover-color);
}

.article-toc-title {
    margin: 0;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.article-toc-nav {
    flex: 1;
    overflow-y: auto;
    padding: 0 8px 8px 4px;
    scrollbar-width: thin;
}

.article-toc-item {
    display: block;
    width: 100%;
    text-align: left;
    border: none;
    background: transparent;
    color: var(--toc-item-color);
    font-size: 13px;
    line-height: 1.45;
    padding: 5px 8px;
    margin: 1px 0;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s, color 0.15s;
}

.article-toc-item:hover {
    background: var(--toc-hover-bg);
    color: var(--toc-item-hover-color);
}

.article-toc-item.active {
    background: rgb(231 237 253);
    color: var(--primary);
    font-weight: 500;
}

.article-toc-item.level-1 { padding-left: 8px; font-weight: 600; }
.article-toc-item.level-2 { padding-left: 16px; }
.article-toc-item.level-3 { padding-left: 24px; font-size: 12px; }
.article-toc-item.level-4 { padding-left: 32px; font-size: 12px; }
.article-toc-item.level-5 { padding-left: 40px; font-size: 12px; }
.article-toc-item.level-6 { padding-left: 48px; font-size: 12px; }

.article-toc-empty {
    margin: 0;
    padding: 12px 16px;
    font-size: 13px;
    color: var(--text-tertiary);
}
</style>
