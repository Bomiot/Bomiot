from fastapi import FastAPI,WebSocket
from django.contrib.auth import get_user_model

User = get_user_model()

fastapi_app = FastAPI(title="FastAPI APP")

@fastapi_app.get("/test/")
async def test():
    return {"msg": "This is FastAPI API"}

@fastapi_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
        except:
            break