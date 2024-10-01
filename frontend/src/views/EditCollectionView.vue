<script setup>
import axios from 'axios';
import { ref, reactive, onMounted } from 'vue';
import router from '@/router';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useAuth0 } from '@auth0/auth0-vue';

const { getAccessTokenSilently } = useAuth0();
const route = useRoute();
const collectionId = route.params.id

const toast = useToast();

const form = reactive({
    title: '',
    description: '',
    selectedArticles: []
});

const articles = ref([]);
// articles.value = ["1"]

const getArticles = async () => {
    try {
        const response = await axios.get('/api/articles');
        articles.value = response.data.articles;
    } catch (error) {
        console.error('Error fetching articles:', error);
    }
};


const state = reactive({
    collection: {},
    isLoading: true
});

const populateForm = async () => {
    try {
        const response = await axios.get(`/api/collections/${collectionId}`)
        state.collection = response.data.collection;
        // populate inputs
        form.title = state.collection.title;
        form.description = state.collection.description;
        form.selectedArticles = state.collection.articles;
        console.log(state.collection);

    } catch (error) {
        console.error('Error fetching article', error)
    } finally {
        state.isLoading = false;
    }

}
onMounted(() => {
    getArticles();
    populateForm();
});


const addCollection = async () => {
    const token = await getAccessTokenSilently();

    const newCollection = {
        title: form.title,
        description: form.description,
        article_ids: form.selectedArticles
    };
    try {
        const response = await axios.patch('/api/collections/', newCollection,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        toast.success('Collection added sucessfully');
        console.log(response);
        router.push(`/collections/${response.data.id}`);
    } catch (error) {
        console.error('Error adding a new collection', error);
        toast.error('Collection was not added');
    }
};

</script>

<template>
    <div class="add-collection  mx-auto p-6 bg-gray-100 rounded-lg shadow-md">
        <h2 class="text-xl font-bold mb-4 text-gray-600">Add New Collection</h2>
        <form @submit.prevent="addCollection">
            <div class="mb-4">
                <label for="collectionTitle" class="block text-gray-600 mb-2">Collection Name:</label>
                <input type="text" v-model="form.title" required
                    class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-red-600" />
            </div>
            <div class="mb-4">
                <label for="collectionDescription" class="block text-gray-600 mb-2">Collection Description:</label>
                <input type="text" v-model="form.description" required
                    class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-red-600" />
            </div>
            <div class="mb-4">
                <h3 class="text-lg font-semibold text-gray-600">Select Articles:</h3>
                <ul>
                    <li v-for="article in articles" :key="article.id" class="flex items-center mb-2">
                        <label class="flex items-center">
                            <input type="checkbox" :value="article.id" v-model="form.selectedArticles"
                                class="form-checkbox h-4 w-4 text-red-600 border-gray-300 rounded" />
                            <span class="ml-2 text-gray-600">{{ article.title }}</span>
                        </label>
                    </li>
                </ul>
            </div>
            <button type="submit"
                class="w-full bg-red-600 text-white p-2 rounded hover:bg-red-700 focus:outline-none focus:ring focus:ring-red-300">
                Save Collection
            </button>
        </form>
    </div>
</template>