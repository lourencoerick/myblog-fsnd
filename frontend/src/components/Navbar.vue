<script setup>
import { RouterLink, useRoute } from 'vue-router';
import logo from '@/assets/mylogo.png';

const route = useRoute();
const isActive = (path) => {
  return route.path === path;
};
</script>

<template>
  <header class="bg-gray-800 text-white p-4">
    <div class="container mx-auto flex items-center justify-between">
      <!-- Logo or Brand Name -->
      <RouterLink class="hover:text-gray-400 flex flex-shrink-0 items-center mr-4" to="/">
        <img class="h-10 w-auto" :src="logo" alt=" My Blog" />
        <span class="hidden md:block text-white text-2xl font-bold ml-2"> My Blog</span>
      </RouterLink>


      <!-- Navigation -->
      <nav>
        <ul class="flex space-x-4">
          <li>
            <RouterLink to="/"
              class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300"
              :class="[
                isActive('/')
                  ? 'bg-red-600 text-white'
                  : 'hover:bg-red-500 hover:text-white'
              ]">
              <i class="pi pi-home mr-1"></i> Home
              <span v-if="isActive('/')"
                class="absolute inset-0 border-2 border-red-600 rounded-lg pointer-events-none"></span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/articles"
              class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300"
              :class="[
                isActive('/articles')
                  ? 'bg-red-600 text-white'
                  : 'hover:bg-red-500 hover:text-white'
              ]">
              <i class="pi pi-book mr-1"></i> Explore Articles
              <span v-if="isActive('/articles')"
                class="absolute inset-0 border-2 border-red-600 rounded-lg pointer-events-none"></span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/collections"
              class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300"
              :class="[
                isActive('/collections')
                  ? 'bg-red-600 text-white'
                  : 'hover:bg-red-500 hover:text-white'
              ]">
              <i class="pi pi-folder mr-1"></i> Explore Collections
              <span v-if="isActive('/collections')"
                class="absolute inset-0 border-2 border-red-600 rounded-lg pointer-events-none"></span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/articles/add"
              class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300"
              :class="[
                isActive('/articles/add')
                  ? 'bg-red-600 text-white'
                  : 'hover:bg-red-500 hover:text-white'
              ]">
              <i class="pi pi-plus mr-1"></i> Add New Article
              <span v-if="isActive('/articles/add')"
                class="absolute inset-0 border-2 border-red-600 rounded-lg pointer-events-none"></span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/collections/add"
              class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300"
              :class="[
                isActive('/collections/add')
                  ? 'bg-red-600 text-white'
                  : 'hover:bg-red-500 hover:text-white'
              ]">
              <i class="pi pi-plus-circle mr-1"></i> Add New Collection
              <span v-if="isActive('/collections/add')"
                class="absolute inset-0 border-2 border-red-600 rounded-lg pointer-events-none"></span>
            </RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>
