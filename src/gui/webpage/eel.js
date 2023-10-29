// document.getElementById("button-search").addEventListener("click", ()=>{search()}, false);

// Exposed python functions
function search() {
    console.log('searching');
    var input = document.getElementById('search_input').value;
    var results = document.getElementById('search_container');
    results.innerHTML = '';

    console.log("Input: " + input)
    
    eel.search_project(input)(handleSearchResults)
}



// Exposed javascript functions

eel.expose(prompt_alerts);

function prompt_alerts(description) {
    alert(description);
}
