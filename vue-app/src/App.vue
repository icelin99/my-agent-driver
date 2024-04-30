<template>
  <div class="heading" >Heading</div>
  <div class="main-container">
    <div style="width:30%; display: flex; flex-direction: column;">
    <div class="container border-left" style="width:100%; height:33.3%;"><Map /></div>
    <div class="container border-left" style="width:100%; height:33.3%"><HelloWorld /></div>
    <div class="container border-left border-bottom" style="width:100%; height:33.3%"><HelloWorld /></div>
  </div>
    <div style="width:70%; display: flex; flex-direction: column;">
      <div style="width:100%; height:46%; display: flex; flex-direction: row;" class="container border-left border-right"><VideoView />
      </div>
      <div class="container border-left border-right border-bottom" style="width:100%; height:54%"><HelloWorld /></div>
    </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import VideoView from './components/VideoView.vue';
import Map from './components/MapView.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
    VideoView,
    Map
  }
}
</script>

<style>
::-webkit-scrollbar {
    display: none;  /* 完全不显示滚动条 */
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  overflow: hidden;
  /* margin-top: 60px; */
}
.heading {
  width: 100%;
  height:30px;
  top: 0px;
  border-bottom:1px solid #2c3e50;
  background-color: rgb(239, 254, 254);
}
.main-container {
  width: 100%;
  height: 855px;
  background-color: aliceblue;
  display: flex;
  flex-direction: row;
}
.container {
  width: 100%;
  height:100%;
  box-sizing: border-box;
  background-color: #ffffff;
  border-radius: 5px;
  /* border: 4px solid rgb(243, 246, 251); */
}

/* 对第一个容器特殊处理，只添加顶部边框 */

.border-left {
  border-top: 5px solid rgb(243, 246, 251); 
  border-left: 5px solid rgb(243, 246, 251);
}
.border-bottom {
  border-bottom: 5px solid rgb(243, 246, 251);
}
.border-right {
  border-right: 5px solid rgb(243, 246, 251); 
}
</style>
