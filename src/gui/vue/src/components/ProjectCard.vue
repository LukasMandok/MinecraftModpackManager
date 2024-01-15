/**
* From the Modrinth Knossos project
* The AGPL-3.0 License
* Copyright (c) 2023 The Modrinth Knossos Authors
* https://github.com/modrinth/knossos/blob/undefined/components/ui/ProjectCard.vue
* Modified template and script to use Vue 3 composition API and work with this project
*/

<template>
	<article class="project-card base-card padding-bg equalize" role="listitem">
		<!-- Project Icon -->
		<router-link :title="name" class="icon" tabindex="-1" :to="link">
			<Avatar :src="iconUrl" :alt="name" size="md" no-shadow loading="lazy" />
		</router-link>

		<!-- Project Image -->
		<router-link
class="gallery" :class="{ 'no-image': !featuredImage }" tabindex="-1"
			:to="link" :style="color ? `background-color: ${toColor};` : ''">
			<img v-if="featuredImage" :src="featuredImage" alt="gallery image" loading="lazy" />
		</router-link>

		<!-- Project Title -->
		<div class="title">
			<router-link :to="link">
				<h2 class="name">
					{{ name }}
				</h2>
			</router-link>
			<p v-if="author" class="author">
				by
				<router-link :to="authorLink">
					{{ author }}
				</router-link>
			</p>
		</div>

		<!-- Project Description -->
		<p class="description">
			{{ description }}
		</p>

		<!-- Categories -->
		<div class="tags categories" :type="type">
			<Categories type="source" :categories="sources" class="scope">
				Available on:
			</Categories>
			<Categories type="loader" :categories="loaders">
				Loaders:
			</Categories>
			<span>Version: {{recent_version }}</span>
		</div>

		<!-- Stats -->
		<div class="stats">
			<div v-if="downloads" class="stat">
				<DownloadIcon aria-hidden="true" />
				<p>
					<strong>{{ $formatNumber(downloads) }}</strong>
					<span class="stat-label"> downloads</span>
				</p>
			</div>

			<div v-tooltip="$dayjs(updated).format('MMMM D, YYYY [at] h:mm A')" class="stat date">
				<EditIcon aria-hidden="true"/>
				<span class="stat-label">Updated </span>
			</div>
		</div>
	</article>
</template>

<script setup>
	// import { computed } from 'vue'

	// import { useTags } from './stores/tags'

	// Components
	// import Categories from '~/components/Categories.vue'
	// import Avatar from '~/components/Avatar.vue'

	// import EditIcon from '~/assets/icons/updated.svg'
	// import DownloadIcon from '~/assets/icons/download.svg'

	const props = defineProps({
		type: {
			type: String,
			default: 'mod'
		},
		name: {
			type: String,
			required: true
		},
		author: {
			type: String,
			default: null
		},
		description: {
			type: String,
			default: null
		},

		link: {
			type: String,
			required: true
		},
		authorLink: {
			type: String,
			default: null
		},
		iconUrl: {
			type: String,
			default: '#',
		},

		featuredImage: {
			type: String,
			default: null
		},

		sources: {
			type: Array,
			default: () => []
		},
		loaders: {
			type: Array,
			default: () => []
		},
		recentVersion: {
			type: String,
			default: null
		},

		downloads: {
			type: Number,
			default: null
		},
		updated: {
			type: String,
			default: null
		},

		color: {
			type: Number,
			default: null
		}
	})

	// const tags = useTags()

	const toColor = computed(() => {
		let color = props.color

		color >>>= 0
		const b = color & 0xff
		const g = (color & 0xff00) >>> 8
		const r = (color & 0xff0000) >>> 16
		return 'rgba(' + [r, g, b, 1].join(',') + ')'
	})

	// CHECKME: what about getProjectTypeForDisplay? Do I need this for anything?

</script>

<style lang="scss" scoped>
.project-card {
	display: inline-grid;
	box-sizing: border-box;
	overflow: hidden;
	margin: 0;
}

.display-mode--list .project-card {
	grid-template:
		'icon title stats'
		'icon description stats'
		'icon tags stats';
	grid-template-columns: min-content 1fr auto;
	grid-template-rows: min-content 1fr min-content;
	column-gap: var(--spacing-card-md);
	row-gap: var(--spacing-card-sm);
	width: 100%;

	@media screen and (max-width: 750px) {
		grid-template:
			'icon title'
			'icon description'
			'icon tags'
			'stats stats';
		grid-template-columns: min-content auto;
		grid-template-rows: min-content 1fr min-content min-content;
	}

	@media screen and (max-width: 550px) {
		grid-template:
			'icon title'
			'icon description'
			'tags tags'
			'stats stats';
		grid-template-columns: min-content auto;
		grid-template-rows: min-content 1fr min-content min-content;
	}
}

