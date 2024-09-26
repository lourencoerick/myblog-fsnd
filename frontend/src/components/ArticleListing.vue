<script setup>
import { defineProps, ref, computed } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
    article: Object
});

const showFullContent = ref(false);
const toggleFullContent = () => {
    showFullContent.value = !showFullContent.value
}
const truncatedContent = computed(() => {
    let content = props.article.content;

    if (!showFullContent.value) {
        content = content.slice(0, 50) + '...';
    }
    return content;
});
</script>

<template>

    <div class="bg-white rounded-xl shadow-md relative">
        <div class="p-4">
            <div class="mb-4">
                <h3 class="text-lg font-bold">{{ article.title }}</h3>
            </div>

            <div class="mb-5">
                <div>
                    {{ truncatedContent }}
                </div>
                <button @click="toggleFullContent" class="text-red-600 hover:text-red-500 mb-5">
                    {{ showFullContent ? 'Less' : 'More'}}

                </button>

            </div>

            <div class="border border-gray-100 mb-5"></div>

            <div class="flex flex-col lg:flex-row justify-between mb-4">
                <RouterLink :to="'/articles/' + article.id"
                    class="h-[36px] bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-lg text-center text-sm">
                    Read More
                </RouterLink>
            </div>
        </div>
    </div>
    
</template>
