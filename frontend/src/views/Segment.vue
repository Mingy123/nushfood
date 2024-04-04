<template>
  <div id="app" class="relative">
    <video autoplay></video>
    <div class="absolute top-0 inset-x-0 flex justify-center">
      <button @click="takePhoto"
        class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 text-3xl hover:bg-yellow-400">Take Photo</button>
      <input id="img_upload" type='file' accept=".jpg,.jpeg" class="hidden" />
      <label for="img_upload"
        class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 ml-8 text-3xl hover:bg-yellow-400 text-center">Upload
        Image</label>
    </div>
    <div v-if="img_processing" class="absolute inset-0 bg-white opacity-60 flex justify-center items-center">
      <img src="/src/assets/loading.gif" class="w-48 ">
    </div>
  </div>
</template>

<script>
import { api_segment } from '../api.js'


export default {
  name: 'app',
  components: {},
  data: function () {
    return {
      stream: null,
      img_processing: false
    }
  },
  methods: {
    init: async function () {
      // var output = document.createElement('p');
      // document.body.appendChild(output);
      // output.innerHTML = navigator.mediaDevices
      if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
        console.log('gaming')
        let constraints = {
          video: {
            width: { min: 1280 },
            height: { min: 720 },
            facingMode: 'environment'
          },
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);

        const video = document.querySelector('video');
        video.srcObject = stream
        video.play()
      } else {
        console.log("oops")
      }
    },
    getDevices: async function () {
      const devices = await navigator.mediaDevices.enumerateDevices();
    },
    takePhoto: async function () {
      const router = this.$router
      const video = document.querySelector('video');
      var canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      var ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      var dataURL = canvas.toDataURL('image/jpeg');
      this.img_processing = true
      // add a spinning circle thing to show it is loading
      let answer = await api_segment(dataURL)
      console.log(answer)
      router.push({
        name: 'Food Result',
        query: {
          rawData: answer
        }
      })
    },
  },
  beforeMount: function () {
    this.init();
    const router = this.$router
    let _this = this;
    window.addEventListener('load', function () {
      document.querySelector('input[type="file"]').addEventListener('change', async function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = async function () {
            _this.img_processing = true
            // add a spinning circle thing to show it is loading
            let answer = await api_segment(reader.result)
            console.log(answer)
            router.push({
              name: 'Food Result',
              query: {
                rawData: answer
              }
            })
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
    });

  }
}
</script>

<style>
video {
  width: 100%;
  background: rgba(0, 0, 0, 0.2);
}
</style>