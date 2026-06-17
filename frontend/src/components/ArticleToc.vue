<template>
    <div class="article-toc">
        <div v-if="displayHeadings.length" class="article-toc-head" aria-hidden="true">
            <span class="article-toc-head-bar"></span>
            <span class="article-toc-head-rule"></span>
        </div>
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
                <span v-if="h.level === 1" class="article-toc-level1-bar" aria-hidden="true"></span>
                <span v-else class="article-toc-rail" :class="`rail-${h.level}`" aria-hidden="true">
                    <span class="article-toc-rail-stem"></span>
                    <span class="article-toc-rail-node"></span>
                </span>
                <span class="article-toc-text">{{ h.text }}</span>
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

.article-toc-head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px 12px;
    flex-shrink: 0;
}

.article-toc-head-bar {
    flex-shrink: 0;
    width: 3px;
    height: 14px;
    border-radius: 999px;
    background: linear-gradient(180deg, var(--primary) 0%, rgba(79, 110, 247, 0.35) 100%);
    opacity: 0.55;
}

.article-toc-head-rule {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-color) 0%, transparent 100%);
}

.article-toc-nav {
    flex: 1;
    overflow-y: auto;
    padding: 0 10px 8px;
    scrollbar-width: none;
}

.article-toc-nav::-webkit-scrollbar {
    display: none;
}

.article-toc-item {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    text-align: left;
    border: none;
    background: transparent;
    color: var(--toc-item-color);
    line-height: 1.45;
    cursor: pointer;
    font-family: inherit;
    transition: color 0.18s ease, background 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.article-toc-text {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 一级：章节块 */
.article-toc-item.level-1 {
    margin-top: 10px;
    padding: 10px 12px;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    border-radius: 8px;
    border: 1px solid transparent;
}

.article-toc-item.level-1:first-child {
    margin-top: 0;
}

.article-toc-level1-bar {
    flex-shrink: 0;
    width: 3px;
    height: 16px;
    border-radius: 999px;
    background: linear-gradient(180deg, var(--primary) 0%, rgba(79, 110, 247, 0.35) 100%);
    opacity: 0.55;
    transition: opacity 0.18s ease, height 0.18s ease;
}

.article-toc-item.level-1:hover:not(.active),
.article-toc-item.level-1.active {
    background: var(--toc-hover-bg);
    border-color: var(--border-subtle);
    color: var(--text-primary);
}

.article-toc-item.level-1:hover:not(.active) .article-toc-level1-bar,
.article-toc-item.level-1.active .article-toc-level1-bar {
    opacity: 0.85;
}

.article-toc-item.level-1.active {
    font-weight: 600;
}

.article-toc-item.level-1.active .article-toc-level1-bar {
    height: 16px;
}

/* 二三级：树形导轨 */
.article-toc-rail {
    position: relative;
    flex-shrink: 0;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.article-toc-rail-stem {
    position: absolute;
    left: 8px;
    top: -10px;
    bottom: 50%;
    width: 1px;
    background: linear-gradient(180deg, transparent 0%, var(--border-color) 28%, var(--border-color) 100%);
    opacity: 0.9;
}

.article-toc-rail-node {
    position: relative;
    z-index: 1;
    transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.rail-2 .article-toc-rail-node {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    border: 1.5px solid var(--text-tertiary);
    background: var(--bg-white);
    transform: rotate(45deg);
}

.rail-3 .article-toc-rail-stem {
    left: 9px;
}

.rail-3 .article-toc-rail-node {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-tertiary);
    box-shadow: 0 0 0 3px var(--bg-white);
}

.article-toc-item.level-2 {
    margin-top: 2px;
    padding: 8px 10px 8px 6px;
    font-size: 13.5px;
    font-weight: 400;
    color: var(--text-secondary);
    border-radius: 7px;
}

.article-toc-item.level-3 {
    margin-top: 1px;
    padding: 7px 10px 7px 20px;
    font-size: 13px;
    font-weight: 400;
    color: var(--text-secondary);
    border-radius: 6px;
}

.article-toc-item.level-2:hover:not(.active),
.article-toc-item.level-3:hover:not(.active) {
    color: var(--text-primary);
    background: var(--toc-hover-bg);
}

.article-toc-item.level-2:hover:not(.active) .article-toc-rail-node {
    border-color: var(--primary);
    background: var(--primary-light);
}

.article-toc-item.level-3:hover:not(.active) .article-toc-rail-node {
    background: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
}

.article-toc-item.level-2.active,
.article-toc-item.level-3.active {
    color: var(--text-primary);
    font-weight: 500;
    background: var(--toc-hover-bg);
}

.article-toc-item.level-2.active .article-toc-rail-node {
    border-color: var(--text-secondary);
    background: var(--bg-white);
    box-shadow: none;
}

.article-toc-item.level-3.active .article-toc-rail-node {
    background: var(--text-secondary);
    box-shadow: 0 0 0 3px var(--bg-white);
}

.article-toc-empty {
    margin: 0;
    padding: 14px 16px;
    font-size: 13px;
    color: var(--text-tertiary);
    line-height: 1.5;
}
</style>
