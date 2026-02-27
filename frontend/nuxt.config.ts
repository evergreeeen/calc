export default defineNuxtConfig({
  ssr: false,

  app: {
    head: {
      htmlAttrs: { lang: 'ru' },
      title: 'Калькулятор цен ЖК',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    },
  },

  css: ['~/assets/css/main.css'],

  nitro: {
    devProxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
    },
  },

  compatibilityDate: '2025-01-01',
})
