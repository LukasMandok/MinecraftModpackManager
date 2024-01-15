// document.getElementById("button-search").addEventListener("click", ()=>{search()}, false);
// document.getElementById('search-input').addEventListener('keydown', function(event) {
//     if (event.key === 'Enter') {
//         search();
//     }
// });

// Exposed python functions
export function search() {
    var input = document.getElementById('search-input').value;
    var container1 = document.getElementById('search-container-1');
    container1.innerHTML = ''; 
    var container2 = document.getElementById('search-container-2');
    container2.innerHTML = '';
    
    // eel.get_mod_search_results(input, "modrinth")(handleSearchResults)
    window.eel.get_mod_search_results(input, "modrinth")((results) => handleSearchResults(results, 1));
    // eel.get_mod_search_results(input, "curseforge")(handleSearchResults)
    window.eel.get_mod_search_results(input, "curseforge")((results) => handleSearchResults(results, 2));
}

export function request_download_list() {
    window.eel.request_download_list()
}

export function request_downloaded_list() {
    window.eel.request_downloaded_list()
}

// TODO: dynamically create the search filters from websites
// create_filter(["Filter1_Option1", "Filter1_Option2", "Filter1_Option3"])
// create_filter(["Filter2_Option1", "Filter2_Option2", "Filter2_Option3", "Filter2_Option4"])


// Exposed javascript functions
window.eel.expose(prompt_alerts, "prompt_alerts");
window.eel.expose(receive_download_list, "receive_download_list");

function prompt_alerts(description) {
    console.log("javascript eel - prompt alerts:", description);
    alert(description);
}

function receive_download_list(download_list){
    console.log("javascript eel - receive download list:", download_list);
    // create_download_list(download_list);
    return true;
}