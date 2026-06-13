<template>
    <router-link to="/" class="site-brand" :class="{ 'site-brand--centered': centered }" title="首页">
        <img class="site-brand-logo" :src="siteLogo" alt="" width="20" height="20" />
        <span class="site-brand-name">{{ siteName }}</span>
    </router-link>
</template>

<script>
import { SITE_NAME, SITE_LOGO } from '@/constants/brand'

export default {
    name: 'SiteBrandLink',
    props: {
        centered: { type: Boolean, default: false },
    },
    computed: {
        siteName() {
            return SITE_NAME
        },
        siteLogo() {
            return SITE_LOGO
        },
    },
}
</script>

<style scoped>
.site-brand {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
    text-decoration: none;
    color: var(--text-secondary);
    transition: color 0.15s;
}

.site-brand:hover {
    color: var(--text-primary);
}

.site-brand--centered {
    justify-content: center;
}

.site-brand-logo {
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    display: block;
    object-fit: contain;
}

.site-brand-name {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
