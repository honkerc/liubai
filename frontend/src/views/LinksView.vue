<template>
    <SimplePageShell title="链接" desc="相关链接与资源">
        <div class="simple-link-list">
            <a
                v-for="item in links"
                :key="item.url"
                :href="item.url"
                class="simple-link-item"
                target="_blank"
                rel="noopener noreferrer"
            >
                <span class="simple-link-item__label">{{ item.label }}</span>
                <span class="simple-link-item__hint">{{ item.hint }}</span>
            </a>
        </div>
    </SimplePageShell>
</template>

<script>
import SimplePageShell from '@/components/SimplePageShell.vue'

export default {
    name: 'LinksView',
    components: { SimplePageShell },
    data() {
        return {
            links: [
                {
                    label: 'GitHub 仓库',
                    hint: 'honkerc/liubai',
                    url: 'https://github.com/honkerc/liubai',
                },
            ],
        }
    },
}
</script>
