<script setup>
import { defineProps, onMounted, reactive } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';
import ArticleListing from './ArticleListing.vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';


const state = reactive({
    articles: {},
    isLoading: true,
});


const props = defineProps({
    limit: Number,

    showButton: {
        type: Boolean,
        default: false
    },

    headingText: {
        type: String,
        default: 'Explore Articles'
    },    

    collectionID: String,


});



onMounted(async () => {
    if (props.collectionID === undefined) {
        try {
            const response = await axios.get('/api/articles');
            state.articles = response.data.articles;
        } catch (error) {
            console.error('Error fetching articles', error);
        } finally {
            state.isLoading = false;
        }
    } else {
        try {
            const response = await axios.get(`/api/collections/${props.collectionID}`);
            const articleIDs = response.data.collection.article_ids;
            state.articles = await Promise.all(articleIDs.map(async (articleID) => {
                const response = await axios.get(`/api/articles/${articleID}`);
                return response.data.article
            }
            ));

        } catch (error) {
            console.error('Error fetching articles', error);
        } finally {
            state.isLoading = false;
        }
    }
})

</script>

<template>
    <!-- Article Listings -->
    <!-- to go through the elements of article in a specific order the key is mandatory! -->

    <section class="bg-blue-50 px-4 py-10">
        <div class="container-xl lg:container m-auto">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
                {{ props.headingText }}
            </h2>
            <!-- Show loading spinner when it is loading -->
            <div v-if="state.isLoading" class=" text-center text-gray-500 py-6">
                <PulseLoader />
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <ArticleListing v-for="article in state.articles.slice(0, props.limit || state.articles.length)"
                    :key="article.id" :article="article" />

            </div>
        </div>
    </section>

    <section v-if="props.showButton" class="m-auto max-w-lg my-10 px-6">
        <RouterLink to="/articles"
            class="block bg-gray-800 text-white text-center py-4 px-6 rounded-xl hover:bg-gray-700">View All Articles
        </RouterLink>
    </section>
</template>
