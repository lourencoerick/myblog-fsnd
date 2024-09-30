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
      domain: 'dev-u87omsusx1w1jtso.us.auth0.com',
      clientId: 'E8xpUla9GyHNYXoK6xgRcJ9edApb32dl',
      authorizationParams: {
        redirect_uri: window.location.origin,
        audience: 'my-blog',
        response_type: 'token'
      }
    })
  )

// https://dev-u87omsusx1w1jtso.us.auth0.com/authorize?audience=my-blog&response_type=token&client_id=E8xpUla9GyHNYXoK6xgRcJ9edApb32dl&redirect_uri=http://localhost:3000
app.mount('#app')
