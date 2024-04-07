<script setup>
import { ref } from 'vue'
import QrcodeVue from 'qrcode.vue'

const props = defineProps(['rawData'])
const data = props.rawData

console.log()

const items = ref(data["result"])
const price = data["price"]
const payNowString = data["paynow"]
const billRef = data["bill"]

</script>

<template>
    <h2 class="text-center text-xl font-bold my-4">Results</h2>
    <div class="text-2xl mx-4">
        <p>Your drink is {{ data }}</p><br><br>
        <p>Price: $1.00</p>
    </div>
    <div class="absolute bottom-4 inset-x-0 flex justify-center">
        <RouterLink to="/drink">
            <button
                class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 text-3xl hover:bg-yellow-400">Back</button>
        </RouterLink>
    </div>
</template>