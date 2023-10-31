// Process Incomming Data

function handleSearchResults(data) {

    console.log("return from search_project:", JSON.parse(data));

    data = JSON.parse(data);
    data.forEach(item => {
        createSearchItem(item);
    });
}

// Create HTML Elements

function createSearchItem(item) {
    const resultsContainer = document.getElementById('search_container');

    const resultItem = document.createElement('div');
    resultItem.className = 'search-item';

    const modIcon = document.createElement('img');
    modIcon.src = item.icon;
    modIcon.className = 'mod-icon';

    const modInfo = document.createElement('div');
    modInfo.className = 'mod-info';

    const modTitle = document.createElement('h2');
    modTitle.className = 'mod-title';
    modTitle.innerText = item.name;

    const modDesc = document.createElement('p');
    modDesc.className = 'mod-desc';
    modDesc.innerText = item.description;

    const modDetails = document.createElement('div');
    modDetails.className = 'mod-details';

    // Add more span elements for each detail
    const modLoader = document.createElement('span');
    modLoader.innerText = 'Modloader: ' + item.mod_loaders;

    const modVersion = document.createElement('span');
    modVersion.innerText = 'Newest Version: ' + item.recent_version;

    const modPlatform = document.createElement('span');
    modPlatform.innerText = 'Available on: ' + item.source;

    modDetails.append(modLoader, modVersion, modPlatform);
    modInfo.append(modTitle, modDesc, modDetails);
    resultItem.append(modIcon, modInfo);

    resultsContainer.appendChild(resultItem);
}