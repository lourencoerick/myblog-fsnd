<script setup>
import { useAuth0 } from '@auth0/auth0-vue';
const { loginWithRedirect } = useAuth0(); 

const login = async () => {
    loginWithRedirect();
};

</script>

<template>
    <button @click="login"
        class="relative flex items-center px-4 py-2 rounded-lg hover:text-white transition-colors duration-300 hover:bg-red-500 bg-gray-700">
        <i class="pi pi-user mr-1"></i>
        <pre> LOGIN</pre>
    </button>
</template>