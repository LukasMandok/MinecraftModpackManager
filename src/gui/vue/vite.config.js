import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'
import svgLoader from 'vite-svg-loader'

import AutoImport from 'unplugin-auto-import/vite'
// import Components from 'unplugin-vue-components/vite'


// import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    server: {
        host: 'localhost',
        port: 8000,
        strictPort: true,
        // TODO: remove the proxy again for production
        proxy: mode === 'development' ? {
            '/api': {
                target: 'http://localhost:8080', // was 8080 before
                // changeOrigin: true,
                // secure: false,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        } : undefined
    },
    plugins: [
        vue(),
        // alias({
        //     entries: [
        //         {
        //             find: '@',
        //             replacement: resolve(projectRootDir, 'src'),
        //         },
        //     ],
        // }),
        svgLoader({
            svgoConfig: {
                plugins: [
                    {
                        name: 'preset-default',
                        params: {
                            overrides: {
                                removeViewBox: false,
                            },
                        },
                    },
                ],
            },
        }),
        eslint(),

        AutoImport({
            // targets to transform
            include: [],
            imports: [
                'vue',
                'vue-router',
                {
                    // '@unhead/vue': [
                    //   'unheadVueComposablesImports',
                    // ],
                    // '@unhead/vue': ['useHead', 'useSeoMeta'],
                    // this should already be taken care of by the dirs option
                    // './src/stores/tags': ['useTags'],
                    // './src/stores/cosmetics': ['useCosmetics'],
                    // './src/stores/config': ['useConfig'], 
                },
            ],
            // dirs: [
            //     "src/composables",
            //     "src/stores",
            // ],
            dts: false, // Disable auto ts support
            eslintrc: {
                enabled: true, // Default `false`
                filepath: './.eslintrc-auto-import.json', // Default `./.eslintrc-auto-import.json`
                globalsPropValue: true, // Default `true`, (true | false | 'readonly' | 'readable' | 'writable' | 'writeable')
            },
        }),

        // Components({
        //     dirs: ["src/components", "src/assets/icons"],
        //     extensions: ['vue'],
        //     deep: true,
        //     dts: false,
        // }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
            '~': fileURLToPath(new URL('.', import.meta.url))
        }
    },
    assetsSubDirectory: 'static',
    base: '/static/',
    build: {
        outDir: "../web",
        emptyOutDir: true
    }
}))