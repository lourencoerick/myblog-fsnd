<script setup>
import { RouterLink } from 'vue-router';
import { defineProps } from 'vue';

const props = defineProps({
  text: {
    type: String,
    default: 'Back to Article Listings'
  },
  to: {
    type: String,
    default: '/articles'
  }
});

</script>

<template>
  <section>
    <div class="container m-auto py-6 px-6">
      <RouterLink :to="`${props.to}`" class="text-red-500 hover:text-red-600 flex items-center">
        <i class="pi pi-arrow-circle-left mr-3"></i> {{ props.text }}
      </RouterLink>
    </div>
  </section>
</template>