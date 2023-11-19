// document.getElementById("button-search").addEventListener("click", ()=>{search()}, false);
document.getElementById('search-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        search();
    }
});

// Exposed python functions
function search() {
    var input = document.getElementById('search-input').value;
    var results = document.getElementById('search-container-1');
    results.innerHTML = '';
    var results = document.getElementById('search-container-2');
    results.innerHTML = '';
    
    // eel.get_mod_search_results(input, "modrinth")(handleSearchResults)
    eel.get_mod_search_results(input, "modrinth")((results) => handleSearchResults(results, 1));
    // eel.get_mod_search_results(input, "curseforge")(handleSearchResults)
    eel.get_mod_search_results(input, "curseforge")((results) => handleSearchResults(results, 2));
}

function request_download_list() {
    eel.request_download_list()
}

function request_downloaded_list() {
    eel.request_downloaded_list()
}

// TODO: dynamically create the search filters from websites
create_filter(["Filter1_Option1", "Filter1_Option2", "Filter1_Option3"])
create_filter(["Filter2_Option1", "Filter2_Option2", "Filter2_Option3", "Filter2_Option4"])


// Exposed javascript functions

eel.expose(prompt_alerts);
eel.expose(receive_download_list);

function prompt_alerts(description) {
    alert(description);
}

function receive_download_list(download_list){
    console.log("javascript eel - receive download list:", download_list);
    create_download_list(download_list);
    return true;
}