"""
CityLink - High-Performance WebSocket Streamer
Streams continuous 10Hz digital twin telemetry to Unity 3D and React dashboard clients.
"""

import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set

from citylink.simulation import citylink_sim


class WebSocketStreamManager:
    """Manages active WebSocket connections for Unity and React frontend."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast_state(self):
        """Broadcasts current snapshot to all connected clients."""
        if not self.active_connections:
            return

        state = citylink_sim.get_full_state()
        data = json.dumps(state)

        disconnected = set()
        for conn in list(self.active_connections):
            try:
                await conn.send_text(data)
            except Exception:
                disconnected.add(conn)

        for dead_conn in disconnected:
            self.active_connections.discard(dead_conn)


ws_manager = WebSocketStreamManager()


async def live_websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
                action = msg.get("action")
                if action == "SET_SCENARIO":
                    citylink_sim.set_scenario(msg.get("scenario", "NORMAL_CITY"))
                elif action == "APPLY_MITIGATION":
                    citylink_sim.apply_mitigation()
                elif action == "RESET":
                    citylink_sim.reset()
                elif action == "PAUSE":
                    citylink_sim.is_paused = True
                elif action == "RESUME":
                    citylink_sim.is_paused = False
                elif action == "SET_SPEED":
                    citylink_sim.sim_speed = float(msg.get("speed", 1.0))
            except Exception as e:
                pass
    except (WebSocketDisconnect, Exception):
        ws_manager.disconnect(websocket)
