import json, sys, os

from fastapi import FastAPI, WebSocket, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient

from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError

import threading
import trio
from hypercorn.config import Config
from hypercorn.trio import serve

import webbrowser
import http.server
import socketserver

from .websockets import WebSocketManager, WebSocketDecorator, WebSocketHandler

websocket = WebSocketDecorator()

class Backend:
    def __init__(self):
        print("Initializing Backend")
        self.app_manager = None
        self.templates = None
        
        file_dir = os.path.dirname(__file__)
        self.gui_dir = os.path.join(file_dir, "..")
        self.web_dir = os.path.join(self.gui_dir, 'web')
        
        self.development = True
        self.backend_port = 8080
        self.frontend_port = 8000
        self.html_file = os.path.join(self.web_dir, 'index.html')
        
        if (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')):
            self.development = False            

        self.app = FastAPI()
        self.router = APIRouter()
        
        print("initialize websocket manager and decorator")
        self.websocket_manager = WebSocketManager(self.router)
        self.websocket_decorator = WebSocketDecorator(self.websocket_manager)
        
        # self.app.add_middleware(SessionMiddleware, secret_key=random.randbytes(64))
        # self.app.on_event("startup")(self._set_event_loop)
        
        # Websocket routes
        # self.router.add_api_websocket_route("/ws", self.websocket_responder)
        # self.router.add_api_websocket_route("/ws/test", self.websocket_responder_test)
        
        # Add router to app:
        self.app.include_router(self.router)
    def init_routes(self):
        print("initialize routes for backends")
        # Add functions to routers
        self.router.add_api_route("/items/{id}", self.read_item, methods=["GET"])
        
        # Test function
        self.router.add_api_route("/", self.test, methods=["GET"])
        
        print("add router to app")
        self.app.include_router(self.router)

    # only needed in case a seperate server is used for the frontend
    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:{self.frontend_port}"],
            # allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
    # DISCUSS: this function might not be needed at all
    def set_application_manager(self, manager):
        self.app_manager = manager
            
    # def get_websocket_manager(self):
    #     return self.websocket_manager
            
    def run_backend_server(self):
        print("setup middleware")
        self.setup_middleware()
        
        print("setup configs")
        config = Config()
        config.bind = ["localhost:" + str(self.backend_port)]
        
        trio.run(serve, self.app, config)
        
        
    def run_frontend_server(self):
        # INFO: maybe put this as the overall working diretory
        os.chdir(self.web_dir)
        with socketserver.TCPServer(("", self.frontend_port), CustomHandler) as httpd:
            print("serving fronted separatly on port", self.frontend_port)
            httpd.serve_forever()
            
            
    def run(self):
        if self.app_manager is None:
            raise ValueError("Manager not set!")

        if not self.development:
            if (self.frontend_port == self.backend_port):
                print("mount static files on dir: " + self.web_dir)
                self.app.mount("/static", StaticFiles(directory=self.web_dir, html=True), name="static")
            else:
                print("run frontend server in separate thread")
                thread = threading.Thread(target = self.run_frontend_server)
                thread.start()
        
        print("host backend server on separate thread")
        # trio.run(serve, self.app, config)
        # run thread with backend server
        thread = threading.Thread(target = self.run_backend_server)
        thread.start()
        
        print("Open Webbrowser")
        webbrowser.open("http://localhost:" + str(self.frontend_port) + "/static/index.html")
        
        # if (self.development):
        #     print("Packaged Python - hosting own webpage")
        #     self.templates = Jinja2Templates(directory=self.web_dir)
        # else:
        #     print("Development Python - using external host")
        #     uvicorn.run(self.app, host="127.0.0.1", port=8000, log_level="info")

    #---------------------------
    #     API Functions
    #---------------------------    

    async def websocket_responder(self, websocket: WebSocket) -> None:
        print("activated websocket route: ", websocket)
        await websocket.accept()
        
        while True:
            try:
                data = await websocket.receive_json()
                content = data.get("content")
                if content:
                    print("received data content: " + content)
                    await websocket.send_text(f"Message text was: {content}")
                else:
                    print("No content in received data")
                    
            except WebSocketDisconnect:
                print("WebSocket connection has been closed")
                break
            
            except ConnectionClosedError:
                print("Websocket Connection has been closed unexpectedly")
                break
            except Exception as e:
                print("Unknown Exception: {e}")
                break

    #--------------------------
    #       Testing stuff
    #--------------------------
    @websocket("ws/test/")
    async def websocket_handler_test(self, endpoint: WebSocketHandler):
        endpoint.send_text("Decorated Hello World")
    
    async def websocket_responder_test(self, websocket: WebSocket) -> None:
        print("websocket responder test")
        await websocket.accept()
        await websocket.send_json({"content": "Hello WebSocket"})
        await websocket.close()     

    async def test(self):
        return {"message": "Hello World"}
    
    
    def test_websocket_decorator(self):
        print("test websocket decorator")
        client = TestClient(self.app)
        with client.websocket_connect("/ws/test") as websocket:
            websocket.receive_text()
    
    def test_websocket(self):
        print("test websocket")
        client = TestClient(self.app)
        with client.websocket_connect("/ws") as websocket:
            websocket.send_json({"content": "Message for the Websocket Backend"})
            data = websocket.receive_text()
            print("data received: ", data)

    async def read_item(self, request: Request, id: str):
        return self.templates.TemplateResponse("item.html", {"request": request, "id": id})
    
    

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.replace('/static/', '/', 1)
        return http.server.SimpleHTTPRequestHandler.translate_path(self, path)