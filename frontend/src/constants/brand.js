/** 站点品牌 */
export const SITE_NAME = '留白'
export const SITE_TAGLINE = '予一席空白'
export const SITE_DESCRIPTION = '留白 — 个人博客，予一席空白'
export const SITE_LOGO = `${process.env.BASE_URL}cat.svg`

/** 浏览器标签页标题 */
export function formatPageTitle(pageTitle) {
    if (!pageTitle || pageTitle === SITE_NAME) return SITE_NAME
    return `${pageTitle} · ${SITE_NAME}`
}
