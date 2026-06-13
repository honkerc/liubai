import { request } from './request'

export const authApi = {
    login(username, password) {
        return request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        })
    },
}
