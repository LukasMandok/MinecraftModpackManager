<template>
	<div
:class = "{'search-page': true, 
                    'normal-page': true,
                    // 'alt-layout': cosmetics.searchLayout,
                    }">

        <Head>
            <Title>Search {{ projectType.display }}s</Title>
        </Head>

        <!-- Sidebar -->
        <aside :class="{'normal-page__sidebar' : true, open: sidebarMenuOpen,}">

            <!-- Filters -->
            <section class="card filters-card" role="presentation">
                <div class="sidebar-menu" :class="{ 'sidebar-menu_open': sidebarMenuOpen}">
                    
                    <!-- Clear filter button -->
                    <button 
						:disabled=" 
							onlyOpenSource === false &&
                            selectedEnvironments.length === 0 &&
                            selectedVersions.length === 0 &&
                            facets.length === 0 &&
                            orFacets.length === 0"                                        
                        class="iconified-button" @click="clearFilters">
                        <ClearIcon />
                        Clear filters
                    </button>
					
					<!-- Category filter -->
                    <section aria-label="Category filters">
                        <div v-for="(categories, header) in categoriesMap" :key="header">
                            <h3 v-if="categories.filter((x) => x.project_type === projectType.actual).length > 0" class="sidebar-menu-heading">
                                {{ $formatCategoryHeader(header) }}
                            </h3>

                            <SearchFilter
                                v-for="category in categories.filter((x) => x.project_type === projectType.actual)"
                                :key="category.name"
                                :active-filters="facets"
                                :display-name="$formatCategory(category.name)"
                                :facet-name="`categories:'${encodeURIComponent(category.name)}'`"
                                :icon="header === 'resolutions' ? null : category.icon"
                                @toggle="toggleFacet"
                            />
                        </div>
					</section>

					<!-- Loader Filter -->
					<section v-if="projectType.id !== 'resourcepack' && projectType.id !== 'datapack'" aria-label="Loader filters">
						<h3
