<template>
    <div class="article-list-item" @click="$emit('click')">
        <span v-if="index != null" class="article-list-item__index">{{ index }}</span>
        <div class="article-list-item__main">
            <div class="article-list-item__row">
                <div class="article-list-item__title">
                    <slot>{{ title }}</slot>
                </div>
                <span v-if="topic" class="article-list-item__topic">#{{ topic }}</span>
                <time v-if="date" class="article-list-item__date">{{ date }}</time>
            </div>
            <div v-if="desc" class="article-list-item__desc" v-html="desc"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ArticleListItem',
    props: {
        title: { type: String, default: '' },
        date: { type: String, default: '' },
        desc: { type: String, default: '' },
        index: { type: [Number, String], default: null },
        topic: { type: String, default: '' },
    },
    emits: ['click'],
}
</script>

<style scoped>
.article-list-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
    cursor: pointer;
    transition: background-color 0.15s;
}

.article-list-item:hover {
    background-color: var(--bg-hover);
    margin: 0 -12px;
    padding: 12px;
    border-radius: 6px;
}

.article-list-item__index {
    flex-shrink: 0;
    width: 22px;
    margin-top: 1px;
    font-size: 14px;
    font-weight: 600;
    color: var(--primary);
    text-align: center;
    line-height: 1.5;
}

.article-list-item__main {
    flex: 1;
    min-width: 0;
}

.article-list-item__row {
    display: flex;
    align-items: center;
    gap: 16px;
}

.article-list-item__title {
    flex: 1;
    min-width: 0;
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
    line-height: 1.5;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.article-list-item__topic {
    flex-shrink: 0;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 12px;
    color: var(--text-tertiary);
}

.article-list-item__desc {
    margin-top: 4px;
    font-size: 13px;
    line-height: 1.6;
    color: var(--text-tertiary);
    white-space: pre-wrap;
    word-break: break-word;
}

.article-list-item__date {
    flex-shrink: 0;
    font-size: 13px;
    color: var(--text-tertiary);
    white-space: nowrap;
}
</style>
