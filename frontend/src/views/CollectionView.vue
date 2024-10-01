<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import router from '@/router';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import BackButton from '@/components/BackButton.vue';
import ArticleListings from  '@/components/ArticleListings.vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { useAuth0 } from '@auth0/auth0-vue';

const route = useRoute();
const toast = useToast();
const { isAuthenticated, getAccessTokenSilently } = useAuth0();

const collectionId = route.params.id;

const state = reactive({
    collection: {},
    isLoading: true,
});

const deleteCollection = async () => {
    try {
        const confirm = window.confirm('Are you sure you want to delete this collection?');
        const token = await getAccessTokenSilently();

        if (confirm) {
            await axios.delete(`/api/collections/${collectionId}`,          {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            toast.success('Collection deleted');
            router.push('/collections');
        }

    } catch (error) {
        console.error('Error fetching collections', error);
        toast.error('Collection was not deleted');
    }
};

onMounted(async () => {
    try {
        const response = await axios.get(`/api/collections/${collectionId}`);
        state.collection = response.data.collection;
    } catch (error) {
        console.error('Error fetching collection', error);
    } finally {
        state.isLoading = false;
    }

})
</script>

<template>
    <!-- <BackButton /> -->
    <section v-if="!state.isLoading" class="bg-white">
        <BackButton text="Back to Collection Listings" to="/collections" />
        <div class="container m-auto py-10 px-6">
            <div class="grid grid-cols-1 w-full gap-6"
                :class="[
                isAuthenticated
                  ? 'md:grid-cols-70/30' 
                  : ''
              ]">
                <main>
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h2 class="text-gray-800 text-3xl font-bold mb-6">
                            {{ state.collection.title }}
                        </h2>

                        <p class="mb-4">
                            {{ state.collection.description }}
                        </p>
                    </div>
                </main>


                <!-- Sidebar -->
                <aside v-if="isAuthenticated" >
                    <!-- Manage -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl font-bold mb-6">Manage Collection</h3>
                        <RouterLink :to="`/collections/edit/${state.collection.id}`"
                            class="bg-gray-500 hover:bg-gray-600 text-white text-center font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline mt-4 block">
                            Edit Collection</RouterLink>
                        <button @click="deleteCollection"
                            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline mt-4 block">
                            Delete Collection
                        </button>
                    </div>
                </aside>
            </div>
        </div>
        <ArticleListings :collectionID="collectionId" :headingText="`Explore articles about ${state.collection.title}`"/>
    </section>

    <div v-else class="text-center text-gray-500 py-6">
        <PulseLoader />
    </div>

</template>