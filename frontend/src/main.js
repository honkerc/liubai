import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { installToast } from './utils/toast'
import './styles/variables.css'
import 'highlight.js/styles/atom-one-dark.css'
import './styles/global.css'
import './styles/skeleton.css'
import './styles/page-list.css'

const app = createApp(App)
app.use(router)
installToast(app)
app.mount('#app')
