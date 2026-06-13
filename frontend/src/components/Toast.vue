<template>
    <div class="toast-container" aria-live="polite">
        <transition-group name="toast">
            <div
                v-for="item in toastState.toasts"
                :key="item.id"
                class="toast-item"
                :class="'toast-' + item.type"
            >
                <span class="toast-icon" :class="'toast-icon--' + item.type">
                    <svg v-if="item.type === 'success'" width="15" height="15" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"></circle>
                        <path d="M8 12.5l2.5 2.5L16 9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                    </svg>
                    <svg v-else-if="item.type === 'error'" width="15" height="15" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"></circle>
                        <path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"></path>
                    </svg>
                    <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"></circle>
                        <path d="M12 8v5M12 16h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"></path>
                    </svg>
                </span>
                <span class="toast-text">{{ item.message }}</span>
            </div>
        </transition-group>
    </div>
</template>

<script>
import { toastState } from '@/utils/toast'

export default {
    name: 'ToastNotification',
    data() {
        return { toastState }
    },
}
</script>

<style scoped>
.toast-container {
    position: fixed;
    top: calc(20px + env(safe-area-inset-top, 0px));
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    pointer-events: none;
    width: max-content;
    max-width: min(90vw, 400px);
}

.toast-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    border-radius: 6px;
    font-size: 13px;
    line-height: 20px;
    color: var(--text-primary);
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    pointer-events: auto;
    word-break: break-word;
}

.toast-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.toast-icon--success {
    color: #16a34a;
}

.toast-icon--error {
    color: #dc2626;
}

.toast-icon--info {
    color: var(--text-tertiary);
}

.toast-success {
    background: #f6fef9;
    border-color: #bbf7d0;
}

.toast-error {
    background: #fef2f2;
    border-color: #fecaca;
}

.toast-info {
    background: var(--bg-white);
}

.toast-text {
    flex: 1;
    min-width: 0;
}

.toast-enter-active {
    animation: toast-in 0.22s ease;
}

.toast-leave-active {
    animation: toast-out 0.16s ease forwards;
}

@keyframes toast-in {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes toast-out {
    from {
        opacity: 1;
        transform: translateY(0);
    }
    to {
        opacity: 0;
        transform: translateY(-6px);
    }
}

@media (max-width: 768px) {
    .toast-container {
        top: calc(14px + env(safe-area-inset-top, 0px));
        max-width: calc(100vw - 32px);
    }

    .toast-item {
        padding: 8px 12px;
        font-size: 13px;
    }
}

@media (prefers-color-scheme: dark) {
    .toast-success,
    .toast-error,
    .toast-info {
        background: var(--bg-white);
    }

    .toast-success {
        border-color: rgba(34, 197, 94, 0.35);
    }

    .toast-error {
        border-color: rgba(239, 68, 68, 0.35);
    }
}
</style>
