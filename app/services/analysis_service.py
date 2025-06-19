import chess.pgn
from io import StringIO
from app.utils.stockfish_engine import analyze_position

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

            # Obtem análise ANTES de aplicar o lance
            engine_info = analyze_position(board)

            best_move_uci = engine_info["best_move"]
            best_move_san = None
            accuracy = None

            if best_move_uci:
                best_move_obj = chess.Move.from_uci(best_move_uci)
                if best_move_obj in board.legal_moves:
                    best_move_san = board.san(best_move_obj)
                    if best_move_san == san:
                        accuracy = "preciso"

            board.push(move)  # Aplica o lance depois da análise

            analysis.append({
                "move": san,
                "fen": board.fen(),
                "evaluation": engine_info["evaluation"],
                "best_move": best_move_uci,
                "depth": engine_info["depth"],
                "accuracy": accuracy
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