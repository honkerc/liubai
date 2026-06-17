<template>
    <div class="app-layout" :class="{ 'sidebar-open': sidebarOpen }">
        <div
            v-if="isMobile && sidebarOpen"
            class="layout-sidebar-backdrop"
            @click="closeSidebar"
        ></div>

        <AppSidebar
            ref="sidebar"
            :open="!isMobile || sidebarOpen"
            @close="closeSidebar"
            @login-required="showLogin = true"
        />

        <main class="layout-right">
            <header v-if="isMobile" class="layout-mobile-bar">
                <button class="layout-mobile-menu" type="button" title="文章列表" @click="toggleSidebar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="4" y1="6" x2="20" y2="6"></line>
                        <line x1="4" y1="12" x2="20" y2="12"></line>
                        <line x1="4" y1="18" x2="20" y2="18"></line>
                    </svg>
                </button>
                <SiteBrandLink centered />
                <span class="layout-mobile-bar-spacer" aria-hidden="true"></span>
            </header>
            <div class="layout-right-body">
                <router-view />
            </div>
        </main>

        <div v-if="!isEditorRoute" class="layout-fab-group">
            <button class="layout-fab" @click="scrollToTop" title="回到顶部">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="18 15 12 9 6 15"></polyline>
                </svg>
            </button>
            <slot name="fab" />
        </div>

        <div class="layout-overlay" v-if="showLogin" @click.self="showLogin = false">
            <LoginView @login-success="onLoginSuccess" />
        </div>
    </div>
</template>

<script>
import LoginView from '@/views/LoginView.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import SiteBrandLink from '@/components/SiteBrandLink.vue'
import { editorState } from '@/utils/articleEditorState'

export default {
    name: 'AppLayout',
    components: { LoginView, AppSidebar, SiteBrandLink },
    data() {
        return {
            showLogin: false,
            sidebarOpen: false,
            isMobile: false,
        }
    },
    computed: {
        isEditorRoute() {
            if (this.$route.name === 'new-article') return true
            return this.$route.name === 'public-article' && editorState.inEditor
        },
    },
    watch: {
        '$route'() {
            this.closeSidebar()
        },
    },
    mounted() {
        this._mq = window.matchMedia('(max-width: 768px)')
        this._onMqChange = () => {
            this.isMobile = this._mq.matches
            if (!this.isMobile) this.sidebarOpen = false
        }
        this._onMqChange()
        this._mq.addEventListener('change', this._onMqChange)
        this._onAuthExpired = () => {
            this.showLogin = true
            this.$toast?.info('登录已过期，请重新登录')
        }
        window.addEventListener('auth-expired', this._onAuthExpired)
    },
    beforeUnmount() {
        this._mq?.removeEventListener('change', this._onMqChange)
        window.removeEventListener('auth-expired', this._onAuthExpired)
    },
    methods: {
        toggleSidebar() {
            this.sidebarOpen = !this.sidebarOpen
        },
        closeSidebar() {
            this.sidebarOpen = false
        },
        onLoginSuccess() {
            this.showLogin = false
            this.$refs.sidebar?.onAuthChange()
        },
        scrollToTop() {
            const right = this.$el.querySelector('.layout-right-body')
            if (right) right.scrollTo({ top: 0, behavior: 'smooth' })
        },
    },
}
</script>

<style scoped>
.app-layout {
    display: flex;
    height: 100%;
    gap: 6px;
}

.layout-right {
    flex: 1;
    min-width: 0;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg-white);
    border-radius: 8px;
    border: 1px solid var(--border-card);
}

.layout-right-body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
}

.layout-right :deep(.page) {
    padding: 28px 36px;
}

.layout-mobile-bar {
    display: none;
}

.layout-right :deep(.post-view--editing) {
    height: 100%;
}

.layout-right:has(.post-view--editing) {
    overflow: hidden;
}

.layout-right:has(.post-view--editing) .layout-right-body {
    overflow: hidden;
}

.layout-fab-group {
    position: fixed;
    bottom: calc(24px + env(safe-area-inset-bottom, 0px));
    right: calc(16px + env(safe-area-inset-right, 0px));
    z-index: 100;
}

.layout-fab {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 4px;
    background: transparent;
    color: var(--text-tertiary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.15s, background 0.15s;
    font-family: inherit;
    padding: 0;
}

.layout-fab:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

.layout-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 200;
}

@media (max-width: 768px) {
    .app-layout {
        gap: 0;
        height: 100%;
    }

    .layout-sidebar-backdrop {
        position: fixed;
        inset: 0;
        z-index: 140;
        background: rgba(0, 0, 0, 0.35);
    }

    .layout-right {
        width: 100%;
        border-radius: 0;
        box-shadow: none;
    }

    .layout-mobile-bar {
        display: grid;
        grid-template-columns: 28px 1fr 28px;
        align-items: center;
        gap: 6px;
        flex-shrink: 0;
        padding: 4px 8px;
        padding-top: calc(4px + env(safe-area-inset-top, 0px));
        border-bottom: 1px solid var(--border-color);
        background: var(--bg-white);
    }

    .layout-mobile-bar :deep(.site-brand) {
        justify-self: center;
        max-width: 100%;
    }

    .layout-mobile-bar-spacer {
        width: 28px;
        height: 28px;
        flex-shrink: 0;
    }

    .layout-mobile-menu {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border: none;
        border-radius: 4px;
        background: transparent;
        color: var(--text-secondary);
        cursor: pointer;
        flex-shrink: 0;
        padding: 0;
        font-family: inherit;
    }

    .layout-mobile-menu:active {
        background: var(--bg-hover);
    }

    .layout-right :deep(.page) {
        padding: 16px;
    }

    .layout-fab-group {
        bottom: calc(16px + env(safe-area-inset-bottom, 0px));
        right: calc(12px + env(safe-area-inset-right, 0px));
    }
}
</style>
