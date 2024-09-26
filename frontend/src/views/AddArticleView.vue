<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import router from '@/router';
import { useToast } from 'vue-toastification';
const form = reactive({
    title: '',
    content: '',
    author: ''
});

const toast = useToast();
const handleSubmit = async () => {

    const newArticle = {
        title: form.title,
        content: form.content,
        author: form.author
    }

    try {
        const response = await axios.post('/api/articles', newArticle);
        toast.success('Article added sucessfully');
        router.push(`/articles/${response.data.id}`);
    } catch (error) {
        console.error('Error fetching articles', error);
        toast.error('Article was not added');
    }
};

</script>

<template>
    <section class="bg-white">
        <div class="container m-auto max-w-2xl py-24">
            <div class="bg-white px-6 py-8 mb-4 shadow-md rounded-md border m-4 md:m-0">
                <form @submit.prevent="handleSubmit">
                    <h2 class="text-3xl text-center font-semibold mb-6">Add Article</h2>


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
                            Add Job
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </section>

</template>