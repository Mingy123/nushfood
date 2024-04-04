<script setup>
import { ref } from 'vue'
import QrcodeVue from 'qrcode.vue'

const props = defineProps(['rawData'])
const data = JSON.parse(props.rawData)

console.log()

const items = ref(data["result"])
const price = data["price"]
const payNowString = data["paynow"]
const billRef = data["bill"]

</script>

<template>
    <h2 class="text-center text-xl font-bold my-4">Results</h2>
    <div class="text-2xl mx-4">
        <p>You've ordered:</p>
        <ul class="list-disc mx-8" v-for="item in items">
            <li>{{ item[0] }} <span class="text-gray-500">{{ item[1] }}</span></li>
            <!-- <li>Rice</li>
            <li>Scrambled Egg <span class="text-gray-500">(Veg)</span></li>
            <li>Pork Belly <span class="text-gray-500">(Meat)</span></li> -->
        </ul>
        <p class="my-4">Total Cost: <span class="font-bold">${{ price.toFixed(2) }}</span></p>
        <div class="flex flex-row justify-center align-center p-8">
            <qrcode-vue :value=payNowString size=300 level="M" />
        </div>
        <p class="text-center">Bill Reference: {{ billRef }}</p>
    </div>
    <div class="absolute bottom-4 inset-x-0 flex justify-center">
        <RouterLink to="/food">
            <button
                class="bg-yellow-200 rounded-full p-4 pl-6 pr-6 font-bold mt-2 text-3xl hover:bg-yellow-400">Back</button>
        </RouterLink>
    </div>
</template>