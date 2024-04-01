<template>
  <div class="flex justify-center h-screen bg-gradient-to-r from-pink-500 to-yellow-500">
    <div class="flex flex-col justify-center items-center">
      <img src="/src/assets/ncl.png" class="w-48">
      <h1 class="text-5xl font-black m-2">NUSHFood</h1>
      <p class="text-xl mx-12 text-center">The automatic price detector for NUSH food stalls.</p>
    </div>
  </div>
  <div class="flex justify-center flex-col p-8 h-screen">
    <p class="text-center text-xl">Choose whether you're using this on a food or drink...</p>
    <div class="flex justify-center flex-row gap-4 p-8">
      <RouterLink class="h-fit bg-purple-200 p-12 rounded-xl" to="/drink">
        <img src="https://openmoji.org/data/color/svg/1F379.svg">
        <p class="text-xl m-2">Drink</p>
      </RouterLink>
      <RouterLink class="h-fit bg-yellow-200 p-12 rounded-xl" to="/food">
        <img src="https://openmoji.org/data/color/svg/1F35B.svg">
        <p class="text-xl m-2">Food</p>
      </RouterLink>
    </div>
  </div>
</template>