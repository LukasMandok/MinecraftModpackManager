export class WebSocketHandler {
    constructor(path, onMessageCallback = null) {
        this.url = `ws://localhost:8080/ws/${path}`;
        this.socket = new WebSocket(this.url);

        console.log("create new WebSocket Handler")

        if (onMessageCallback) {
            this.onMessage(onMessageCallback);
        }
    }

    send(data) {
        this.socket.send(JSON.stringify(data));
    }

    onMessage(callback) {
        console.log("setup new onMessage callback function")
        this.socket.onmessage = event => callback(JSON.parse(event.data));
    }
}