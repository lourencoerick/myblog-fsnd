<script setup>
import { defineProps, ref, computed } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
    collection: Object
});

const showFullDescription = ref(false);
const toggleFullDescription = () => {
    showFullDescription.value = !showFullDescription.value
}
const truncatedDescription = computed(() => {
    let description = props.collection.description;

    if (!showFullDescription.value) {
        description = description.slice(0, 50) + '...';
    }
    return description;
});
</script>

<template>

    <div class="bg-white rounded-xl shadow-md relative">
        <div class="p-4">
            <div class="mb-4">
                <h3 class="text-lg font-bold">{{ collection.title }}</h3>
            </div>

            <div class="mb-5">
                <div>
                    {{ truncatedDescription }}
                </div>
                <button @click="toggleFullDescription" class="text-red-600 hover:text-red-500 mb-5">
                    {{ showFullDescription ? 'Less' : 'More'}}

                </button>

            </div>

            <div class="border border-gray-100 mb-5"></div>

            <div class="flex flex-col lg:flex-row justify-between mb-4">
                <RouterLink :to="'/collections/' + collection.id"
                    class="h-[36px] bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-lg text-center text-sm">
                    See all articles about 
                </RouterLink>
            </div>
        </div>
    </div>
    
</template>
