<script setup>
import { onMounted, reactive } from 'vue';
import axios from 'axios';
import CollectionListing from './CollectionListing.vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';


const state = reactive({
    collections: {},
    isLoading: true,
});

onMounted(async () => {
    try {
        const response = await axios.get('/api/collections');
        state.collections = response.data;
    } catch (error) {
        console.error('Error fetching collections', error);
    } finally {
        state.isLoading = false;
    }

})



</script>

<template>
    <!-- Collection Listings -->
    <!-- to go through the elements of article in a specific order the key is mandatory! -->

    <section class="bg-blue-50 px-4 py-10">
        <div class="container-xl lg:container m-auto">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
                Explore Collections
            </h2>
            <!-- Show loading spinner when it is loading -->
            <div v-if="state.isLoading" class=" text-center text-gray-500 py-6"> 
                <PulseLoader />
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <CollectionListing v-for="collection in state.collections" :key="collection.id" :collection="collection"/>
                    
            </div>
        </div>
    </section>

</template>
