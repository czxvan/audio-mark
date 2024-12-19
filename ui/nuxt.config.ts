// https://nuxt.com/docs/api/configuration/nuxt-config
import Theme from '@primevue/themes/aura';

export default defineNuxtConfig({
    compatibilityDate: '2024-04-03',
    devtools: {enabled: true},
    modules: ['@primevue/nuxt-module', '@nuxtjs/tailwindcss', '@nuxt/eslint'],
    css: [
        '@/assets/styles.scss'
    ],
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {}
        }
    },
    primevue: {
        options: {
            ripple: true,
            theme: {
                preset: Theme,
                options: {
                    darkModeSelector: '.app-dark'
                }
            }
        }
    },
    plugins: ['~/plugins/primevue.js'],
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    quietDeps: true,
                    silenceDeprecations: ['legacy-js-api'],
                }
            }
        }
    },
    runtimeConfig: {
        public: {
            API_URL: process.env.API_URL || 'http://10.108.25.241:8910'
        }
    },
    app: {
        keepalive: true
    },
})