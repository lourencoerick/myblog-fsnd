import './style.css'
import 'primeicons/primeicons.css'
import 'vue-toastification/dist/index.css'
import { createAuth0 } from '@auth0/auth0-vue'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'

const app = createApp(App)

app
  .use(router)
  .use(Toast)
  .use(
    createAuth0({
      domain: import.meta.env.VITE_AUTH0_DOMAIN,
      clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
      authorizationParams: {
        redirect_uri: window.location.origin,
        audience: import.meta.env.VITE_AUTH0_AUDIENCE,
        response_type: 'token'
      }
    })
  )

app.mount('#app')
