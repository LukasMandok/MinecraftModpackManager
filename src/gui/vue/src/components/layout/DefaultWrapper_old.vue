<template>
    <div ref="main_page" class="layout" :class="{ 'expanded-mobile-nav': isBrowseMenuOpen }">
        <header class="site-header" role="presentation">
            <!-- Navigation Bar -->
            <section class="navbar columns" role="navigation">
                <!-- LOGO -->
                <section class="logo column" role="presentation">
                    <RouterLink class="button-base" to="/">
                        <!-- TODO: add real TextLogo -->
                        <!-- <BrandTextLogo class="text-logo" @click="developerModeIncrement()" /> -->
                        <IconCommunity class="text-logo" />
                    </RouterLink>
                </section>

                <!-- Navigation Buttons -->
                <section class="nav-group columns" role="presentation">
                    <section class="nav">
                        <NavRow class="navigation" :links="navRoutes" />
                    </section>
                    <section class="column-grow user-outer">
                        <section class="user-controls">
                            <!-- TODO:  Implement a own notification system-->
                            <router-link
to="/dashboard/notifications"
                                class="control-button button-transparent" title="Notifications">
                                <NotificationIcon />
                            </router-link>
                            <button class="control-button button-transparent" title="Switch theme" @click="changeTheme">
                                <MoonIcon v-if="theme.colorMode === 'light'" />
                                <SunIcon v-else />
                            </button>
                            <div
class="dropdown" :class="{ closed: !isDropdownOpen }" tabindex="0"
                                @mouseover="isDropdownOpen = true" @focus="isDropdownOpen = true"
                                @mouseleave="isDropdownOpen = false">
                                <div class="content card">
                                    <RouterLink class="item button-transparent" to="/dashboard/notifications">
                                        <NotificationIcon class="icon" />
                                        <span class="title">Notifications</span>
                                    </RouterLink>
                                    <hr class="divider" />
                                    <RouterLink class="item button-transparent" to="/dashboard">
                                        <ChartIcon class="icon" />
                                        <span class="title">Dashboard</span>
                                    </RouterLink>
                                    <RouterLink class="item button-transparent" to="/settings">
                                        <SettingsIcon class="icon" />
                                        <span class="title">Settings</span>
                                    </RouterLink>
                                </div>
                            </div>
                        </section>
                    </section>
                </section>
            </section>

            <!-- Mobile Navigation Bar -->
            <section class="mobile-navigation">
                <div
class="nav-menu nav-menu-browse" :class="{ expanded: isBrowseMenuOpen }"
                    @focusin="isBrowseMenuOpen = true" @focusout="isBrowseMenuOpen = false">
                    <div class="links cascade-links">
                        <RouterLink
v-for="navRoute in navRoutes" :key="navRoute.href" :to="navRoute.href"
                            class="iconified-button">
                            {{ navRoute.label }}
                        </RouterLink>
                    </div>
                </div>
                <div
class="nav-menu nav-menu-mobile" :class="{ expanded: isMobileMenuOpen }"
                    @focusin="isMobileMenuOpen = true" @focusout="isMobileMenuOpen = false">
                    <div class="links">
                        <RouterLink class="iconified-button" to="/settings">
                            <SettingsIcon />
                            Settings
                        </RouterLink>
                        <button class="iconified-button" @click="changeTheme">
                            <MoonIcon v-if="theme.colorMode === 'light'" class="icon" />
                            <SunIcon v-else class="icon" />
                            <span class="dropdown-item__text">Change theme</span>
                        </button>
                    </div>
                </div>
                <div class="mobile-navbar" :class="{ expanded: isBrowseMenuOpen || isMobileMenuOpen }">
                    <RouterLink to="/" class="tab button-animation" title="Home">
                        <HomeIcon />
                    </RouterLink>
                    <button
class="tab button-animation" :class="{ 'router-link-exact-active': isBrowseMenuOpen }"
                        title="Search" @click="toggleBrowseMenu()">
                        <div>
                            <SearchIcon class="smaller" />
                            Search
                        </div>
                    </button>
                    <div>
                        <RouterLink
