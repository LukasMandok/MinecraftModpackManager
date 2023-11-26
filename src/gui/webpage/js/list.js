class Mod {
    constructor(name) {
        this.name = name;

        this.selected = false;
        this.visible = true;

        this.versions = [];
        this.loader = [];

        this._createHTML();
        this._createEventListener();

        this.onSelectionChange = () => {};
        this.onSelectionChangeList = () => {};
    }

    _createHTML() {
        this.title = document.createElement('div');
        this.title.className = 'project-card base-card project padding-sm';
        this.title.id = "mod-" + CategoryList.name_to_id(this.name);

        this.label = document.createElement('span');
        this.label.className = 'project-label';
        this.label.innerText = this.name;

        this.title.append(this.label);
    }

    _createEventListener() {
        this.title.addEventListener('click', (event) => {
            this.select();
            event.stopPropagation();
        });
    }

    getHTML() {
        return this.title;
    }

    // Getter and Setter

    setCategories(categories) {
        this.categories = categories;
    }

    getCategory() {
        return this.categories;
    }

    getName() {
        return this.name;
    }

    // Selection

    // allows for back propagation of selection status to parent category
    setOnSelectionCallback(callbackFunction) {
        this.onSelectionChange = callbackFunction;
    }


    // toggle selection status or set it to flag if given
    select(flag = null){
        this.selected = flag !== null ? flag : !this.selected;

        // TODO: apply selection to html
        if (this.selected) {
            this.title.classList.add("selected");
        }
        else {
            this.title.classList.remove("selected");
        }

        // if flag != null, selection was made by forward propagation, so there is no need to propagate back
        if (flag == null) {
            this.onSelectionChange(this.selected);
        }
    }

    isSelected() {
        return this.selected;
    }
}

class Category { 
    constructor(name, id = null, level = 1) {
        this.name = name;
        this.id = id || "category-" + CategoryList.name_to_id(name);
        this.level = level;

        this.selected = false;
        this.partlySelected = false;
        this.visible = true;

        this.categories = {};
        this.mods = {};

        console.log("creating new html of Category", this.name)

        this._createHTML();
        this._createEventListener();

        this.onSelectionChange = () => {};
    }

    // HTML Content

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

    // Getters

    getName() {
        return this.name;
    }

    // TODO: do error handling -maybe?
    getCategory(name) {
        return this.categories[name];
    }

    // Add Items to list

    addCategory(name) {
        let id = this.id + "-" + CategoryList.name_to_id(name);
        let category = new Category(name, id);

        console.log("added new Category: ", name)

        category.setOnSelectionCallback(this.handleChildSelectionChange.bind(this));

        console.log("added callback function to Category: ", name, ":", category.onSelectionChange, "to:", this.handleChildSelectionChange.bind(this))

        this.categories[name] = category;
        this._appendHTML(category.getHTML());

        return category;
    }
    
    addMod(mod) {
        mod.setOnSelectionCallback(this.handleChildSelectionChange.bind(this));

        console.log("Category - addMdod: ", mod)
        this.mods[mod.getName()] = mod;
        console.log("append html to Category:", mod.getHTML())
        this._appendHTML(mod.getHTML());
    }

    // Selection

    setOnSelectionCallback(callbackFunction) {
        this.onSelectionChange = callbackFunction;
    }

    isSelected() {
        return this.selected;
    }

    isPartlySelected() {
        return this.partlySelected;
    }

    partlySelect(flag = true) {
        this.partlySelected = flag;

        this.updateSelection();
    }

    select(flag = null, propagate = true) {
        // toggle selected status or set it to flag if given
        this.selected = flag !== null ? flag : !this.selected;

        console.log("!!! select Category:", this.name, "to:", this.selected, "flag:", flag)

        if (propagate) {
            for (let name in this.categories) {
                let category = this.categories[name];
                category.select(this.selected, true);
            }
            for (let name in this.mods) {
                let mod = this.mods[name];
                mod.select(this.selected, true);
            }
        } 

        // remove partly selection:
        this.partlySelected = false;

        // initiate back propagation if currently not forward propagating
        if (flag != null) {
            // if selection was set by back propagation
            if (propagate == false) {
                this.onSelectionChange(this.selected);
            }
        }
        // start back propagation though categories if selection was toggled, otherwise we are in forward propagation
        else {
            this.onSelectionChange(this.selected);
        }

        // Update selection html
        this.updateSelection();
    }

