from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from puzzle_parser import parse_puz_file
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")
board_state = {}

# WebSocket Connection Manager to track active browsers
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await websocket.send_json({"type": "init_state", "state": board_state})

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

"""
.the @ (called decorator) modifies the function directly below it
.the .get specifies that this function should only handle incoming HTTP get requests
. the / represents the root directory (homepage) of your website 
"""
@app.get("/", response_class=HTMLResponse)
def show_room(request: Request):
    """
    web route handler, configures a specific web endpoint (route)
    executes everytime someone visits the http://localhost:8000/ port 
    """
    puzzle_data = parse_puz_file("NYTpuzzle_example.puz")
    return templates.TemplateResponse(
        request,
        "room.html", #template file from jinja2
        {
            "puzzle": puzzle_data
        }
    )

# WebSocket endpoint for real-time sync
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            key = data.get("key")
            value = data.get("value")
            
            if key is not None:
                if value == "":
                    board_state.pop(key, None)
                else:
                    board_state[key] = value
                
                # Broadcast the update to everyone else (and sender)
                await manager.broadcast({"key": key, "value": value})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


