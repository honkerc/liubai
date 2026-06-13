<template>

    <div :class="rootClass">

        <router-view />

        <Toast />

    </div>

</template>



<script>

import Toast from '@/components/Toast.vue'



export default {

    name: 'App',

    components: { Toast },

    computed: {

        rootClass() {

            return this.$route.name === 'login' ? 'plain-root' : 'app-container'

        },

    },

}

</script>

