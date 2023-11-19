function openTab(event, tab_name) {
    var i, tabcontent, tablinks;

    // disable active content
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // disable active tab button
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // display new tab and make button active
    document.getElementById(tab_name).style.display = "block";
    event.currentTarget.className += " active";
}


// Mod Item
function createProjectCard(item) {
    const projectCard = document.createElement('article');
    projectCard.className = 'project-card base-card padding-bg equalize';

    // Icon with Link
    const projectIconLink = document.createElement('a');
    projectIconLink.href = null; // TODO
    projectIconLink.className = "icon"
    const modIcon = document.createElement('img');
    modIcon.src = item.icon;
    modIcon.className = 'avatar size-md';
    projectIconLink.append(modIcon);

    // Title: Link, Name, Author
    const modTitle = document.createElement('div');
    modTitle.className = 'title';

    const modNameLink = document.createElement('a');
    modNameLink.href = null; // TODO
    const modName = document.createElement('h2');
    modName.className = 'name';
    modName.innerText = item.name;
    modNameLink.append(modName);

    const modAuthor = document.createElement('p');
    modAuthor.className = 'author';
    modAuthor.innerText = "by ";
    const modAuthorLink = document.createElement('a');
    modAuthorLink.href = null; // TODO
    modAuthorLink.innerText = item.author;
    modAuthor.append(modAuthorLink);

    modTitle.append(modNameLink, modAuthor);

    // Description
    const modDescription = document.createElement('p');
    modDescription.className = 'description';
    modDescription.innerText = item.description;

    const modDetails = document.createElement('div');
    modDetails.className = 'tags categories';

    // Add more span elements for each detail
    // TODO:: add icons
    const modScope = document.createElement('span');
    modScope.className = 'scope';
    modScope.innerText = 'Available on: ' + item.source;

    const modLoader = document.createElement('span');
    modLoader.innerText = 'Modloader: ' + item.mod_loaders;

    const modVersion = document.createElement('span');
    modVersion.innerText = 'Version: ' + item.recent_version;

    modDetails.append(modScope, modLoader, modVersion);
    
    // Mod Stats

    const modStats = document.createElement('div');
    modStats.className = 'stats';

    // TODO: put stats into divs = (svg + p = strong + span (stat-label))
    const modDownloads = document.createElement('div');
    modDownloads.className = 'stat';
    modDownloadsP = document.createElement('p');
    modDownloadsNumber = document.createElement('strong');
    modDownloadsNumber.innerText = item.downloads;
    modDownloadsLabel = document.createElement('span');
    modDownloadsLabel.innerText = ' downloads';
    modDownloadsP.apptmlend(modDownloadsNumber, modDownloadsLabel);
    modDownloads.append(modDownloadsP);

    const modUpdated = document.createElement('div');
    modUpdated.className = 'stat date';
    modUpdatedLabel = document.createElement('span');
    modUpdatedLabel.innerText = 'Updated ';
    modUpdatedDate = document.createElement('span');
    // TODO: get meaningful date    
    modUpdatedDate.innerText = "5 days ago"//item.updated;
    modUpdated.append(modUpdatedLabel, modUpdatedDate);

    modStats.append(modDownloads, modUpdated);
    

    projectCard.append(projectIconLink, modTitle, modDescription, modDetails, modStats);

    return projectCard
}


