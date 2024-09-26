<script setup>
import ArticleListings from '@/components/ArticleListings.vue';
import Hero from '@/components/Hero.vue';
import HomeCards from '@/components/HomeCards.vue';
</script>

<template>
    <Hero />
    <HomeCards />
    <ArticleListings :limit="3" :showButton="true" />
</template>