to="/dashboard/notifications" class="tab button-animation" :class="{
                            'no-active': isMobileMenuOpen || isBrowseMenuOpen,
                                }" title="Notifications" @click="() => {
                                    isMobileMenuOpen = false
                                    isBrowseMenuOpen = false
                                }
                        ">
                            <NotificationIcon />
                        </RouterLink> 
                        <RouterLink to="/dashboard" class="tab button-animation" title="Dashboard">
                            <ChartIcon />
                        </RouterLink>
                    </div>
                    <button class="tab button-animation" title="Toggle Mobile Menu" @click="toggleMobileMenu()">
                        <div>
                            <HamburgerIcon v-if="!isMobileMenuOpen" />
                            <CrossIcon v-else />
                        </div>
                    </button>
                </div>
            </section>
        </header>

        <!-- Page Content -->
        <main>

            <slot name="main" />
            <slot>
                Here is some test space for additinoal content
            </slot>
        </main>

        <!-- Footer -->
        <footer>
            <div class="logo-info" role="region">
                <IconCommunity class="text-logo" />
                <!-- TODO: replace by actual text logo -->
                <!-- <BrandTextLogo class="text-logo" @click="developerModeIncrement()" /> -->
            </div>
            <div class="links links-1" role="region">
                <h4>Company</h4>
                <router-link to="/legal/terms"> Terms</router-link>
                <router-link to="/legal/privacy"> Privacy</router-link>
                <router-link to="/legal/rules"> Rules</router-link>
                <a :target="$external()" href="https://careers.modrinth.com">Careers <span class="count-bubble">1</span></a>
            </div>
            <div class="links links-2" role="region">
                <h4>Resources</h4>
                <a rel="noopener" :target="$external()" href="https://github.com/modrinth">GitHub</a>
            </div>
            <div class="links links-3" role="region">
                <h4>Interact</h4>
                <a rel="noopener" :target="$external()" href="https://discord.modrinth.com"> Discord </a>
            </div>
            <div class="buttons">
                <router-link class="btn btn-outline btn-primary" to="/app">
                    <DownloadIcon />
                    Get Modrinth App
                </router-link>
                <button class="iconified-button raised-button" @click="changeTheme">
                    <MoonIcon v-if="theme.colorMode === 'light'" />
                    <SunIcon v-else />
                    Change theme
                </button>
                <router-link class="iconified-button raised-button" to="/settings">
                    <SettingsIcon/>
                    Settings
                </router-link>
            </div>
            <div class="not-affiliated-notice">
                NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG.
            </div>  
        </footer>
    </div>
</template>


