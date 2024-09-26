<script setup>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { RouterView } from 'vue-router';
</script>

<template>
    <div class="min-h-screen flex flex-col">
        <Navbar />
        <!-- Main Content Area (grows to fill the space) -->
        <main class="flex-grow">
            <RouterView />
        </main>
        <Footer />
    </div>
</template>