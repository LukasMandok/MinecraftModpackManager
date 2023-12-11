// store/config.js
import { defineStore } from 'pinia'

export const useConfig = defineStore({
    id: 'config',

    state: () => ({
        apiBaseUrl: '',
        rateLimitKey: '',
        public: {
            apiBaseUrl: '',
            siteUrl: '',
            owner: '',
            slug: '',
            branch: '',
            hash: '',
        },
    }),

    actions: {
        async fetchConfig() {
            // Simulate fetching configuration from an API
            // Replace this with your actual logic to fetch runtime configuration
            await new Promise((resolve) => setTimeout(resolve, 1000))

            // Assign runtime configuration
            this.apiUrl = 'https://example.com/api'
            this.apiKey = 'your-api-key'
        },
    },

    // Lifecycle hook for fetching config on store creation
    onInit() {
        onMounted(() => {
            this.fetchConfig()
        })
    },
})
