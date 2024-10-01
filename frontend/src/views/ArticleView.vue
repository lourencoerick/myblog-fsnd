<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import router from '@/router';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import BackButton from '@/components/BackButton.vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { useAuth0 } from '@auth0/auth0-vue';

const { isAuthenticated, getAccessTokenSilently } = useAuth0();
const route = useRoute();
const toast = useToast();

const articleId = route.params.id;

const state = reactive({
    article: {},
    isLoading: true,
});

const deleteArticle = async () => {
    try {
        const confirm = window.confirm('Are you sure you want to delete this article?');
        const token = await getAccessTokenSilently();

        if (confirm) {
            await axios.delete(`/api/articles/${articleId}`,          {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            toast.success('Article deleted');
            router.push('/articles');
        }

    } catch (error) {
        console.error('Error fetching articles', error);
        toast.error('Article was not deleted');
    }
};

onMounted(async () => {
    try {
        const response = await axios.get(`/api/articles/${articleId}`);
        state.article = response.data.article;
    } catch (error) {
        console.error('Error fetching article', error);
        if (error.status === 404) {
            router.push("/not-found")
        }
    } finally {
        state.isLoading = false;
    }

})
</script>

<template>
    <!-- <BackButton /> -->
    <section v-if="!state.isLoading" class="bg-white">
        <BackButton />
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
                            {{ state.article.title }}
                        </h2>

                        <small class="text-gray-800 text-sm italic mb-6 block">
                            written by {{ state.article.author }}
                        </small>

                        <p class="mb-4">
                            {{ state.article.content }}
                        </p>
                    </div>
                </main>


                <!-- Sidebar -->
                <aside v-if="isAuthenticated">
                    <!-- Manage -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl font-bold mb-6">Manage Article</h3>
                        <RouterLink :to="`/articles/edit/${state.article.id}`"
                            class="bg-gray-500 hover:bg-gray-600 text-white text-center font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline mt-4 block">
                            Edit Article</RouterLink>
                        <button @click="deleteArticle"
                            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline mt-4 block">
                            Delete Article
                        </button>
                    </div>
                </aside>
            </div>
        </div>
    </section>

    <div v-else class="text-center text-gray-500 py-6">
        <PulseLoader />
    </div>

</template>