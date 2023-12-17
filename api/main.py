from fastapi import FastAPI 
from routers import playbyplay

app = FastAPI()

app.include_router(playbyplay.router)

