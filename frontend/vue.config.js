const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
    devServer: {
        port: 8080,
        proxy: {
            '/api': { target: 'http://127.0.0.1:8000' },
            '/uploads': { target: 'http://127.0.0.1:8000' },
        },
    },
})