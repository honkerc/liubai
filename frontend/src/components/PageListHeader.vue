<template>
    <div class="page-list-header">
        <div class="page-list-header__inner">
            <svg
                v-if="showIcon"
                class="page-list-header__icon"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
            >
                <template v-if="icon === 'tag'">
                    <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                    <circle cx="7" cy="7" r="1.5" fill="currentColor" stroke="none"></circle>
                </template>
                <template v-else>
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </template>
            </svg>
            <div class="page-list-header__text">
                <slot />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PageListHeader',
    props: {
        showIcon: { type: Boolean, default: true },
        icon: { type: String, default: 'search' },
    },
}
</script>
