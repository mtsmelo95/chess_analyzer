import chess.engine
import os
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

system = platform.system()

if system == "Darwin":
    ENGINE_FILENAME = "stockfish"
elif system == "Linux":
    ENGINE_FILENAME = "stockfish-ubuntu"
elif system == "Windows":
    ENGINE_FILENAME = "stockfish-windows.exe"
else:
    raise RuntimeError(f"Sistema operacional não suportado: {system}")

ENGINE_PATH = os.path.join(BASE_DIR, "stockfish", ENGINE_FILENAME)

if not os.path.isfile(ENGINE_PATH):
    raise FileNotFoundError(f"Arquivo do Stockfish não encontrado: {ENGINE_PATH}")

engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

def analyze_position(board):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    
    score = info["score"].white().score(mate_score=10000)
    best_move = info.get("pv", [None])[0]
    depth = info.get("depth", None)

    return {
        "score": score,
        "best_move": best_move.uci() if best_move else None,
        "depth": depth
    }