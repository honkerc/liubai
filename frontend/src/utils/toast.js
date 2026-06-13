import { reactive } from 'vue'

let toastId = 0

export const toastState = reactive({
    toasts: [],
})

function remove(id) {
    const idx = toastState.toasts.findIndex(t => t.id === id)
    if (idx !== -1) toastState.toasts.splice(idx, 1)
}

function show(message, type = 'info', duration = 2600) {
    if (!message) return
    const id = ++toastId
    toastState.toasts.push({ id, message, type })
    setTimeout(() => remove(id), duration)
}

export const toast = {
    show,
    success(message, duration) {
        show(message, 'success', duration)
    },
    error(message, duration) {
        show(message, 'error', duration)
    },
    info(message, duration) {
        show(message, 'info', duration)
    },
}

export function installToast(app) {
    app.config.globalProperties.$toast = toast
}
