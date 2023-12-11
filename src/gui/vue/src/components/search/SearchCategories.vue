/**
* From the Modrinth Knossos project
* The AGPL-3.0 License
* Copyright (c) 2023 The Modrinth Knossos Authors
* https://github.com/modrinth/knossos/blob/undefined/components/ui/search/Categories.vue
* Modified script to use Vue 3 composition API
*/

<template>
	<div class="categories">
		<slot />
		<span
			v-for="category in categoriesFiltered"
			:key="category.name"
			v-html="category.icon + $formatCategory(category.name)"
		/>
	</div>
</template>

<script setup>
	// import { computed } from 'vue'
	
	// import { useTags } from './stores/tags'

	const props = defineProps({
		categories: {
			type: Array,
			default() {
				return []
			},
		},
		type: {
			type: String,
			required: true,
		},
	})

	const tags = useTags()

	const categoriesFiltered = computed(() => {
		return tags.categories
			.concat(tags.loaders)
			.filter((x) =>
				props.categories.includes(x.name) && 
				(!x.project_type || x.project_type === props.type)
			)	
	})

</script>

<style lang="scss" scoped>

	.categories {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;

		:deep(span) {
			display: flex;
			align-items: center;
			flex-direction: row;

			&:not(:last-child) {
				margin-right: var(--spacing-card-md);
			}

			&:not(.badge) {
				color: var(--color-icon);
				margin-right: var(--spacing-card-sm);
			}

			svg {
				width: 1rem;
				margin-right: 0.2rem;
			}
		}
	}
</style>