<script setup>
    // import { useRouter } from 'vue-router'
    // import { useTags, useCosmetics, useConfig } from '~/stores'
    // import { useHead } from '@unhead/vue'

    // import HamburgerIcon from '@/assets/icons/hamburger.svg'
    // import CrossIcon from '@/assets/icons/x.svg'
    // import SearchIcon from '@/assets/icons/search.svg'

    // import NotificationIcon from '@/assets/icons/notifications.svg'
    // import ModerationIcon from '~/assets/images/sidebar/admin.svg'
    // import HomeIcon from '@/assets/icons/home.svg'

    // import { MoonIcon, SunIcon, DownloadIcon, SettingsIcon } from '@/assets/icons'
    // import PlusIcon from '~/assets/images/utils/plus.svg'
    // import DropdownIcon from '@/assets/icons/dropdown.svg'
    // import LogOutIcon from '~/assets/images/utils/log-out.svg'
    // import HeartIcon from '@/assets/icons/heart.svg'
    // import ChartIcon from '@/assets/icons/chart.svg'

    // import NavRow from '@/components/ui/NavRow.vue'
    // import Avatar from '@/components/ui/Avatar.vue'

    const theme = useTheme()
    const date = useDate()

    const config = useConfig()
    const router = useRouter()
    const route = router.currentRoute.value

    const link = config.public.siteUrl + route.path.replace(/\/+$/, '')

    useHead({
        link: [
            {
                rel: 'canonical',
                href: link,
            },
        ],
    })

    const description =
        'Download Minecraft mods, plugins, datapacks, shaders, resourcepacks, and modpacks on Modrinth. ' +
        'Discover and publish projects on Modrinth with a modern, easy to use interface and API.'

    useSeoMeta({
        title: 'Modrinth',
        description,
        publisher: 'Modrinth',
        themeColor: [{ color: '#1bd96a' }],
        colorScheme: 'dark light',

        // OpenGraph
        ogTitle: 'Modrinth',
        ogSiteName: 'Modrinth',
        ogDescription: 'Discover and publish Minecraft content!',
        ogType: 'website',
        ogImage: 'https://cdn.modrinth.com/modrinth-new.png',
        ogUrl: link,

        // Twitter
        twitterCard: 'summary',
        twitterSite: '@modrinth',
    })

    // States
    const isDropdownOpen = ref(false)
    const isMobileMenuOpen = ref(false)
    const isBrowseMenuOpen = ref(false)
    // const registeredSkipLink = ref(null)
    // const hideDropdown = ref(false)

    // Routes ar probabily not needed
    const navRoutes = ref([
        { label: 'Mods', href: '/mods' },
        { label: 'Plugins', href: '/plugins' },
        { label: 'Data Packs', href: '/datapacks' },
        { label: 'Shaders', href: '/shaders' },
        { label: 'Resource Packs', href: '/resourcepacks' },
        { label: 'Modpacks', href: '/modpacks' },
    ])

    // const isOnSearchPage = computed(() => {
    //     return navRoutes.value.some(route => route.path.startsWith(route.href))
    // })

    watch(() => route.path, () => {
        isMobileMenuOpen.value = false
        isBrowseMenuOpen.value = false

        if (typeof window !== 'undefined') {
            document.body.style.overflowY = 'scroll'
            document.body.setAttribute('tabindex', '-1')
            document.body.removeAttribute('tabindex')
        }

        date.updateCurrentDate()
    })

    onMounted(() => {
        if (typeof window !== 'undefined') {
            window.history.scrollRestoration = 'auto'
        }

    })

    function toggleMobileMenu() {
        isMobileMenuOpen.value = !isMobileMenuOpen.value
        if (isMobileMenuOpen.value) {
            isBrowseMenuOpen.value = false
        }
    }

    function toggleBrowseMenu() {
        isBrowseMenuOpen.value = !isBrowseMenuOpen.value

        if (isBrowseMenuOpen.value) {
            isMobileMenuOpen.value = false
        }
    }

    function changeTheme() {
        // theme.updateTheme(theme.colorMode === 'dark' ? 'light' : 'dark', true)
        theme.updateTheme(null, true)
    }

</script>

<style lang="scss">
@import '@/assets/styles/global.scss';
// @import 'omorphia/dist/style.css'; 