.display-mode--gallery .project-card,
.display-mode--grid .project-card {
	padding: 0 0 var(--spacing-card-bg) 0;
	grid-template: 'gallery gallery' 'icon title' 'description  description' 'tags tags' 'stats stats';
	grid-template-columns: min-content 1fr;
	grid-template-rows: min-content min-content 1fr min-content min-content;
	row-gap: var(--spacing-card-sm);

	.gallery {
		display: inline-block;
		width: 100%;
		height: 10rem;
		background-color: var(--color-button-bg-active);

		&.no-image {
			filter: brightness(0.7);
		}

		img {
			box-shadow: none;
			width: 100%;
			height: 10rem;
			object-fit: cover;
		}
	}

	.icon {
		margin-left: var(--spacing-card-bg);
		margin-top: -3rem;
		z-index: 1;

		img,
		svg {
			border-radius: var(--size-rounded-lg);
			box-shadow: -2px -2px 0 2px var(--color-raised-bg), 2px -2px 0 2px var(--color-raised-bg);
		}
	}

	.title {
		margin-left: var(--spacing-card-md);
		margin-right: var(--spacing-card-bg);
		flex-direction: column;

		.name {
			font-size: 1.25rem;
		}

		.status {
			margin-top: var(--spacing-card-xs);
		}
	}

	.description {
		margin-inline: var(--spacing-card-bg);
	}

	.tags {
		margin-inline: var(--spacing-card-bg);
	}

	.stats {
		margin-inline: var(--spacing-card-bg);
		flex-direction: row;
		align-items: center;

		.stat-label {
			display: none;
		}

		.buttons {
			flex-direction: row;
			gap: var(--spacing-card-sm);
			align-items: center;

			> :first-child {
				margin-left: auto;
			}

			&:first-child> :last-child {
				margin-right: auto;
			}
		}

		.buttons:not(:empty)+.date {
			flex-basis: 100%;
		}
	}
}

.display-mode--grid .project-card {
	.gallery {
		display: none;
	}

	.icon {
		margin-top: calc(var(--spacing-card-bg) - var(--spacing-card-sm));

		img,
		svg {
			border: none;
		}
	}

	.title {
		margin-top: calc(var(--spacing-card-bg) - var(--spacing-card-sm));
	}
}

.icon {
	grid-area: icon;
	display: flex;
	align-items: center;
}

.gallery {
	display: none;
	height: 10rem;
	grid-area: gallery;
}

.title {
	grid-area: title;
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	align-items: baseline;
	column-gap: var(--spacing-card-sm);
	row-gap: 0;
	word-wrap: anywhere;

	h2,
	p {
		margin: 0;
	}

	svg {
		width: auto;
		color: var(--color-special-orange);
		height: 1.5rem;
		margin-bottom: -0.25rem;
	}
}

.stats {
	grid-area: stats;
	display: flex;
	flex-direction: column;
	flex-wrap: wrap;
	align-items: flex-end;
	gap: var(--spacing-card-md);

	.stat {
		display: flex;
		flex-direction: row;
		align-items: center;
		width: fit-content;
		gap: var(--spacing-card-xs);
		--stat-strong-size: 1.25rem;

		strong {
			font-size: var(--stat-strong-size);
		}

		p {
			margin: 0;
		}

		svg {
			height: var(--stat-strong-size);
			width: var(--stat-strong-size);
		}
	}

	.date {
		margin-top: auto;
	}

	@media screen and (max-width: 750px) {
		flex-direction: row;
		column-gap: var(--spacing-card-md);
		margin-top: var(--spacing-card-xs);
	}

	@media screen and (max-width: 600px) {
		margin-top: 0;

		.stat-label {
			display: none;
		}
	}
}

.environment {
	color: var(--color-text) !important;
	font-weight: bold;
}

.description {
	grid-area: description;
	margin-block: 0;
	display: flex;
	justify-content: flex-start;
}

.tags {
	grid-area: tags;
	display: flex;
	flex-direction: row;

	@media screen and (max-width: 550px) {
		margin-top: var(--spacing-card-xs);
	}
}

.buttons {
	display: flex;
	flex-direction: column;
	gap: var(--spacing-card-sm);
	align-items: flex-end;
	flex-grow: 1;
}

.small-mode {
	@media screen and (min-width: 750px) {
		grid-template:
			'icon title'
			'icon description'
			'icon tags'
			'stats stats' !important;
		grid-template-columns: min-content auto !important;
		grid-template-rows: min-content 1fr min-content min-content !important;

		.tags {
			margin-top: var(--spacing-card-xs) !important;
		}

		.stats {
			flex-direction: row;
			column-gap: var(--spacing-card-md) !important;
			margin-top: var(--spacing-card-xs) !important;

			.stat-label {
				display: none !important;
			}
		}
	}
}
</style>