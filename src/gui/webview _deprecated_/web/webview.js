function search() {
    console.log('searching');
    var input = document.getElementById('search_input').value;
    var results = document.getElementById('search_results');
    results.innerHTML = '';
    
    pywebview.api.search_project(input)
        .then(data => {
            data = JSON.parse(data);
            data.forEach(mod => {
                var li = document.createElement('li');
                li.appendChild(document.createTextNode(mod.name));
                results.appendChild(li);
            });
        });
}