v-if=" tags.loaders.filter((x) => x.supported_project_types.includes(projectType.actual))
							.length > 0" class="sidebar-menu-heading">
							Loaders
						</h3>

						<SearchFilter
							v-for="loader in tags.loaders.filter((x) => {
								if (
									projectType.id === 'mod' &&
									!showAllLoaders &&
									x.name !== 'forge' &&
									x.name !== 'fabric' &&
									x.name !== 'quilt' &&
									x.name !== 'neoforge'
								) {
									return false
								} else if (projectType.id === 'mod' && showAllLoaders) {
									return tags.loaderData.modLoaders.includes(x.name)
								} else if (projectType.id === 'plugin') {
									return tags.loaderData.pluginLoaders.includes(x.name)
								} else if (projectType.id === 'datapack') {
									return tags.loaderData.dataPackLoaders.includes(x.name)
								} else {
									return x.supported_project_types.includes(projectType.actual)
								}
							})"
							:key="loader.name"
							ref="loaderFilters"
							:active-filters="orFacets"
							:display-name="$formatCategory(loader.name)"
							:facet-name="`categories:'${encodeURIComponent(loader.name)}'`"
							:icon="loader.icon"
							@toggle="toggleOrFacet"
						/>
						<Checkbox
							v-if="projectType.id === 'mod'"
							v-model="showAllLoaders"
							:label="showAllLoaders ? 'Less' : 'More'"
							description="Show all loaders"
							style="margin-bottom: 0.5rem"
							:border="false"
							:collapsing-toggle-style="true"
						/>
					</section>

					<!-- Environments -->
					<section
						v-if="!['resourcepack', 'plugin', 'shader', 'datapack'].includes(projectType.id)"
						aria-label="Environment filters"
					>
						<h3 class="sidebar-menu-heading">Environments</h3>
						<SearchFilter
							:active-filters="selectedEnvironments"
							display-name="Client"
							facet-name="client"
							@toggle="toggleEnv"
							>
							<ClientIcon />
						</SearchFilter>
						<SearchFilter
							:active-filters="selectedEnvironments"
							display-name="Server"
							facet-name="server"
							@toggle="toggleEnv"
							>
							<ServerIcon />
						</SearchFilter>
					</section>

					<!-- Versions -->
					<section>
						<h3 class="sidebar-menu-heading">Minecraft versions</h3>
						<Checkbox
							v-model="showSnapshots"
							label="Show all versions"
							description="Show all versions"
							style="margin-bottom: 0.5rem"
							:border="false"
						/>
						<multiselect
							v-model="selectedVersions"
							:options="
							showSnapshots
								? tags.gameVersions.map((x) => x.version)
								: tags.gameVersions
									.filter((it) => it.version_type === 'release')
									.map((x) => x.version)
							"
							:multiple="true"
							:searchable="true"
							:show-no-results="false"
							:close-on-select="false"
							:clear-search-on-select="false"
							:show-labels="false"
							:selectable="() => selectedVersions.length <= 6"
							placeholder="Choose versions..."
							@update:model-value="onSearchChange(1)"
						/>
					</section>
				</div>
			</section>
        </aside>

		<!-- Search Results -->
		<section class="normal-page__content">
			<!-- Search Controls -->
			<div class="card search-controls">
				<div class="search-filter-container">
					<!-- Filters button, if sidebar not shown -->
					<button
						class="iconified-button sidebar-menu-close-button"
						:class="{ open: sidebarMenuOpen }"
						@click="sidebarMenuOpen = !sidebarMenuOpen"
					>
						<FilterIcon />
						Filters...
					</button>

					<!-- Search bar -->
					<div class="iconified-input">
						<label class="hidden" for="search">Search</label>
						<SearchIcon />
						<input
						id="search"
						v-model="query"
						type="search"
						name="search"
						:placeholder="`Search ${projectType.display}s...`"
						autocomplete="off"
						@input="onSearchChange(1)"
						/>
					</div>
				</div>

				<div class="sort-controls">
					<!-- Sorting -->
					<div class="labeled-control">
						<span class="labeled-control__label">Sort by</span>
						<Multiselect
						v-model="sortType"
						placeholder="Select one"
						class="search-controls__sorting labeled-control__control"
						track-by="display"
						label="display"
						:options="sortTypes"
						:searchable="false"
						:close-on-select="true"
						:show-labels="false"
						:allow-empty="false"
						@update:model-value="onSearchChange(1)"
						>
						<template #singleLabel="{ option }">
							{{ option.display }}
						</template>
						</Multiselect>
					</div>

					<!-- Amount of Entries per page -->
					<div class="labeled-control">
						<span class="labeled-control__label">Show per page</span>
						<Multiselect
						v-model="maxResults"
						placeholder="Select one"
						class="labeled-control__control"
						:options="maxResultsForView[cosmetics.searchDisplayMode[projectType.id]]"
						:searchable="false"
						:close-on-select="true"
						:show-labels="false"
						:allow-empty="false"
						@update:model-value="onMaxResultsChange(currentPage)"
						/>
					</div>

					<!-- toggle layout mode -->
					<button
						v-tooltip="$capitalizeString(cosmetics.searchDisplayMode[projectType.id]) + ' view'"
						:aria-label="$capitalizeString(cosmetics.searchDisplayMode[projectType.id]) + ' view'"
						class="square-button"
						@click="cycleSearchDisplayMode()"
					>
						<GridIcon v-if="cosmetics.searchDisplayMode[projectType.id] === 'grid'" />
						<ImageIcon v-else-if="cosmetics.searchDisplayMode[projectType.id] === 'gallery'" />
						<ListIcon v-else />
					</button>
				</div>
			</div>
			<Pagination
				:page="currentPage"
				:count="pageCount"
				:link-function="(x) => getSearchUrl(x <= 1 ? 0 : (x - 1) * maxResults)"
				class="pagination-before"
				@switch-page="onSearchChange"
			/>
			<LogoAnimated v-if="searchLoading && !noLoad"></LogoAnimated>
			<div v-else-if="results && results.hits && results.hits.length === 0" class="no-results">
				<p>No results found for your query!</p>
			</div>
			<div v-else class="search-results-container">
				<div
				id="search-results"
				class="project-list"
				:class="'display-mode--' + cosmetics.searchDisplayMode[projectType.id]"
				role="list"
				aria-label="Search results"
				>
				<ProjectCard
					v-for="result in results?.hits"
					:id="result.slug ? result.slug : result.project_id"
					:key="result.project_id"
					:display="cosmetics.searchDisplayMode[projectType.id]"
					:featured-image="result.featured_gallery ? result.featured_gallery : result.gallery[0]"
					:type="result.project_type"
					:author="result.author"
					:name="result.title"
					:description="result.description"
					:created-at="result.date_created"
					:updated-at="result.date_modified"
					:downloads="result.downloads.toString()"
					:follows="result.follows.toString()"
					:icon-url="result.icon_url"
					:client-side="result.client_side"
					:server-side="result.server_side"
					:categories="result.display_categories"
					:search="true"
					:show-updated-date="sortType.name !== 'newest'"
					:hide-loaders="['resourcepack', 'datapack'].includes(projectType.id)"
					:color="result.color"
				/>
				</div>
			</div>
			<pagination
				:page="currentPage"
				:count="pageCount"
				:link-function="(x) => getSearchUrl(x <= 1 ? 0 : (x - 1) * maxResults)"
				class="pagination-after"
				@switch-page="onSearchChangeToTop"
			/>
			</section>
		</div>
</template>

<script setup>
    
</script>

<style lang="scss" scoped>

</style>