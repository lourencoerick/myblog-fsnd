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
import { useAuth0 } from '@auth0/auth0-vue'

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
      component: EditArticleView,
      meta: { requiresAuth: true }
    },
    {
      path: '/articles/add',
      name: 'add-article',
      component: AddArticleView,
      meta: { requiresAuth: true }
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
      component: AddCollectionView,
      meta: { requiresAuth: true }
    },
    {
      path: '/collections/edit/:id',
      name: 'edit-collection',
      component: EditCollectionView,
      meta: { requiresAuth: true }
    },        
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView
    }
  ]
});

router.beforeEach((to, from, next) => {
  const { isAuthenticated, loginWithRedirect } = useAuth0();

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isAuthenticated.value) {
      localStorage.setItem('redirectTo', to.fullPath);
      loginWithRedirect();
    }
  }
  next(); 
});

export default router
