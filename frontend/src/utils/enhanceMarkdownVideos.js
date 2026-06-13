/** 根据视频宽高比标记竖屏/横屏，避免竖屏视频被拉满整行 */
export function enhanceMarkdownVideos(root) {
    if (!root) return

    root.querySelectorAll('video').forEach((video) => {
        if (video.dataset.videoEnhanced) return
        video.dataset.videoEnhanced = '1'
        video.classList.add('markdown-video')
        video.removeAttribute('style')

        const apply = () => {
            const { videoWidth, videoHeight } = video
            if (!videoWidth || !videoHeight) return
            const portrait = videoHeight > videoWidth
            video.classList.toggle('is-portrait', portrait)
            video.classList.toggle('is-landscape', !portrait)
        }

        if (video.readyState >= 1) {
            apply()
        } else {
            video.addEventListener('loadedmetadata', apply, { once: true })
        }
    })
}
