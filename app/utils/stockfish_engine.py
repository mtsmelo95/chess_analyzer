# app/utils/stockfish_engine.py
import chess.engine
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_PATH = os.path.join(BASE_DIR, "stockfish", "stockfish")

engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

def analyze_position(board):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    
    score = info["score"].white().score(mate_score=10000)
    best_move = info.get("pv", [None])[0]  # "pv" = principal variation
    depth = info.get("depth", None)

    return {
        "score": score,
        "best_move": best_move.uci() if best_move else None,
        "depth": depth
    }