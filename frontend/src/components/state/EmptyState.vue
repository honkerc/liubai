<template>
    <div class="page-state empty-state" :class="{ compact, 'align-left': align === 'left' }">
        <div v-if="!compact && showIcon" class="page-state-icon">
            <slot name="icon">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
            </slot>
        </div>
        <p class="page-state-title">{{ title }}</p>
        <p v-if="description" class="page-state-desc">{{ description }}</p>
        <div v-if="$slots.default" class="page-state-action">
            <slot />
        </div>
    </div>
</template>

<script>
export default {
    name: 'EmptyState',
    props: {
        title: { type: String, required: true },
        description: { type: String, default: '' },
        compact: { type: Boolean, default: false },
        showIcon: { type: Boolean, default: true },
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
    color: var(--text-tertiary);
}

.page-state-desc {
    font-size: 13px;
    color: var(--text-tertiary);
    margin: 0;
    line-height: 1.5;
    max-width: 320px;
}

.page-state-action {
    margin-top: 16px;
}

.page-state-action :deep(a),
.page-state-action :deep(button) {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    font-size: 13px;
    font-family: inherit;
    color: var(--primary);
    background: var(--primary-light);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    transition: opacity 0.15s;
}

.page-state-action :deep(a:hover),
.page-state-action :deep(button:hover) {
    opacity: 0.85;
}
</style>
