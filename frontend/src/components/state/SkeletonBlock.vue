<template>
    <span
        class="skeleton-block"
        :style="{ width, height, borderRadius: radius }"
    ></span>
</template>

<script>
export default {
    name: 'SkeletonBlock',
    props: {
        width: { type: String, default: '100%' },
        height: { type: String, default: '14px' },
        radius: { type: String, default: '6px' },
    },
}
</script>
