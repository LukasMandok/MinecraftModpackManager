


// Event listener for an offline event
export function offline_listener(callback) {
    window.addEventListener('offline', (event) => {
        callback(event); // event doesn't have a payload property in this case
    });
}
