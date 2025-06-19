import chess.pgn
from io import StringIO

def analyze_pgn(pgn_content: str):
    pgn_io = StringIO(pgn_content)
    game = chess.pgn.read_game(pgn_io)

    if game is None:
        return {"error": "PGN inválido ou vazio."}

    board = game.board()
    analysis = []

    for move in game.mainline_moves():
        try:
            san = board.san(move)
            board.push(move) 
            analysis.append({
                "move": san,
                "fen": board.fen()
            })
        except Exception as e:
            return {"error": f"Erro ao analisar o movimento {move}: {str(e)}"}

    return {
        "analysis": analysis,
        "result": game.headers.get("Result", "N/A"),
        "event": game.headers.get("Event", "N/A"),
        "white": game.headers.get("White", "N/A"),
        "black": game.headers.get("Black", "N/A")
    }