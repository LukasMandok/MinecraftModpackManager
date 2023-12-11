<template>
    <nav class="navigation">
        <RouterLink
v-for="(link, index) in filteredLinks" v-show="link.shown === undefined ? true : link.shown"
            :key="index" :ref="setLinkElement" :to="query ? (link.href ? `?${query}=${link.href}` : '?') : link.href"
            class="nav-link button-animation">
            <span>{{ link.label }}</span>
        </RouterLink>
        <div
class="nav-indicator" :style="{
            left: positionToMoveX,
            top: positionToMoveY,
            width: sliderWidth,
            opacity: activeIndex === -1 ? 0 : 1,
        }" aria-hidden="true"></div>
    </nav>
</template>

<script setup>
    const props = defineProps({
        links: {
            default: () => [],
            type: Array,
        },
        query: {
            default: null,
            type: String,
        },
    })

    const route = useRoute()

    let sliderPositionX = ref(0)
    let sliderPositionY = ref(18)
    let selectedElementWidth = ref(0)
    let activeIndex = ref(-1)
    let oldIndex = ref(-1)
    let linkElements = ref([])


    const filteredLinks = computed(() => props.links.filter((x) => (x.shown === undefined ? true : x.shown)))
    const positionToMoveX = computed(() => `${sliderPositionX.value}px`)
    const positionToMoveY = computed(() => `${sliderPositionY.value}px`)
    const sliderWidth = computed(() => `${selectedElementWidth.value}px`)


    const pickLink = () => {
        activeIndex.value = props.query
            ? filteredLinks.value.findIndex(
                (x) => (x.href === '' ? undefined : x.href) === route.path[props.query]
            )
            : filteredLinks.value.findIndex((x) => x.href === decodeURIComponent(route.path))

        if (activeIndex.value !== -1) {
            startAnimation()
        } else {
            oldIndex.value = -1
            sliderPositionX.value = 0
            selectedElementWidth.value = 0
        }
    }

    const startAnimation = () => {
        const el = linkElements.value[activeIndex.value] //.$el

        sliderPositionX.value = el.offsetLeft
        sliderPositionY.value = el.offsetTop + el.offsetHeight
        selectedElementWidth.value = el.offsetWidth
    }

    const setLinkElement = (el) => {
        if (el) {
            linkElements.value.push(el)
        }
    }

    watch(() => route.path, pickLink)
    watch(() => route.query, () => {
        if (props.query) pickLink()
    })

    onMounted(() => {
        window.addEventListener('resize', pickLink)
        pickLink()
    })

    onUnmounted(() => {
        window.removeEventListener('resize', pickLink)
    })
</script>

<style lang="scss" scoped>
    .navigation {
        display: flex;
        flex-direction: row;
        align-items: center;
        grid-gap: 1rem;
        flex-wrap: wrap;
        position: relative;

        .nav-link {
            text-transform: capitalize;
            font-weight: var(--font-weight-bold);
            color: var(--color-text);
            position: relative;

            &:hover {
                color: var(--color-text);

                &::after {
                    opacity: 0.4;
                }
            }

            &:active::after {
                opacity: 0.2;
            }

            &.router-link-exact-active {
                color: var(--color-text);

                &::after {
                    opacity: 1;
                }
            }
        }

        &.use-animation {
            .nav-link {
                &.is-active::after {
                    opacity: 0;
                }
            }
        }

        .nav-indicator {
            position: absolute;
            height: 0.25rem;
            bottom: -5px;
            left: 0;
            width: 3rem;
            transition: all ease-in-out 0.2s;
            border-radius: var(--size-rounded-max);
            background-color: var(--color-brand);

            @media (prefers-reduced-motion) {
                transition: none !important;
            }
        }
    }
</style>
