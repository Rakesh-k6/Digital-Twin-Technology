"""
CityLink - FastAPI Server Entry Point
Serves:
1. 3D Virtual World of Bangalore Digital Twin on http://localhost:8000/
2. REST API endpoints on http://localhost:8000/api/
3. 10Hz live WebSocket streaming on ws://localhost:8000/ws/live
4. Interactive Swagger documentation on http://localhost:8000/docs
"""

import os
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routes import router as api_router
from api.websocket import live_websocket_endpoint, ws_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    broadcast_task = asyncio.create_task(periodic_broadcast())
    yield
    broadcast_task.cancel()


async def periodic_broadcast():
    """Streams digital twin telemetry at 10 updates per second (10Hz)."""
    while True:
        try:
            await ws_manager.broadcast_state()
        except Exception as e:
            print(f"Broadcast error: {e}")
        await asyncio.sleep(0.1)


app = FastAPI(
    title="CityLink Cyber-Physical Digital Twin API",
    version="1.0.0",
    description="Backend coordinator for 3D Virtual World of Bangalore, SUMO simulation, BESCOM Grid, and CSOC",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router, prefix="/api")


@app.websocket("/ws/live")
async def websocket_route(websocket: WebSocket):
    await live_websocket_endpoint(websocket)


# Serve 3D Virtual World of Bangalore directly on root '/'
STANDALONE_HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "dashboard", "index_standalone.html")


@app.get("/", response_class=HTMLResponse)
def serve_3d_bangalore_twin():
    if os.path.exists(STANDALONE_HTML_PATH):
        with open(STANDALONE_HTML_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    return HTMLResponse("<h1>CityLink Digital Twin is running. (index_standalone.html not found)</h1>")


@app.get("/status")
def server_status():
    return {
        "project": "CityLink – 3D Virtual World of Bangalore",
        "status": "ONLINE",
        "api_docs": "/docs",
        "direct_link": "http://localhost:8000/"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=1)
