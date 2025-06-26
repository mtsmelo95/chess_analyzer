import chess.pgn
import io
from collections import Counter
from app.utils.stockfish_engine import analyze_position

def classify_accuracy(diff):
    if diff is None:
        return "desconhecido"
    elif diff == 0:
        return "perfeito"
    elif diff <= 20:
        return "preciso"
    elif diff <= 50:
        return "imprecisão"
    elif diff <= 150:
        return "erro"
    else:
        return "erro grave"

def analyze_pgn(pgn_text: str):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    
    if game is None:
        raise ValueError("PGN inválido ou vazio.")

    current_board = game.board()
    previous_board = game.board()
    analysis = []
    accuracy_counter = Counter()

    for move in game.mainline_moves():
        san_move = current_board.san(move)

        result = analyze_position(current_board)
        eval_score = result["score"]
        best_move = result["best_move"]
        depth = result["depth"]

        diff = None
        if best_move:
            try:
                test_board = previous_board.copy(stack=False)
                move_obj = chess.Move.from_uci(best_move)

                if move_obj in test_board.legal_moves:
                    test_board.push(move_obj)
                    best_eval = analyze_position(test_board)["score"]
                    if eval_score is not None and best_eval is not None:
                        diff = abs(eval_score - best_eval)
            except Exception as e:
                print(f"[WARN] Falha ao simular melhor lance: {e}")
                diff = None

        current_board.push(move)
        previous_board.push(move)

        accuracy = classify_accuracy(diff)
        accuracy_counter[accuracy] += 1

        analysis.append({
            "move": san_move,
            "fen": current_board.fen(),
            "evaluation": eval_score,
            "best_move": best_move,
            "depth": depth,
            "accuracy": accuracy
        })

    summary = dict(accuracy_counter)
    
    return {
        "summary": summary,
        "analysis": analysis
    }