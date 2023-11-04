import PySimpleGUI as sg

# Filter options: 
PROJECT_TYPE = ["All", "Mod", "Data Pack", "Resource Pack", "Shader Pack"]
VERSIONS = ["All", "1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4", "1.20", "1.20.1"]
MOD_LOADERS = ["All", "Fabric", "Forge", "Quilt"]


options = ["Option 1", "Option 2", "Option 3", "Option 4"]

def create_checkbox_popup():
    checkbox_layout = [[sg.Checkbox(option, key=option)] for option in options]
    checkbox_window = sg.Window("Checkbox Popup", checkbox_layout, modal=True)
    event, values = checkbox_window.read()
    checkbox_window.close()
    return [option for option in options if values[option]]


class Application:
    def __init__(self):
        self.applicationManager = None

        self.layout = [
            [sg.Text("Search for a project:"), sg.InputText(key="search"), sg.Button("Search", key="search_button")],
            [sg.Text("Filter by:"), sg.Column([
                [sg.Text("Project Type"), sg.Combo([[sg.Checkbox(option, key=option)] for option in PROJECT_TYPE], key="project_type")],
                [sg.Combo(values=options, default_value="All", enable_events=True, key="selected_option")],
                [sg.Text("Version Number"), sg.Checkbox("All", key=None), sg.Checkbox("1.19", key="1.19"), sg.Checkbox("1.19.1", key="1.19.1"), sg.Checkbox("1.19.2", key="1.19.2"), sg.Checkbox("1.19.3", key="1.19.3"), sg.Checkbox("1.19.4", key="1.19.4"), sg.Checkbox("1.20", key="1.20"), sg.Checkbox("1.20.1", key="1.20.1")],
                [sg.Text("Mod Loader"), sg.Checkbox("All", key=None), sg.Checkbox("Fabric", key="fabric"), sg.Checkbox("Forge", key="forge"), sg.Checkbox("Quilt", key="quilt")]
            ])],
            [sg.Text("Best result:"), sg.Text("", key="result_text"), sg.Button("Add to data manager", key="add_button"), sg.Button("Get more options", key="more_button")],
            [sg.Text("", key="source_text")]
        ]

        self.window = sg.Window("Minecraf Modpack Manager", self.layout)

    def _clear_selection(self, values):
        if "All" in values["selected_option"]:
            window["options"].update(set_to_index=None)


    def set_application_manager(self, manager):
        self.manager = manager

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == "search_button":
                search_term = values["search"]
                result = self.manager.search_project(search_term)

                if result is None:
                    sg.popup("No result found")
                    continue

                self.window["result_text"].update(result["name"])
                self.window["source_text"].update(f"Source: {result['source']}")

            if event == "filter_type":
                filter_type = values["filter_type"]
                if filter_type == "Project Type":
                    filter_values = ["Mod", "Data Pack", "Resource Pack", "Shader Pack"]
                elif filter_type == "Version Number":
                    filter_values = ["1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4", "1.20", "1.20.1"]
                elif filter_type == "Mod Loader":
                    filter_values = ["Fabric", "Forge", "Quilt"]
                self.window["filter_values"].update(filter_values)

            if event == "selected_option":
                if values["selected_option"] == "All":
                    selected_options = create_checkbox_popup()
                    window["selected_option"].update("All" if len(selected_options) == len(options) else selected_options)

            if event == "more_button":
                # TODO: implement function to get more options
                sg.popup("Not implemented yet")

            if event == "add_button":
                self.manager.add_project(result)

        self.window.close()