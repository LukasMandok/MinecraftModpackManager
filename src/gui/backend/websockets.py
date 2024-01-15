# websocket_manager.py
from functools import wraps
from typing import Any, Coroutine

from fastapi import APIRouter, WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError, AbortHandshake

class WebSocketManager:
    def __init__(self, router : APIRouter):
        self.router = router
        self.active_connection = None
        self.handlers = []
        
    def add_handler(self, path: str, handler: callable):
        if handler in self.handlers:
            raise ValueError("Handler already exists")
        
        self.handlers.append(handler)
        
        # register new handler
        print("add handler to router")
        self.router.add_api_websocket_route(path, handler)

    async def connect(self, websocket: WebSocket):  
        try:
            if self.active_connection:
                print("There was a previous connection, which is terminated now")
                await self.active_connection.close()
            
            self.active_connection = websocket
            await websocket.accept()  
            
            # for handler in self.handlers:
            #     handler.on_connect(websocket)
            
        except Exception as e:      
            print(e)
            
    async def disconnect(self, websocket: WebSocket):
        try:
            if self.active_connection == websocket:
                self.active_connection = None
                websocket.close()
                
            else: 
                raise ValueError("Websocket is not the active connection")
                
        except Exception as e:
            print("Connection does not exist")
            return
        
        websocket.close()

    # async def send_data(self, data: dict, key: str | None = None):
    #     if key:
    #         await self.connections[key].send_json(data)
    #     else:
    #         for connection in self.connections.values():
    #             await connection.send_json(data)

    # async def send_text(self, data: str, key: str | None = None):
    #     if key:
    #         await self.connections[key].send_text(data)
    #     else:
    #         for connection in self.connections.values():
    #             await connection.send_text(data)


class WebSocketDecorator:
    # def __init__(self, manager: WebSocketManager):
    #     self.manager = manager
    _instance = None
    
    def __new__(cls, manager: WebSocketManager):
        print("WebSocketDecorator - __new__ with manager:", manager)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.manager = manager
        return cls._instance
            
    def __call__(self, path):
        print("WebSocketDecorator - __call__")
        def decorator(handler):
            print("WebSocketDecorator - __call__ + decorator")
            @wraps(handler)
            async def wrapper(*args, **kwargs):
                print("WebSocketDecorator - __call__ + decorator + wrapper")
                instance = WebSocketHandler(handler, path)
                await handler(instance, *args, **kwargs)
                # do some error handling here
                return instance
            
            self.manager.add_handler(path, wrapper)
            return wrapper
        return decorator
    
    # def __call__(self, handler):
    #     async def wrapper(*args, **kwargs):
    #         instance = WebSocketHandler(handler)
    #         await handler(instance, *args, **kwargs)
    #         # do some error handling here
    #         return instance
    
    
class WebSocketDecorator2:
    _instance = None
    
    def __new__(cls, manager):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.manager = manager
        return cls._instance
    
    def __call__(self, path):
        
    

class WebSocketHandler(WebSocketEndpoint):
    def __init__(self, func: callable, path: str):
        super().__init__(path)
        self.func = func
        self.websocket = None
        
    def on_connect(self, websocket: WebSocket):
        self.websocket = websocket
    
    def on_receive(self, websocket: WebSocket, data: Any) -> Coroutine[Any, Any, None]:
        # transfer data to receive method or something. I dont really know what this function is for...
        pass
    
    def on_disconnect(self, websocket: WebSocket, close_code: int) -> Coroutine[Any, Any, None]:
        pass
    
    async def receive(self):
        if self.websocket:
            return self.websocket.receive_text()
        else:
            raise ValueError("No active connection")
    
    async def send_text(self, text):
        if self.websocket:
            self.websocket.send_text(text)
        else: 
            raise ValueError("No active connection")
        
    async def send_json(self, data):
        if self.websocket:
            self.websocket.send_json(data)
        else:
            raise ValueError("No active connection")
        
    def __call__(self, websocket: WebSocket):
        self.scope = websocket.scope
        self.receive = websocket.receive
        self.send = websocket.send
        return self
    
# manager = WebSocketManager()
# websocket_decorator = WebSocketDecorator(manager)

# @WebSocketDecorator("/ws")
# async def handler_test(endpoint, param1):
#     endpoint.send_text(param1)
#     # data = await endpoint.receive()
    