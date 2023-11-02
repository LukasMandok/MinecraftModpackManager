// Process Incomming Data

function handleSearchResults(data, container = 1) {

    console.log("return from search_project:", JSON.parse(data));

    data = JSON.parse(data);
    data.forEach(item => {
        createSearchItem(item, container);
    });

    equalizeLayout();
}

// Create HTML Elements

// Create Search Content
function createSearchItem(item, container = 1) {
    const searchContainer = document.getElementById('search-container-' + container.toString());
    searchContainer.className = 'search-container';

    const searchItem = document.createElement('div');
    searchItem.className = 'search-item';

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
    searchItem.append(modIcon, modInfo);

    searchContainer.appendChild(searchItem);
}

// Rezise Search-Item Height
function equalizeLayout() {
    console.log("load event.")
    //const searchItems = document.getElementsByClassName('search-item');
    const searchItems = document.querySelectorAll('.search-item');
    
    let maxHeight = 0;
    searchItems.forEach(item => {
        item.style.height = 'auto';

        const itemHeight = item.clientHeight;
        if (itemHeight > maxHeight) {
            maxHeight = itemHeight;
        }
    });

    searchItems.forEach(item => {
        item.style.height = `${maxHeight}px`;
    });
}

const selectedOptionsMap = {};

// Filter Options
function create_filter(filter_list) {
    const filter_bar = document.getElementById('filter-bar');

    console.log("filter_bar", filter_bar)

    const i = filter_bar.children.length;
    const filter_options = document.createElement('div');
    filter_options.className = 'filter-options';
    filter_options.id = 'filter-options-' + i.toString();

    const filter_dropdown = document.createElement('div');
    filter_dropdown.className = 'filter-dropdown';

    const filter_dropdown_button = document.createElement('button');
    filter_dropdown_button.className = 'filter-dropdown-button';
    filter_dropdown_button.innerText = 'Filter ' + i.toString();

    const filter_dropdown_content = document.createElement('div');
    filter_dropdown_content.className = 'filter-dropdown-content';


    const filter_selected_options = document.createElement('div');
    filter_selected_options.className = 'filter-selected-options';
    filter_selected_options.id = 'filter-selected-options-' + i.toString();

    filter_list.forEach((filter, j) => {
        const filter_option = document.createElement('label');
        filter_option.className = 'filter-label';

        const filter_checkbox = document.createElement('input');
        filter_checkbox.type = 'checkbox';
        filter_checkbox.id = filter_options.id + '-' + j.toString();
        filter_checkbox.value = filter;

        filter_checkbox.addEventListener('change', function () {
            if (this.checked) {
                addSelectedOption(filter_selected_options, this.parentElement.innerText.trim(), this.id);
            }
            else {
                removeSelectedOption(filter_selected_options, this.id);
            }
        });

        filter_option.htmlFor = filter_checkbox.id;
        filter_option.innerText = filter;
        filter_option.appendChild(filter_checkbox);
        // const filter_checkbox_label = document.createElement('span');
        // filter_checkbox_label.className = 'filter-option-label';
        // filter_checkbox_label.innerText = filter.label;


        filter_dropdown_content.appendChild(filter_option);
    });

    filter_dropdown.append(filter_dropdown_button, filter_dropdown_content);

    filter_options.append(filter_dropdown, filter_selected_options);

    filter_bar.appendChild(filter_options);
}

// Close the dropdown when clicking outside of it
function close_filter_dropdown() {
    var dropdowns = document.getElementsByClassName('dropdown-content');
    for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.style.display === 'block') {
            openDropdown.style.display = 'none';
        }
    }
}

// Function to add a selected option to the list
function addSelectedOption(selectedOptions, labelText, checkboxId) {
    const selectedOption = document.createElement('div');
    selectedOption.className = 'filter-selected-option';
    // set id of selectedOption:
    selectedOption.id = "selected_" + checkboxId;
    selectedOption.innerHTML = labelText + '<span class="remove-option" data-id="' + checkboxId + '">X</span>';
    
    const checkbox = document.getElementById(checkboxId);

    if (checkbox) {
        let nextCheckbox = checkbox.parentElement.nextElementSibling?.children[0];
        let nextSelectedOption = nextCheckbox ? document.getElementById("selected_" + nextCheckbox.id) : null;

        while (!nextSelectedOption && nextCheckbox) {
            nextCheckbox = nextCheckbox.parentElement.nextElementSibling?.children[0];
            nextSelectedOption = nextCheckbox ? document.getElementById("selected_" + nextCheckbox.id) : null;
        }

        if (nextSelectedOption) {
            selectedOptions.insertBefore(selectedOption, nextSelectedOption);
        } else {
            selectedOptions.appendChild(selectedOption);
        }
    }

    // Find the corresponding checkbox
    // const checkbox = document.getElementById(checkboxId);
    // if (checkbox) {
    //     if (selectedOptions.children.length == 0) {
    //         selectedOptions.appendChild(selectedOption);
    //     }
    //     else if (checkbox.parentElement.nextElementSibling != null) {
    //         console.log(selectedOptions, selectedOptions.contains);
    //         found = false;
    //         let nextCheckbox = checkbox.parentElement.nextElementSibling.children[0];
    //         let nextSelectedOption = null;

    //         while (found == false && nextCheckbox != null) {
    //             // check if nextSibling is in selectedOptions
    //             nextSiblingId = nextCheckbox.id;
    //             selectedOptionId = "selected_" + nextSiblingId;
    //             nextSelectedOption = document.getElementById(selectedOptionId);
    //             if (nextSelectedOption != null) {
    //                 found = true;
    //             } else {
    //                 if (nextCheckbox.parentElement.nextElementSibling != null) {
    //                     nextCheckbox = nextCheckbox.parentElement.nextElementSibling.children[0];
    //                 }
    //                 else {
    //                     break;
    //                 }
    //             }
    //         }
    //         if (found) {
    //             // Insert the selected option right before the next sibling
    //             selectedOptions.insertBefore(selectedOption, nextSelectedOption);
    //         } else {
    //             // If there's no next sibling, just append the selected option
    //             selectedOptions.appendChild(selectedOption);
    //         }
    //     }
    //     else {
    //         selectedOptions.appendChild(selectedOption);
    //     }
    // }
    
    // Add click event to remove the selected option
    selectedOption.querySelector('.remove-option').addEventListener('click', function () {
        const checkbox = document.getElementById(this.getAttribute('data-id'));
        checkbox.checked = false;
        selectedOptions.removeChild(selectedOption);
    });
}

// Function to remove a selected option from the list
function removeSelectedOption(selectedOptions, checkboxId) {
    const selectedOption = document.getElementById('selected_' + checkboxId);
    if (selectedOption) {
        selectedOptions.removeChild(selectedOption);
    }
}


// ------------- Event Listeners --------------

// Search Content

// equalize Layout when loaded
window.addEventListener('load', () => {
    equalizeLayout();
});


// equalize Layout when content resized
resizeTimer = null;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(equalizeLayout, 250);
});


// Search FIlter

// add event listener for click on dropdown button
window.addEventListener('click', (event) => {
    if (!event.target.matches('.filter-dropdown-button')) {
        close_filter_dropdown();
    }
});
