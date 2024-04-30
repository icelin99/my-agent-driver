<template>
    <div class="map-container">
        <img :src="mapUrl" alt="map" class="map-img" />
    </div>
</template>

<script>
export default {
    name: 'MapView',
    // components: {

    // },
    data() {
        return {
            mapUrl: "./assets/map.png",
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.map-container {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.map-img {
    position: relative;
    width: auto; /* 自适应容器宽度 */
    height: 100%; /* 保持图像比例 */

}
</style>
