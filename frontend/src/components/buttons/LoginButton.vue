<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore(); 
// authStore.initAuth();

const login = async () => {
    await authStore.login();
};

</script>

<template>
    <button @click="login"
        class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300 hover:bg-red-500 bg-gray-700">
        <i class="pi pi-user mr-1"></i>
        <pre> LOGIN</pre>
    </button>
</template>