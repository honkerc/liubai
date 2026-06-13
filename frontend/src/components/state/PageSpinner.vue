<template>
    <div class="page-spinner" :class="{ inline: inline, sm: size === 'sm' }">
        <span class="page-spinner-ring"></span>
        <span v-if="label" class="page-spinner-label">{{ label }}</span>
    </div>
</template>

<script>
export default {
    name: 'PageSpinner',
    props: {
        label: { type: String, default: '' },
        inline: { type: Boolean, default: false },
        size: { type: String, default: 'md', validator: v => ['sm', 'md'].includes(v) },
    },
}
</script>

<style scoped>
.page-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 32px 16px;
    color: var(--text-tertiary);
}

.page-spinner.inline {
    flex-direction: row;
    padding: 16px;
}

.page-spinner-ring {
    width: 24px;
    height: 24px;
    border: 2px solid var(--border-color);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
}

.page-spinner.sm .page-spinner-ring {
    width: 16px;
    height: 16px;
}

.page-spinner-label {
    font-size: 14px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
