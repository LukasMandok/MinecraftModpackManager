<template>
    some text before the wrapper

    <button @click="sendMessage">Send Message</button>

    <!-- <DefaultWrapper>
        <template #main>
            SOme text for the main slog
            <HelloWorld msg="Hello Vue 3 + Vite" />
        </template>

        some text inside the wrapper
        <TheWelcome />

    </DefaultWrapper> -->
</template>

<script setup>
    // import websockethandler from @/helpers/websockets.js
    import {onMounted} from 'vue'
    import { WebSocketHandler } from './helpers/websockets';

    let wsHandler = null

    onMounted(() => {
        wsHandler = new WebSocketHandler('', onMessage)
    })

    const sendMessage = () => {
        wsHandler.send( {type: 'test', content: 'test'} )
    }

    const onMessage = (data) => {
        console.log(data)
    }

    // import HelloWorld from '@/components/HelloWorld.vue'
    // import DefaultWrapper from '@/components/layout/DefaultWrapper.vue'
</script>

<style scoped>
    header {
        line-height: 1.5;
        max-height: 100vh;
    }

    .logo {
        display: block;
        margin: 0 auto 2rem;
    }

    nav {
        width: 100%;
        font-size: 12px;
        text-align: center;
        margin-top: 2rem;
    }

    nav a.router-link-exact-active {
        color: var(--color-text);
    }

    nav a.router-link-exact-active:hover {
        background-color: transparent;
    }

    nav a {
        display: inline-block;
        padding: 0 1rem;
        border-left: 1px solid var(--color-border);
    }

    nav a:first-of-type {
        border: 0;
    }

    @media (min-width: 1024px) {
        header {
            display: flex;
            place-items: center;
            padding-right: calc(var(--section-gap) / 2);
        }

        .logo {
            margin: 0 2rem 0 0;
        }

        header .wrapper {
            display: flex;
            place-items: flex-start;
            flex-wrap: wrap;
        }

        nav {
            text-align: left;
            margin-left: -1rem;
            font-size: 1rem;

            padding: 1rem 0;
            margin-top: 1rem;
        }
    }
</style>
