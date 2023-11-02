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
    
    // eel.search_mod(input, "modrinth")(handleSearchResults)
    eel.search_mod(input, "modrinth")((results) => handleSearchResults(results, 1));
    // eel.search_mod(input, "curseforge")(handleSearchResults)
    eel.search_mod(input, "curseforge")((results) => handleSearchResults(results, 2));
}


create_filter(["Filter1_Option1", "Filter1_Option2", "Filter1_Option3"])
create_filter(["Filter2_Option1", "Filter2_Option2", "Filter2_Option3", "Filter2_Option4"])


// Exposed javascript functions

eel.expose(prompt_alerts);

function prompt_alerts(description) {
    alert(description);
}
