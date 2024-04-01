<template>
  <div id="app" class="relative">
    <video autoplay></video>
    <div class="absolute top-0 inset-x-0 flex justify-center">
      <button class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 text-3xl hover:bg-yellow-400">Take Photo</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  components: {},
  data: function () {
    return {
      stream: null
    }
  },
  methods: {
    init: async function () {
      if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
        console.log('gaming')
        let constraints = {
          video: {
            width: { min: 1280 },
            height: { min: 720 }
          },
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);

        const video = document.querySelector('video');
        video.srcObject = stream
        video.play()
      }
    },
    getDevices: async function () {
      const devices = await navigator.mediaDevices.enumerateDevices();
    }
  },
  beforeMount: function () {
    this.init();
  }
}
</script>

<style>
video {
  width: 100%;
  background: rgba(0, 0, 0, 0.2);
}
</style>