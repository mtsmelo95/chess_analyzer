from fastapi import UploadFile
from app.services.analysis_service import analyze_pgn

def upload_and_analyze(file: UploadFile):
    pgn_content = file.file.read().decode("utf-8")
    return analyze_pgn(pgn_content)