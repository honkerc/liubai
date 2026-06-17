<template>
    <SimplePageShell title="关于" desc="关于这个站点">
        <div class="simple-prose">
            <p>
                <strong>{{ siteName }}</strong> — {{ siteTagline }}
            </p>
            <p>
                个人博客，用来记录技术笔记、项目实践与一些随想。
                你可以从首页浏览最新文章，或通过话题、搜索找到感兴趣的内容。
            </p>
            <ul>
                <li>访客可阅读已发布的文章</li>
                <li>登录后可撰写与管理文章</li>
                <li>支持 Markdown 写作与代码高亮</li>
            </ul>
        </div>
    </SimplePageShell>
</template>

<script>
import SimplePageShell from '@/components/SimplePageShell.vue'
import { SITE_NAME, SITE_TAGLINE } from '@/constants/brand'

export default {
    name: 'AboutView',
    components: { SimplePageShell },
    computed: {
        siteName() {
            return SITE_NAME
        },
        siteTagline() {
            return SITE_TAGLINE
        },
    },
}
</script>
