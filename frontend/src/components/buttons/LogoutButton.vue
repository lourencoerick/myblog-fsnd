<script setup>
import { useAuth0 } from '@auth0/auth0-vue';

const auth0 = useAuth0();

const logout = () => {
    auth0.logout();
};
</script>

<template>
    <button @click="logout"
        class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300 hover:bg-red-500 bg-gray-700">
        <i class="pi pi-sign-out mr-1"></i>
        <pre> LOGOUT</pre>
    </button>
</template>