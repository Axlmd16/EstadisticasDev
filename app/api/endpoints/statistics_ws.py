from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from app.websocket.connection_manager import ConnectionManager
import logging

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/statistics")
async def websocket_statistics(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Aquí se puede manejar la lógica de eventos y broadcast
            await manager.broadcast(f"Mensaje recibido: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logging.info("WebSocket desconectado")