.layout {
    min-height: 100vh;
    background-color: var(--color-bg);
    display: block;

    @media screen and (min-width: 1024px) {
        min-height: calc(100vh - var(--spacing-card-bg));
    }

    @media screen and (max-width: 750px) {
        margin-bottom: calc(var(--size-mobile-navbar-height) + 2rem);
    }

    .site-header {
        max-width: 100vw;

        @media screen and (min-width: 1024px) {
            margin-top: var(--spacing-card-md);
            margin-bottom: var(--spacing-card-md);
        }

        @media screen and (min-width: 1280px) {
            border-radius: var(--size-rounded-sm);
            max-width: 1280px;
            margin-left: auto;
            margin-right: auto;
        }

        .navbar {
            padding: 0 var(--spacing-card-lg);
            margin: 0 var(--spacing-card-lg);
            max-width: 1280px;
            margin-left: auto;
            margin-right: auto;

            section.logo {
                display: flex;
                justify-content: space-between;
                color: var(--color-text-dark);
                z-index: 5;

                a {
                    align-items: center;
                    display: flex;
                }

                .small-logo {
                    display: block;
                }

                svg {
                    height: 1.75rem;
                    width: auto;
                }

                button {
                    background: none;
                    border: none;
                    margin: 0 0 0 0.5rem;
                    padding: 0;

                    svg {
                        height: 1.5rem;
                        width: 1.5rem;
                    }
                }
            }

            section.nav-group {
                display: flex;
                flex-grow: 5;
                z-index: 5;

                section.nav {
                    flex-grow: 5;

                    .navigation {
                        display: flex;
                        width: fit-content;
                        position: relative;
                        top: 50%;
                        transform: translateY(-50%);
                        margin-left: 2rem;
                        grid-gap: 1.5rem;

                        a {
                            margin-left: 0;
                            margin-right: auto;
                        }

                        a.tab {
                            padding: 0;
                            margin-right: 1rem;
                            display: flex;
                            align-items: flex-start;

                            &--alpha::after {
                                content: 'Alpha';
                                background-color: var(--color-warning-bg);
                                color: var(--color-warning-text);
                                border-radius: 1rem;
                                padding: 0.25rem 0.5rem;
                                margin-left: 0.4rem;
                                font-size: 0.7rem;
                            }
                        }
                    }
                }

                .user-outer {
                    z-index: 5;
                }

                section.user-controls {
                    align-items: center;
                    display: flex;
                    flex-direction: row;
                    justify-content: space-between;
                    position: relative;
                    top: 50%;
                    transform: translateY(-50%);
                    min-width: 6rem;
                    gap: 0.25rem;

                    .control-button {
                        position: relative;
                        display: flex;
                        padding: 0.5rem;
                        color: var(--color-text);
                        border-radius: 2rem;
                        transition: filter 0.1s ease-in-out;
                        border: 2px solid transparent;
                        box-sizing: border-box;

                        svg {
                            height: 1.25rem;
                            width: 1.25rem;
                        }

                        &.bubble {
                            &::after {
                                background-color: var(--color-brand);
                                border-radius: var(--size-rounded-max);
                                content: '';
                                height: 0.5rem;
                                position: absolute;
                                right: 0.25rem;
                                top: 0.5rem;
                                width: 0.5rem;
                            }
                        }

                        //&.router-link-exact-active {
                        //  color: var(--color-button-text-active);
                        //  background-color: var(--color-button-bg);
                        //}
                    }

                    .hide-desktop {
                        display: none;
                    }

                    .dropdown {
                        position: relative;
                        margin-left: 0.5rem;

                        .control {
                            align-items: center;
                            background: none;
                            display: flex;
                            justify-content: center;
                            padding: 0;

                            .user-icon {
                                height: 2rem;
                                width: 2rem;
                                outline: 2px solid var(--color-raised-bg);
                                transition: outline-color 0.1s ease-in-out;
                            }

                            .caret {
                                color: var(--color-button-text);
                                margin-left: 0.25rem;
                                width: 1rem;
                            }
                        }

                        .content {
                            border: 1px solid var(--color-divider-dark);
                            list-style: none;
                            margin: 0.5rem 0 0 0;
                            max-width: 25rem;
                            min-width: 12rem;
                            opacity: 0;
                            padding: 1rem;
                            position: absolute;
                            right: -1rem;
                            transform: scaleY(0.9);
                            transform-origin: top;
                            transition: all 0.1s ease-in-out 0.05s, color 0s ease-in-out 0s,
                                background-color 0s ease-in-out 0s, border-color 0s ease-in-out 0s;
                            visibility: hidden;
                            width: max-content;
                            z-index: 1;
                            box-shadow: var(--shadow-floating);

                            .divider {
                                background-color: var(--color-divider-dark);
                                border: none;
                                color: var(--color-divider-dark);
                                height: 1px;
                                margin: 0.5rem 0;
                            }

                            .item {
                                align-items: center;
                                border-radius: 0.5rem;
                                box-sizing: border-box;
                                color: inherit;
                                display: flex;
                                padding: 0.5rem 0.75rem;
                                width: 100%;

                                .icon {
                                    margin-right: 0.5rem;
                                    height: 20px;
                                    width: 20px;
                                }

                                &.router-link-exact-active {
                                    color: var(--color-button-text-active);
                                    background-color: var(--color-button-bg);

                                    &.primary-color {
                                        color: var(--color-button-text-active);
                                        background-color: var(--color-brand-highlight);
                                    }
                                }

                                &.primary-color {
                                    color: var(--color-brand);
                                }
                            }

                            .profile-link {
                                .prompt {
                                    margin-top: 0.25rem;
                                    color: var(--color-text-secondary);
                                }
                            }
                        }

                        @media screen and (max-width: 1300px) {
                            .content {
                                margin-right: 1rem;
                            }
                        }
                    }

                    .dropdown:hover .user-icon {
                        outline-color: var(--color-brand);
                    }

                    .dropdown:hover:not(.closed) .content,
                    .dropdown:focus:not(.closed) .content,
                    .dropdown:focus-within:not(.closed) .content {
                        opacity: 1;
                        transform: scaleY(1);
                        visibility: visible;
                    }
                }

                section.auth-prompt {
                    display: flex;
                    align-items: center;
                    height: 100%;
                    margin: 0;
                    gap: 0.5rem;

                    .log-in-button {
                        margin: 0 auto;
                    }
                }
            }

            @media screen and (max-width: 1095px) {
                display: none;
            }
        }

        .mobile-navigation {
            display: none;

            .nav-menu {
                width: 100%;
                position: fixed;
                bottom: calc(var(--size-mobile-navbar-height) - var(--size-rounded-card));
                padding-bottom: var(--size-rounded-card);
                left: 0;
                background-color: var(--color-raised-bg);
                z-index: 6;
                transform: translateY(100%);
                transition: transform 0.4s cubic-bezier(0.54, 0.84, 0.42, 1);
                border-radius: var(--size-rounded-card) var(--size-rounded-card) 0 0;
                box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0);

                .links,
                .account-container {
                    display: grid;
                    grid-template-columns: repeat(1, 1fr);
                    grid-gap: 1rem;
                    justify-content: center;
                    padding: 1rem;

                    .iconified-button {
                        width: 100%;
                        max-width: 500px;
                        padding: 0.75rem;
                        justify-content: center;
                        font-weight: 600;
                        font-size: 1rem;
                        margin: 0 auto;
                    }
                }

                .cascade-links {
                    @media screen and (min-width: 354px) {
                        grid-template-columns: repeat(2, 1fr);
                    }

                    @media screen and (min-width: 674px) {
                        grid-template-columns: repeat(3, 1fr);
                    }
                }

                &-browse {
                    &.expanded {
                        transform: translateY(0);
                        box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.3);
                    }
                }

                &-mobile {
                    .account-container {
                        padding-bottom: 0;

                        .account-button {
                            padding: var(--spacing-card-md);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 0.5rem;

                            .user-icon {
                                width: 2.25rem;
                                height: 2.25rem;
                            }

                            .account-text {
                                flex-grow: 0;
                            }
                        }
                    }

                    &.expanded {
                        transform: translateY(0);
                        box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.3);
                    }
                }
            }

            .mobile-navbar {
                display: flex;
                height: calc(var(--size-mobile-navbar-height) + env(safe-area-inset-bottom));
                border-radius: var(--size-rounded-card) var(--size-rounded-card) 0 0;
                padding-bottom: env(safe-area-inset-bottom);
                position: fixed;
                left: 0;
                bottom: 0;
                background-color: var(--color-raised-bg);
                box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.3);
                z-index: 7;
                width: 100%;
                align-items: center;
                justify-content: space-between;
                transition: border-radius 0.3s ease-out;
                border-top: 2px solid rgba(0, 0, 0, 0);
                box-sizing: border-box;

                &.expanded {
                    box-shadow: none;
                    border-radius: 0;
                }

                .tab {
                    position: relative;
                    background: none;
                    display: flex;
                    flex-basis: 0;
                    justify-content: center;
                    align-items: center;
                    flex-direction: row;
                    gap: 0.25rem;
                    font-weight: bold;
                    padding: 0;
                    transition: color ease-in-out 0.15s;
                    color: var(--color-text-inactive);
                    text-align: center;

                    &.browse {
                        svg {
                            transform: rotate(180deg);
                            transition: transform ease-in-out 0.3s;

                            &.closed {
                                transform: rotate(0deg);
                            }
                        }
                    }

                    &.bubble {
                        &::after {
                            background-color: var(--color-brand);
                            border-radius: var(--size-rounded-max);
                            content: '';
                            height: 0.5rem;
                            position: absolute;
                            left: 1.5rem;
                            top: 0;
                            width: 0.5rem;
                        }
                    }

                    svg {
                        height: 1.75rem;
                        width: 1.75rem;

                        &.smaller {
                            width: 1.25rem;
                            height: 1.25rem;
                        }
                    }

                    .user-icon {
                        width: 2rem;
                        height: 2rem;
                        transition: border ease-in-out 0.15s;
                        border: 0 solid var(--color-brand);
                        box-sizing: border-box;

                        &.expanded {
                            border: 2px solid var(--color-brand);
                        }
                    }

                    &:hover,
                    &:focus {
                        color: var(--color-text);
                    }

                    &:first-child {
                        margin-left: 2rem;
                    }

                    &:last-child {
                        margin-right: 2rem;
                    }

                    &.router-link-exact-active:not(&.no-active) {
                        svg {
                            color: var(--color-brand);
                        }

                        color: var(--color-brand);
                    }
                }
            }

            @media screen and (max-width: 1095px) {
                display: flex;
            }
        }

        div {
            flex-grow: 1;
            justify-content: end;
            align-items: center;
            row-gap: 1rem;
        }

        &.active {
            display: flex;

            @media screen and (min-width: 1095px) {
                display: none;
            }
        }
    }

    main {
        grid-area: main;
    }

    footer {
        margin: 6rem 0 2rem 0;
        text-align: center;
        display: grid;
        grid-template:
            'logo-info  logo-info  logo-info' auto
            'links-1    links-2    links-3' auto
            'buttons    buttons    buttons' auto
            'notice     notice     notice' auto
            / 1fr 1fr 1fr;
        max-width: 1280px;

        .logo-info {
            margin-left: auto;
            margin-right: auto;
            max-width: 15rem;
            margin-bottom: 1rem;
            grid-area: logo-info;

            .text-logo {
                width: 10rem;
                height: auto;
            }
        }

        .links {
            display: flex;
            flex-direction: column;
            margin-bottom: 1rem;

            h4 {
                color: var(--color-text-dark);
                margin: 0 0 1rem 0;
            }

            a {
                margin: 0 0 1rem 0;
            }

            &.links-1 {
                grid-area: links-1;
            }

            &.links-2 {
                grid-area: links-2;
            }

            &.links-3 {
                grid-area: links-3;
            }

            .count-bubble {
                font-size: 1rem;
                border-radius: 5rem;
                background: var(--color-brand);
                color: var(--color-text-inverted);
                padding: 0 0.35rem;
                margin-left: 0.25rem;
            }
        }

        .buttons {
            margin-left: auto;
            margin-right: auto;
            grid-area: buttons;

            button,
            a {
                margin-bottom: 0.5rem;
                margin-left: auto;
                margin-right: auto;
            }
        }

        .not-affiliated-notice {
            grid-area: notice;
            font-size: var(--font-size-xs);
            text-align: center;
            font-weight: 500;
            margin-top: var(--spacing-card-md);
        }

        @media screen and (min-width: 1024px) {
            display: grid;
            margin-inline: auto;
            grid-template:
                'logo-info  links-1 links-2 links-3 buttons' auto
                'notice     notice  notice  notice  notice' auto;
            text-align: unset;

            .logo-info {
                margin-right: 4rem;
            }

            .links {
                margin-right: 4rem;
            }

            .buttons {
                width: unset;
                margin-left: 0;

                button,
                a {
                    margin-right: unset;
                }
            }

            .not-affiliated-notice {
                margin-top: 0;
            }
        }
    }
}

@media (min-width: 1024px) {
    .layout {
        main {
            .alpha-alert {
                margin: 1rem;

                .wrapper {
                    padding: 1rem 2rem 1rem 1rem;
                }
            }
        }
    }
}

.email-nag {
    background-color: var(--color-raised-bg);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 0.5rem 1rem;
}

@media (max-width: 1200px) {
    .app-btn {
        display: none;
    }
}
</style>
<style src="~/node_modules/vue-multiselect/dist/vue-multiselect.min.css"></style>