from fastapi import APIRouter, UploadFile, File
from app.controllers import game_controller

router = APIRouter()

@router.post("/analyze")
def analyze_game(file: UploadFile = File(...)):
    return game_controller.upload_and_analyze(file)