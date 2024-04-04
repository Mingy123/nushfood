<template>
  <div id="app" class="relative">
    <video autoplay></video>
    <div class="absolute top-0 inset-x-0 flex justify-center">
      <button @click="takePhoto"
        class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 text-3xl hover:bg-yellow-400">Take Photo</button>
      <input id="img_upload" type='file' accept=".jpg,.jpeg" class="hidden" />
      <label for="img_upload"
        class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 ml-8 text-3xl hover:bg-yellow-400">Upload
        Image</label>
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
      stream: null
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
            height: { min: 720 }
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
      // add a spinning circle thing to show it is loading
      let answer = await api_segment(dataURL)
      // send the user to the food result page here
      // (you may want to look into vue props)
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
    window.addEventListener('load', function () {
      document.querySelector('input[type="file"]').addEventListener('change', async function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = async function () {
            let answer = await api_segment(reader.result)
            // send the user to the food result page here
            // (you may want to look into vue props)
            console.log(answer)
            router.push({
              name: 'Food Result',
              query: {
                rawData: answer
              }
            })
          }
          reader.readAsDataURL(this.files[0]);
          // add a spinning circle thing to show it is loading
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