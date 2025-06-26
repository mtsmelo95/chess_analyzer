uvicorn app.main:app --reload

 curl -X POST http://localhost:8000/analyze -F "file=@matchs/exemple.pgn"