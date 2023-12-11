// import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@unhead/vue'

import App from './App.vue'
import router from './router'

import Utilities from './utility'

const app = createApp(App)
const pinia = createPinia()
const head = createHead()

// app.config.devtools = true

app.use(Utilities)
app.use(router)
app.use(pinia)
app.use(head)

console.log("mount app: ")
app.mount('#app')

/**------------------------------------------------------------------------
 *                           TODO
 *------------------------------------------------------------------------*/

/**
 * - Add a router link component, which can display the Curseforge and the modrinth link and allows you to choose, which link to follow
 * 
 * 
 * 
 */