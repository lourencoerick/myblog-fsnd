<script setup>
import { RouterLink } from 'vue-router';
import Card from '@/components/Card.vue';
</script>

<template>
  <section class="py-4">
    <div class="container-xl lg:container m-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-lg">
        <Card>
          <h2 class="text-2xl font-bold">For Everyone</h2>
          <p class="mt-2 mb-4">
            Discover a world of fresh perspectives. Dive into insightful articles and stories—find new content that informs and inspires
          </p>
          <RouterLink
            to="/articles"
            class="inline-block bg-gray-800 text-white rounded-lg px-4 py-2 hover:bg-gray-700"
          >
            Explore Articles
          </RouterLink>
        </Card>
        <Card bg="bg-red-100">
          <h2 class="text-2xl font-bold">For Creators</h2>
          <p class="mt-2 mb-4">
            Fuel the world with your creativity. Share your insights, stories, and ideas—add new content that inspires and connects
          </p>
          <RouterLink
            to="/articles/add"
            class="inline-block bg-red-600 text-white rounded-lg px-4 py-2 hover:bg-red-500"
          >
            Write an Article
          </RouterLink>
        </Card>
      </div>
    </div>
  </section>
</template>