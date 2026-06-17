<template>
    <div class="login-wrapper" :class="{ 'login-wrapper--page': isStandalone }">
        <header v-if="isStandalone" class="login-page-top">
            <router-link to="/" class="login-page-home">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
                返回首页
            </router-link>
        </header>

        <div class="login-card">
            <button
                v-if="!isStandalone"
                type="button"
                class="login-close"
                aria-label="关闭"
                @click="$emit('close')"
            >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="1.75" stroke-linecap="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>

            <div v-if="expired" class="login-notice" role="status">
                登录已过期，请重新登录
            </div>

            <div class="login-brand" :class="{ 'login-brand--page': isStandalone }">
                <img class="login-brand__logo" :src="siteLogo" alt="" width="28" height="28" />
                <div class="login-brand__text">
                    <h1 class="login-title">{{ siteName }}</h1>
                    <p class="login-subtitle">
                        {{ isStandalone ? siteTagline : (expired ? '请重新登录后继续' : '登录后继续写作与管理') }}
                    </p>
                </div>
            </div>

            <form class="login-form" @submit.prevent="handleLogin">
                <label class="login-field">
                    <span class="login-field__label">用户名</span>
                    <input
                        ref="usernameInput"
                        v-model="username"
                        type="text"
                        autocomplete="username"
                        placeholder="请输入用户名"
                        class="login-field__input"
                    />
                </label>
                <label class="login-field">
                    <span class="login-field__label">密码</span>
                    <input
                        v-model="password"
                        type="password"
                        autocomplete="current-password"
                        placeholder="请输入密码"
                        class="login-field__input"
                    />
                </label>
                <p v-if="error" class="login-error" role="alert">{{ error }}</p>
                <button type="submit" class="login-btn" :disabled="loading">
                    {{ loading ? '登录中…' : '登录' }}
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import { authApi } from '@/api'
import { SITE_NAME, SITE_LOGO, SITE_TAGLINE } from '@/constants/brand'
import { setToken } from '@/utils/authSession'

export default {
    emits: ['login-success', 'close'],
    data() {
        return {
            username: '',
            password: '',
            error: '',
            loading: false,
        }
    },
    computed: {
        expired() {
            return this.$route.query.expired === '1'
        },
        isStandalone() {
            return this.$route.name === 'login'
        },
        siteName() {
            return SITE_NAME
        },
        siteLogo() {
            return SITE_LOGO
        },
        siteTagline() {
            return SITE_TAGLINE
        },
    },
    mounted() {
        this.$nextTick(() => {
            this.$refs.usernameInput?.focus()
        })
    },
    methods: {
        async handleLogin() {
            if (!this.username || !this.password) {
                this.error = '请输入用户名和密码'
                return
            }
            this.loading = true
            this.error = ''
            try {
                const res = await authApi.login(this.username, this.password)
                setToken(res.access_token)
                this.$toast.success('登录成功')
                this.$emit('login-success')
                if (this.isStandalone) {
                    const redirect = this.$route.query.redirect || '/'
                    this.$router.push(redirect)
                }
            } catch (e) {
                this.error = e.message || '登录失败'
                this.$toast.error(this.error)
            } finally {
                this.loading = false
            }
        },
    },
}
</script>

<style scoped>
.login-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: 16px;
    box-sizing: border-box;
}

.login-wrapper--page {
    position: relative;
    flex-direction: column;
    align-items: stretch;
    justify-content: center;
    min-height: 100%;
    padding: 24px 16px;
    background: var(--bg-body);
}

.login-page-top {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    padding: 16px 20px;
}

.login-page-home {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.15s;
}

.login-page-home:hover {
    color: var(--primary);
}

.login-card {
    position: relative;
    width: 100%;
    max-width: 360px;
    margin: 0 auto;
    padding: 28px 24px 24px;
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 10px;
    box-shadow: var(--shadow-md);
}

.login-wrapper--page .login-card {
    max-width: 400px;
    padding: 32px 28px 28px;
    border-radius: 12px;
    box-shadow: var(--shadow-card);
}

.login-close {
    position: absolute;
    top: 12px;
    right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--text-tertiary);
    cursor: pointer;
    padding: 0;
    transition: color 0.15s, background 0.15s;
}

.login-close:hover {
    color: var(--text-secondary);
    background: var(--bg-hover);
}

.login-notice {
    margin: -4px 0 16px;
    padding: 8px 10px;
    border-radius: 8px;
    font-size: 13px;
    color: #b45309;
    background: #fffbeb;
    border: 1px solid #fde68a;
    line-height: 1.4;
}

.login-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding-right: 24px;
}

.login-brand--page {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-right: 0;
    margin-bottom: 28px;
}

.login-brand__logo {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    object-fit: contain;
}

.login-brand--page .login-brand__logo {
    width: 40px;
    height: 40px;
}

.login-brand__text {
    min-width: 0;
}

.login-title {
    margin: 0 0 2px;
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.login-brand--page .login-title {
    margin-top: 12px;
    font-size: 24px;
}

.login-subtitle {
    margin: 0;
    font-size: 13px;
    color: var(--text-tertiary);
    line-height: 1.45;
}

.login-brand--page .login-subtitle {
    margin-top: 4px;
    font-size: 14px;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.login-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.login-field__label {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
}

.login-field__input {
    width: 100%;
    padding: 10px 12px;
    font-size: 14px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
    box-sizing: border-box;
    font-family: inherit;
    background: var(--bg-white);
    color: var(--text-primary);
}

.login-field__input:focus {
    border-color: rgba(79, 110, 247, 0.45);
    box-shadow: 0 0 0 3px var(--primary-light);
}

.login-field__input::placeholder {
    color: var(--text-tertiary);
}

.login-error {
    margin: -2px 0 0;
    font-size: 13px;
    color: #dc2626;
    line-height: 1.4;
}

.login-btn {
    width: 100%;
    margin-top: 4px;
    padding: 10px 12px;
    font-size: 14px;
    font-weight: 500;
    color: #fff;
    background: var(--primary);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s, opacity 0.15s;
    font-family: inherit;
}

.login-btn:hover:not(:disabled) {
    background: var(--primary-hover);
}

.login-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

@media (max-width: 768px) {
    .login-wrapper--page {
        padding: 20px 12px;
    }

    .login-page-top {
        padding: 12px 14px;
    }

    .login-card,
    .login-wrapper--page .login-card {
        padding: 24px 20px 20px;
    }

    .login-brand--page .login-title {
        font-size: 22px;
    }
}
</style>
