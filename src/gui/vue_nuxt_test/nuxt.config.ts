// https://nuxt.com/docs/api/configuration/nuxt-config
import { fileURLToPath, URL } from 'node:url'

export default defineNuxtConfig({
  // devtools: { enabled: true },
  buildDir: "../web",
  devServer: {
    port: 3000
  },

  app: {
    head: {
      title: 'Minecraft Modpack Manager',
      script: [
        { src: 'http://localhost:3000/eel.js' },
        { src: './publlic/eel.js', type: 'module' },
      ],
    },
    baseURL: "/",
  },

  // alias: {
  //   '@': fileURLToPath(new URL('./src', import.meta.url))
  // },

  vite: {
    build: {
      emptyOutDir: true
    } 
  }
})
