export const isOffline = async () => {
    return await invoke('plugin:utils|is_offline', {})
}
