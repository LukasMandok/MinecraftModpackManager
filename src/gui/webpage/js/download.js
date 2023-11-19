class DownloadList {
    constructor(data) {
        this.container_id = "download-list-container"

        console.log("creating new DownloadList");
        console.log("CategoryList defined: ", typeof CategoryList );
        this.list = new CategoryList(this.container_id);

        console.log("calling process_data...")
        this._process_data(data);
    }

    _process_data(data) {
        console.log("processing data...", data)
        let scope = null;
        let categories = [];

        for (let name in data) {
            console.log("name:", name)
            console.log("data:", data[name])
            scope = data[name]["scope"]
            categories = data[name]["categories"]
            // comment = data[name]["comment"]

            this._create_item(name, scope, categories)
        }

    }

    //  used to extract data from dictionary version (not used for now - switch to array of objects instead)
    _process_data_from_dict(data){
        console.log("processing data...", data)
        let scope = null;
        let categories = [];
        let self = this;
        function recursive_extraction(data, next = null) {
            for (let key in data) {
                console.log("key", key, "next:", next);
                // key names
                if (next == null) {
                    if (key == "scope") {
                        recursive_extraction(data[key], "scope")
                    }
                    else if (key == "category") {
                        recursive_extraction(data[key], "category")
                    }
                    else if (key == "mods") {
                        recursive_extraction(data[key], "mods")
                    }
                    else {
                        console.log("This should not happen: key:", key)
                    }
                }
                // key content
                else {
                    if (next == "scope") {
                        scope = data[key]
                        recursive_extraction(data[key])
                    }
                    else if (next == "category") {
                        categories.push(key)
                        recursive_extraction(data[key])
                        categories.pop()
                    }
                    else if (next == "mods") {
                        self._create_item(data[key], scope, categories)
                    }
                }
            }
        }    
        recursive_extraction(data);
    }

    _create_item(name, scope, categories) {
        console.log("creating item: ", name, scope, categories);

        this.list.addMod(name, scope, categories)
    }


}

function create_download_list(download_list) {
    console.log("creating new DownloadList");
    // console.log("download_list:", download_list)
    let data = JSON.parse(download_list);

    console.log("parsed data:", data)

    let downloadList = new DownloadList(data);
}