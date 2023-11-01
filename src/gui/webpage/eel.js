// document.getElementById("button-search").addEventListener("click", ()=>{search()}, false);
document.getElementById('search_input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        search();
    }
});

// Exposed python functions
function search() {
    console.log('searching');
    var input = document.getElementById('search_input').value;
    var results = document.getElementById('search_container');
    results.innerHTML = '';

    console.log("Input: " + input)
    
    eel.search_mod(input, "modrinth")(handleSearchResults)
    eel.search_mod(input, "curseforge")(handleSearchResults)
}



// Exposed javascript functions

eel.expose(prompt_alerts);

function prompt_alerts(description) {
    alert(description);
}
