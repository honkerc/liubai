import { createRouter, createWebHistory } from 'vue-router'

import AppLayout from '../components/AppLayout.vue'
import { formatPageTitle } from '../constants/brand'



const routes = [

    {

        path: '/login',

        name: 'login',

        component: () => import('../views/LoginView.vue'),

        meta: { title: '登录', layout: 'plain' },

    },

    {

        path: '/',

        component: AppLayout,

        children: [

            {

                path: '',

                name: 'portal-home',

                component: () => import('../views/PortalHomeView.vue'),

                meta: { title: '首页' },

            },

            {

                path: 'search',

                name: 'search',

                component: () => import('../views/SearchView.vue'),

                meta: { title: '搜索' },

            },

            {

                path: 'topics',

                name: 'topics',

                component: () => import('../views/TopicsView.vue'),

                meta: { title: '话题' },

            },

            {

                path: 'topic/:topic',

                name: 'topic',

                component: () => import('../views/TopicView.vue'),

                meta: { title: '话题' },

            },

            {

                path: 'post/new',

                name: 'new-article',

                component: () => import('../views/PostView.vue'),

                meta: { title: '写文章', requiresAuth: true },

            },

            {

                path: 'post/:title',

                name: 'public-article',

                component: () => import('../views/PostView.vue'),

                meta: { title: '文章' },

            },

            {

                path: 'editor',

                redirect: { name: 'new-article' },

            },

            {

                path: 'editor/:title',

                redirect: (to) => ({

                    name: 'public-article',

                    params: { title: to.params.title },

                }),

            },

            {

                path: ':pathMatch(.*)*',

                name: 'not-found',

                component: () => import('../views/NotFoundView.vue'),

                meta: { title: '页面不存在' },

            },

        ],

    },

]



const router = createRouter({

    history: createWebHistory(process.env.BASE_URL),

    routes,

})



router.beforeEach((to, from, next) => {

    const title = to.meta?.title

    document.title = formatPageTitle(title)



    if (to.meta?.requiresAuth) {

        const token = localStorage.getItem('token')

        if (!token) {

            next({ name: 'login', query: { redirect: to.fullPath } })

            return

        }

    }



    next()

})



export default router