    updateSelection() {
        if (this.selected) {
            this.title.classList.add("selected");
        }
        else {
            this.title.classList.remove("selected");
        }

        if (this.partlySelected) {
            this.title.classList.add("partly-selected");
        }
        else {
            this.title.classList.remove("partly-selected");
        }
    }

    handleChildSelectionChange(newState, partly = null) {
        // check if all children have the same new states
        let identical = this.isChildSelectionIdentical(newState);

        // if not a partly selection back propagation (backpropagation started or changed selection on parent category)
        if (partly == null) {        
            if (identical == true) {
                // if new selection state is different from current state
                if (newState != this.selected) {
                    // change to new state of parent as well -> also removes partly selection and continues back propagation
                    this.select(newState, false);
                    return;
                }
            }
            // Initiate back propagation:
            // check partly selection conditions:
            // check if any child is already partly selected -> parent is also partly
            partly = this.areChildrenPartlySelected() || this.areChildrenSelected() && !identical;

            this.partlySelect(partly);
            this.onSelectionChange(newState, partly);
        }
        // propagate partly selection of children
        else {
            // stop propagation, if parent already has the correct partly selection
            if (this.isPartlySelected() == partly) {
                return;
            }
            // if any child is partly selected, parent will also be partly selected, even if the child with the back propgation is not partly selected anymore
            if (partly == false) {
                partly = this.areChildrenPartlySelected() || (this.areChildrenSelected() && !identical);
                if (partly == true) {
                    // if partly parent is already partly selected, stop propagation
                    if (this.isPartlySelected() == partly) {
                        return;
                    }
                }
            }
            this.partlySelect(partly);
            this.onSelectionChange(newState, partly);
        }
    }

    isChildSelectionIdentical(newState) {
        for (let c in this.categories) {
            let category = this.categories[c];
            if (category.isSelected() != newState) {
                return false;
            }
        }

        for (let m in this.mods) {
            let mod = this.mods[m];
            if (mod.isSelected() != newState) {
                return false;
            }
        }
        return true
    }

    areChildrenSelected() {
        for (let c in this.categories) {
            let category = this.categories[c];
            if (category.isSelected()) {
                return true;
            }
        }
        for (let m in this.mods) {
            let mod = this.mods[m];
            if (mod.isSelected()) {
                return true;
            }
        }
        return false;
    }

    areChildrenPartlySelected() {
        for (let c in this.categories) {
            let category = this.categories[c];
            if (category.isPartlySelected()) {
                return true;
            }
        }
        return false;
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
        let cat = new Category(name, null, 0); // TODO: replace null by actual 0 for level-0 (this should lead to the same result)
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
        for (let category of categories) {
            let next_cat = null;
            console.log("!!! current category:", category, "exists:", exists)
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
                console.log("next category does not exist yet", category)
                next_cat = cat.addCategory(category);
            }
            console.log("add category to list")
            category_list.push(next_cat)
            cat = next_cat
        }

        return category_list;
    }

    // MOD STUFF

    // TODO: implement rest
    addMod(name, ...category_names_arg) {
        let category_names = category_names_arg.flat();

        let mod = new Mod(name);
        let categories = this.addCategories(category_names);
        mod.setCategories(categories);

        this.mods[name] = mod;

        // add callback function to update mod selection status in list
        // HELP: the arrow function automatically binds the current value of name to the function
        // FIXME: This does not work at the moment
        // this.setOnSelectionModCallback(name, (newState) => {
        //     this.mods[name]["mod"].selected = newState;
        // });

        console.log("add current mod to category:", categories[categories.length - 1].getName());

        // add the mod to the last category in the list
        categories[categories.length - 1].addMod(mod);

        // NOTE: append reference to object ??? 
    }


    // Callback function to update the mods dict with current selection status
    // setOnSelectionModCallback(modName, callbackFunction) {
    //     if (this.mods[modName]) {
    //         this.mods[modName]["mod"].setOnSelectionListCallback(callbackFunction);
    //     }
    // }


    // static functions
    static name_to_id(name) {
        return name.toLowerCase().replace(/ /g, "_");
    }
}