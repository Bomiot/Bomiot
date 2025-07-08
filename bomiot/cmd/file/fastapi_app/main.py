from fastapi import FastAPI
from django.contrib.auth import get_user_model

User = get_user_model()

fastapi_app = FastAPI(title="FastAPI APP")

@fastapi_app.get("/test/")
async def test():
    return {"msg": "This is FastAPI API"}