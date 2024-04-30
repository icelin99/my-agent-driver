import { createApp } from 'vue'
import App from './App.vue'
import VueVideoPlayer from 'vue-video-player'
import 'video.js/dist/video-js.css'
// import "vue-video-player/src/custom-theme.css"

const app = createApp(App)
app.use(VueVideoPlayer)
app.mount('#app')
