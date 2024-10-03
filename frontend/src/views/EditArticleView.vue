<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import router from '@/router';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useAuth0 } from '@auth0/auth0-vue';

const { getAccessTokenSilently } = useAuth0();
const form = reactive({
    title: '',
    content: '',
    author: ''
});

const route = useRoute();

const articleId = route.params.id
const toast = useToast();
const handleSubmit = async () => {
    const token = await getAccessTokenSilently();

    const updatedArticle = {
        id: articleId,
        title: form.title,
        content: form.content,
        author: form.author
    }


    try {
        const response = await axios.patch(`${import.meta.env.VITE_API_ENDPOINT}/api/articles/${articleId}`, updatedArticle,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        toast.success('Article updated sucessfully');
        router.push(`/articles/${response.data.id}`);
    } catch (error) {
        console.error('Error fetching articles', error);
        toast.error('Article was not updated');
    }
};

const state = reactive({
    article: {},
    isLoading: true
});

onMounted(async () => {
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_ENDPOINT}/api/articles/${articleId}`)
        state.article = response.data.article;
        // populate inputs
        form.title = state.article.title;
        form.content = state.article.content;
        form.author = state.article.author;


    } catch (error) {
        console.error('Error fetching article', error)
    } finally {
        state.isLoading = false;
    }

});
</script>

<template>
    <section class="bg-white">
        <div class="container m-auto max-w-2xl py-24">
            <div class="bg-white px-6 py-8 mb-4 shadow-md rounded-md border m-4 md:m-0">
                <form @submit.prevent="handleSubmit">
                    <h2 class="text-3xl text-center font-semibold mb-6">Edit Article</h2>


                    <div class="mb-4">
                        <label class="block text-gray-700 font-bold mb-2">Article Title</label>
                        <input type="text" v-model="form.title" id="title" name="title"
                            class="border rounded w-full py-2 px-3 mb-2" placeholder="eg. My Perfect Text about Birds"
                            required />
                    </div>
                    <div class="mb-4">
                        <label for="content" class="block text-gray-700 font-bold mb-2">Content</label>
                        <textarea id="content" v-model="form.content" name="content"
                            class="border rounded w-full py-2 px-3" rows="4" placeholder="Add article content here!"
                            required></textarea>
                    </div>

                    <h3 class="text-2xl mb-5">Author Info</h3>

                    <div class="mb-4">
                        <label for="author" class="block text-gray-700 font-bold mb-2">Author Name</label>
                        <input type="text" v-model="form.author" id="author" name="author"
                            class="border rounded w-full py-2 px-3" placeholder="Author Name" required />
                    </div>


                    <div>
                        <button
                            class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline"
                            type="submit">
                            Update Article
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </section>

</template>