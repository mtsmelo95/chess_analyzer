from fastapi import FastAPI
from app.views.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chess Analyzer")

app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)