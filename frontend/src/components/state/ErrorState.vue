<template>
    <div class="page-state error-state" :class="{ compact, 'align-left': align === 'left' }">
        <div v-if="!compact" class="page-state-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
        </div>
        <p class="page-state-title">{{ title }}</p>
        <p v-if="description" class="page-state-desc">{{ description }}</p>
        <div class="page-state-action">
            <button type="button" class="retry-btn" @click="$emit('retry')">重试</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ErrorState',
    emits: ['retry'],
    props: {
        title: { type: String, default: '加载失败' },
        description: { type: String, default: '请检查网络连接后重试' },
        compact: { type: Boolean, default: false },
        align: { type: String, default: 'center', validator: v => ['center', 'left'].includes(v) },
    },
}
</script>

<style scoped>
.page-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 40px 16px;
    color: var(--text-tertiary);
}

.page-state.align-left {
    align-items: flex-start;
    text-align: left;
}

.page-state.compact {
    padding: 24px 12px;
}

.page-state-icon {
    color: var(--text-tertiary);
    opacity: 0.35;
    margin-bottom: 12px;
}

.page-state.compact .page-state-icon {
    display: none;
}

.page-state-title {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-secondary);
    margin: 0 0 4px;
}

.page-state.compact .page-state-title {
    font-size: 13px;
    font-weight: 400;
}

.page-state-desc {
    font-size: 13px;
    color: var(--text-tertiary);
    margin: 0;
    line-height: 1.5;
}

.page-state-action {
    margin-top: 16px;
}

.retry-btn {
    padding: 6px 14px;
    font-size: 13px;
    font-family: inherit;
    color: var(--primary);
    background: var(--primary-light);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: opacity 0.15s;
}

.retry-btn:hover {
    opacity: 0.85;
}
</style>
