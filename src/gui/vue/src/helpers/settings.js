export async function get() {
    // TODO: implement in backend
    window.eel.settings_get()((settings) => {
        return settings
    })
}

export async function set(settings) {
    // TODO: implement in backend
    window.eel.settings_set(settings)
}

export async function change_config_dir(newConfigDir) {
    // TODO: implement in backend
    window.eel.settings_change_config_dir(newConfigDir)((success) => {
        return success
    })
}

export async function is_dir_writeable(newConfigDir) {
    // TODO: implement in backend
    window.eel.settings_is_dir_writeable(newConfigDir)((is_writeable) => {
        return is_writeable
    })
}