<script setup>
import { defineProps } from 'vue';

defineProps({
  title: {
    type: String,
    default: 'Your daily pill of knowledge',
  },
   subtitle: {
    type: String,
    default: 'Unlock insights that matter. <br> Choose your next article wisely and feed your curiosity',
  },
});
</script>

<template>
  <section class="bg-gray-800 py-20 mb-4 mt-[1px]">
    <div
      class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center"
    >
      <div class="text-center my-auto">
        <h1 class="text-4xl font-bold text-white sm:text-5xl md:text-6xl">
          {{ title }}
        </h1>
        <p class="my-4 text-xl text-white" v-html="subtitle">
        </p>
      </div>
    </div>
  </section>
</template>