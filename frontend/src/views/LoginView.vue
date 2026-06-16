<template>
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
                    stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <h2 class="login-title">欢迎回来</h2>
            <p class="login-subtitle">{{ expired ? '登录已过期，请重新登录' : '请登录您的账号' }}</p>
            <div class="form-group">
                <input type="text" v-model="username" placeholder="用户名" class="form-input" />
            </div>
            <div class="form-group">
                <input type="password" v-model="password" placeholder="密码" class="form-input"
                    @keyup.enter="handleLogin" />
            </div>
            <div class="error-msg" v-if="error">{{ error }}</div>
            <button class="login-btn" @click="handleLogin" :disabled="loading">
                {{ loading ? '登录中...' : '登录' }}
            </button>
        </div>
    </div>
</template>

<script>
import { authApi } from '@/api'
import { setToken } from '@/utils/authSession'

export default {
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
    },
    methods: {
        async handleLogin() {
            if (!this.username || !this.password) {
                this.error = '请输入用户名和密码'
                this.$toast.info('请输入用户名和密码')
                return
            }
            this.loading = true
            this.error = ''
            try {
                const res = await authApi.login(this.username, this.password)
                setToken(res.access_token)
                this.$toast.success('登录成功')
                this.$emit('login-success')
                const redirect = this.$route.query.redirect || '/'
                this.$router.push(redirect)
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
    height: 100%;
}

.login-card {
    width: 340px;
    padding: 40px 32px 32px;
    background: var(--bg-white);
    border-radius: 6px;
    box-shadow: var(--shadow-md);
    text-align: center;
}

.login-icon {
    display: flex;
    justify-content: center;
    margin-bottom: 16px;
}

.login-icon svg {
    opacity: 0.6;
    color: var(--icon-color);
}

.login-title {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.login-subtitle {
    font-size: 13px;
    color: var(--text-tertiary);
    margin-bottom: 28px;
}

.form-group {
    margin-bottom: 14px;
}

.form-input {
    width: 100%;
    padding: 11px 14px;
    font-size: 14px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    outline: none;
    transition: all 0.2s;
    box-sizing: border-box;
    font-family: inherit;
    background-color: var(--bg-hover);
    color: var(--text-primary);
}

.form-input:focus {
    border-color: var(--primary);
    background-color: var(--bg-white);
    box-shadow: 0 0 0 3px rgba(79, 110, 247, 0.08);
}

.form-input::placeholder {
    color: var(--text-tertiary);
}

.error-msg {
    color: #d93025;
    font-size: 13px;
    margin-bottom: 12px;
    text-align: left;
}

.login-btn {
    width: 100%;
    padding: 11px;
    font-size: 14px;
    font-weight: 500;
    color: #ffffff;
    background-color: var(--text-primary);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
    letter-spacing: 0.3px;
}

.login-btn:hover {
    background-color: var(--text-secondary);
}

.login-btn:active {
    transform: scale(0.98);
}

.login-btn:disabled {
    background-color: var(--text-tertiary);
    cursor: not-allowed;
    transform: none;
}

@media (max-width: 768px) {
    .login-card {
        width: 90vw;
        max-width: 340px;
        padding: 32px 24px 28px;
    }
}
</style>
