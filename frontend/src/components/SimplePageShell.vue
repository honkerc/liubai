<template>
    <div class="simple-page page">
        <header class="simple-page__head">
            <h1 class="simple-page__title">{{ title }}</h1>
            <p v-if="desc" class="simple-page__desc">{{ desc }}</p>
        </header>
        <div class="simple-page__body">
            <slot />
        </div>
    </div>
</template>

<script>
export default {
    name: 'SimplePageShell',
    props: {
        title: { type: String, required: true },
        desc: { type: String, default: '' },
    },
}
</script>

<style scoped>
.simple-page__head {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
}

.simple-page__title {
    margin: 0 0 4px;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.simple-page__desc {
    margin: 0;
    font-size: 14px;
    color: var(--text-tertiary);
}

.simple-page__body :deep(.simple-prose) {
    font-size: 15px;
    line-height: 1.85;
    color: var(--text-secondary);
}

.simple-page__body :deep(.simple-prose p) {
    margin: 0 0 14px;
}

.simple-page__body :deep(.simple-prose p:last-child) {
    margin-bottom: 0;
}

.simple-page__body :deep(.simple-prose strong) {
    color: var(--text-primary);
    font-weight: 600;
}

.simple-page__body :deep(.simple-prose ul) {
    margin: 0 0 14px;
    padding-left: 1.25em;
}

.simple-page__body :deep(.simple-prose li) {
    margin-bottom: 6px;
}

.simple-page__body :deep(.simple-link-list) {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.simple-page__body :deep(.simple-link-item) {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 14px;
    text-decoration: none;
    color: inherit;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    transition: border-color 0.15s, background 0.15s;
}

.simple-page__body :deep(.simple-link-item:hover) {
    border-color: rgba(79, 110, 247, 0.35);
    background: var(--bg-hover);
}

.simple-page__body :deep(.simple-link-item__label) {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.simple-page__body :deep(.simple-link-item__hint) {
    font-size: 12px;
    color: var(--text-tertiary);
    flex-shrink: 0;
}
</style>
