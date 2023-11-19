class Mod {
    constructor(name) {
        this.name = name;

        this.selected = false;
        this.visible = true;

        this.versions = [];
        this.loader = [];

        this._createHTML();
    }

    _createHTML() {
        this.container = document.createElement('div');
        this.container.className = 'project-card base-card project padding-sm';
        this.container.id = "mod-" + CategoryList.name_to_id(this.name);

        this.label = document.createElement('span');
        this.label.className = 'project-label';
        this.label.innerText = this.name;

        this.container.append(this.label);
    }

    getHTML() {
        return this.container;
    }


    getName() {
        return this.name;
    }


    select(flag = null){
        this.selected = flag !== null ? flag : !this.selected;

        // TODO: apply selection to html
        if (this.selected) {
            this.container.classList.add("selected");
        }
        else {
            this.container.classList.remove("selected");
        }
    }
}

class Category {
    constructor(name, id = null, level = 1) {
        this.name = name;
        this.id = id || "category-" + CategoryList.name_to_id(name);
        this.level = level;

        this.selected = false;
        this.visible = true;

        this.categories = {};
        this.mods = {};

        console.log("creating new html of Category", this.name)

        this._createHTML();
        this._createEventListener();
    }

    _createHTML() {
        this.container = document.createElement('div');
        this.container.className = 'category-container';
        this.container.id = this.id;

        // Create Title Element
        this.title = document.createElement('div');
        this.title.className = 'project-card base-card category padding-sm';

        this.label = document.createElement('span');
        this.label.className = 'category-label';
        this.label.innerText = this.name;

        this.arrow = document.createElement('div');
        this.arrow.className = 'multiselect__select'; 

        this.title.append(this.label, this.arrow);

        // Create Mod Container
        this.sub_container = document.createElement('div');
        this.sub_container.className = 'category-subcontainer' + ' level-' + this.level;

        
        this.container.append(this.title, this.sub_container);
    }

    _createEventListener() {
        this.title.addEventListener('click', (event) => {
            console.log("clicked category:", this.name);
            this.select();
            event.stopPropagation();
        });
    }

    _appendHTML(item_html) {
        this.sub_container.append(item_html);
    }

    getHTML() {
        return this.container;
    }



    getName() {
        return this.name;
    }

    // TODO: do error handling -maybe?
    getCategory(name) {
        return this.categories[name];
    }

    addCategory(name) {
        let id = this.id + "-" + CategoryList.name_to_id(name);
        let category = new Category(name, id);

        this.categories[name] = category;
        this._appendHTML(category.getHTML());

        return category;
    }
    
    addMod(mod) {
        console.log("Category - addMdod: ", mod)
        this.mods[mod.getName()] = mod;
        console.log("append html to Category:", mod.getHTML())
        this._appendHTML(mod.getHTML());
    }

    select(flag = null) {
        // FIXME: maybe this instead: this.selected = flag !== null ? flag : !this.selected
        this.selected = flag !== null ? flag : !this.selected;

        console.log("toggle selected of Category:", this.name, "to:", this.selected)

        for (let name in this.categories) {
            let category = this.categories[name];
            category.select(this.selected);
        }
        for (let name in this.mods) {
            let mod = this.mods[name];
            mod.select(this.selected);
        }
        
        // add class Name selected to html
        if (this.selected) {
            this.title.classList.add("selected");
        }
        else {
            this.title.classList.remove("selected");
        }

    }
}

class CategoryList {
    constructor(container_id) {
        console.log("creating new CategoryList");
        this.categories = {};
        this.mods = {};

        // TODO use as parameter
        this.container_id = container_id;
        
        console.log("creating new html of CategoryList")
        this._createHTML();        
    }

    _createHTML() {
        this.container = document.getElementById(this.container_id);
        console.log("!!!!!!!! get Category List container", this.container)
    }

    _appendHTML(category_html) { 
        console.log("appending html to CategoryList now ")
        console.log("is instance of Node: ", category_html instanceof Node);
        this.container.append(category_html);
        console.log("finished appending html")
    }

    getHTML() {
        return this.container;
    }


    //  get categories from list of categories names
    // TODO: add error handling for missing categories 
    getCategory(...categories_args) {
        let categories = categories_args.flat()

        let cur_category = this.categories[categories.shift()];
        for (let category of categories) {
            cur_category = cur_category.getCategory(category)
        }
        return cur_category;
    }

    addCategory(name) {
        console.log("CategoryList - addCategory: ", name)
        let cat = new Category(name, null, 0);
        this.categories[name] = cat;
        console.log("append html to CategoryList:", cat.getHTML())
        this._appendHTML(cat.getHTML());
        console.log("retrun from addCategory function.")
        return cat;
    }

    // add categories if they dont exist yet
    addCategories(...categories_args) {
        let categories = categories_args.flat()

        let exists = true;
        let category_list = [];

        // add first category
        let first_cat = categories.shift()
        console.log("adding first category", first_cat)
        let cat = this.categories[first_cat]
        if (!(cat)) {
            exists = false;
            console.log("first category does not exist yet", first_cat)
            cat = this.addCategory(first_cat)
        }
        category_list.push(cat)
        
        // add rest of categories from the list
        console.log("adding rest of categories", categories)
        let next_cat = null;
        for (let category of categories) {
            if (exists) {
                console.log("previous category exists, getting next category:", category)
                next_cat = cat.getCategory(category)
                console.log("next category:", next_cat)
                if (!(next_cat)) {
                    exists = false;
                }
            }
            console.log("next category exists:", next_cat)
            if (!(next_cat)) {
                console.log("next   category does not exist yet", category)
                next_cat = cat.addCategory(category);
            }
            category_list.push(next_cat)
            cat = next_cat
        }

        return category_list;
    }

    // MOD STUFF

    // TODO: implement rest
    addMod(name, ...category_names_arg) {
        console.log("called add mod function: ", name, "to categories:", category_names_arg, "to CategoryList")
        let category_names = category_names_arg.flat();
        console.log("adding new mod:", name, "to categories:", category_names, "to CategoryList")
        
        let mod = new Mod(name);
        console.log("created mod")
        let categories = this.addCategories(category_names);
        console.log("added new categories")

        this.mods[name] = {"mod": mod, "categories": categories};

        console.log("add mod to Category:", categories[categories.length - 1])
        // add the mod to the last category in the list
        categories[categories.length - 1].addMod(mod);
        console.log("added mod to last category in list")

        // NOTE: append reference to object ??? 
    }

    // static functions
    static name_to_id(name) {
        return name.toLowerCase().replace(/ /g, "_");
    }
}