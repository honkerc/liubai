<template>

    <div :class="rootClass">

        <router-view />

        <Toast />

    </div>

</template>



<script>
import Toast from '@/components/Toast.vue'
import { initAuthSession } from '@/utils/authSession'

export default {
    name: 'App',
    components: { Toast },
    mounted() {
        initAuthSession()
    },

    computed: {

        rootClass() {

            return this.$route.name === 'login' ? 'plain-root' : 'app-container'

        },

    },

}

</script>

