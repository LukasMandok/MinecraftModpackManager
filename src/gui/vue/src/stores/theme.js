import { defineStore } from 'pinia'
import { useCookie } from "@vue-composable/cookie";

export const useTheme = defineStore({
    id: 'theme',

    state: () => {
        // Convert to eel commands to get the default values.
        const colorModeCookie = useCookie('color-mode', {
            maxAge: 60 * 60 * 24 * 365 * 10,
            sameSite: 'lax',
            secure: true,
            httpOnly: false,
            path: '/',
        })

        let colorMode = colorModeCookie.value

        if (!colorMode) {
            colorMode = {
                value: 'dark',
                preference: 'system',
            }
        }

        if (colorMode.preference !== 'system') {
            colorMode.value = colorMode.preference
        }

        return colorMode
    },

    getters: {
        colorMode() {
            return this.value;
        },
    },

    actions: {

        updateTheme(value, updatePreference = false) {
            const theme = useTheme()

            if (!value) {
                if (theme.value === 'dark') {
                    value = 'light'
                } else if (theme.value === 'light') {
                    value = 'dark'
                } else {
                    value = 'system'
                }
            }

            if (value === 'system') {
                theme.preference = 'system'

                const colorSchemeQueryList = window.matchMedia('(prefers-color-scheme: light)')
                if (colorSchemeQueryList.matches) {
                    theme.value = 'light'
                } else {
                    theme.value = 'dark'
                }
            } else {
                theme.value = value
                if (updatePreference) theme.preference = value
            }

            if (typeof window !== 'undefined') {
                document.documentElement.className = `${theme.value}-mode`
            }

            const themeCookie = useCookie('color-mode', {
                maxAge: 60 * 60 * 24 * 365 * 10,
                sameSite: 'lax',
                secure: true,
                httpOnly: false,
                path: '/',
            })

            themeCookie.value = theme
        },
    },
})
