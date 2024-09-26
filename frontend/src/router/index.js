import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ArticlesView from '@/views/ArticlesView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import ArticleView from '@/views/ArticleView.vue'
import AddArticleView from '@/views/AddArticleView.vue'
import EditArticleView from '@/views/EditArticleView.vue'
import AddCollectionView from '@/views/AddCollectionView.vue'
import EditCollectionView from '@/views/EditCollectionView.vue'
import CollectionView from '@/views/CollectionView.vue'
import CollectionsView from '@/views/CollectionsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticlesView
    },
    {
      path: '/articles/:id',
      name: 'article',
      component: ArticleView
    },
    {
      path: '/articles/edit/:id',
      name: 'edit-article',
      component: EditArticleView
    },
    {
      path: '/articles/add',
      name: 'add-article',
      component: AddArticleView
    },
    {
      path: '/collections',
      name: 'collections',
      component: CollectionsView
    },
    {
      path: '/collections/:id',
      name: 'collection',
      component: CollectionView
    },
    {
      path: '/collections/add',
      name: 'add-collection',
      component: AddCollectionView
    },
    {
      path: '/collections/edit/:id',
      name: 'edit-collection',
      component: EditCollectionView
    },    
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView
    }
  ]
})

export default router
