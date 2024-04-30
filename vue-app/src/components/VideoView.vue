<template>
    <div class="container" style="display: flex; flex-direction: row;">
        <div style="width:62%; height:100%;" class="video-view">
            <video-player class="player" ref="videoPlayer" :options="playerOptions" :playsinline="true" @play="onPlay" @pause="onPause" @timeupdate="onTimeUpdate($event)" />
        </div>
        <div style="width:38%; height:100%;" class="image-container">
            <img :src="currentPointCloudUrl" alt="Point Cloud View" class="responsive-image" />
        </div>
    </div>
    
</template>

<script>
import { videoPlayer } from 'vue-video-player'
import 'video.js/dist/video-js.css'

export default {
    name: 'VideoView',
    components: {
        videoPlayer
    },
    data() {
        return {
            fps: 5.0,
            playerOptions: {
                playbackRates: [0.5, 1.0, 1.5, 2.0], // 播放速度
                live: true,
                controls: true, 
                preload: "auto",
                fluid: true,
                muted: false, // 是否静音
                controlBar: {
                    timeDivider: true,
                    durationDisplay: true,
                    remainingTimeDisplay: true,
                    currentTimeDisplay: true, // 当前时间
                    volumeControl: false, // 声音控制键
                    playToggle: true, // 暂停和播放键
                    progressControl: true, // 进度条
                    fullscreenToggle: true, // 全屏按钮
                },
                sources: [
                    {
                        type: "video/mp4",
                        src: "/assets/output.mp4",
                    },
                ],
                width: document.documentElement.clientWidth,
            },
            currentPointCloudUrl: ''
        }
    },
    methods: {
        goToNextFrame() {
            const frameTime = 1 / this.fps; // fps 是视频的帧率
            this.$refs.videoPlayer.currentTime += frameTime;
        },
        goToPrevFrame() {
            const frameTime = 1 / this.fps;
            this.$refs.videoPlayer.currentTime -= frameTime;
        },
        onPlay() {
            console.log(this.$ref.videoPlayer.currentTime)
            console.log('Video is now playing');
        },
        onPause() {
            console.log('Video is paused');
        },
        onTimeUpdate(event) {
            const currentTime = event.target.player.cache_.currentTime;
            const currentFrame = Math.floor(currentTime * this.fps);
            console.log(currentTime, currentFrame)
            this.updatePointCloudView(currentFrame);
        },
        updatePointCloudView(frame) {
            this.currentPointCloudUrl = `./assets/point-cloud-image/point_cloud_top_${frame}.png`;
            console.log(this.currentPointCloudUrl)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.video-view {
    background-color: #ffffff;
    position: relative;
}
.video-player-box {
  width: 100%; /* Ensure that the video fills the component */
}
.player {
    padding-top:3px;
    padding-bottom: 4px;
    background-color: #ffffff;
    position: absolute;
}

::v-deep .vjs-control-bar {
  position: absolute;
  bottom: -28px !important; /* Adjust this value based on the control bar height */
  width: 100%;
}

.image-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.responsive-image {
  position: relative;
  width: 100%; /* 自适应容器宽度 */
  height: auto; /* 保持图像比例 */
  clip-path: inset(50px 50px 50px 50px); /* 上 右 下 左 */
}
</style>
