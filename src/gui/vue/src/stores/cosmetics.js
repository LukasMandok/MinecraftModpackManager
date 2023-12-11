import { defineStore } from 'pinia'
import { useCookie } from "@vue-composable/cookie";

export const useCosmetics = defineStore({
    id: "cosmetics",

    // state
    state: () => {
        const cosmetics = useCookie('cosmetics', {
            maxAge: 60 * 60 * 24 * 365 * 10,
            sameSite: 'lax',
            secure: true,
            httpOnly: false,
            path: '/',
        })

        if (!cosmetics.value) {
            cosmetics.value = {
                searchLayout: false,
                projectLayout: false,
                advancedRendering: true,
                externalLinksNewTab: true,
                developerMode: false,
                notUsingBlockers: false,
                hideModrinthAppPromos: false,
                searchDisplayMode: {
                    mod: 'list',
                    plugin: 'list',
                    resourcepack: 'gallery',
                    modpack: 'list',
                    shader: 'gallery',
                    datapack: 'list',
                    user: 'list',
                },
            }
        }

        return cosmetics.value
    },

    actions: {
        saveCosmetics() {
            const cosmetics = this.cosmetics

            const cosmeticsCookie = useCookie('cosmetics', {
                maxAge: 60 * 60 * 24 * 365 * 10,
                sameSite: 'lax',
                secure: true,
                httpOnly: false,
                path: '/',
            })

            cosmeticsCookie.value = cosmetics
        },
    },
})
