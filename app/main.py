from fastapi import FastAPI
from app.views.routes import router

app = FastAPI(title="Chess Analyzer")

app.include_router(router)