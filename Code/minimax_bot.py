import chess
import random
import concurrent.futures

SQUARES_CENTER = [chess.D4, chess.D5, chess.E4, chess.E5]

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3.2,
    chess.BISHOP: 3.33,
    chess.ROOK: 5.1,
    chess.QUEEN: 8.8,
    chess.KING: 0
}

PAWN_TABLE = [
      0, 0, 0, 0, 0, 0, 0, 0,
    0.5, 1, 1, -2, -2, 1, 1, 0.5,
    0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
    0, 0, 0, 2, 2, 0, 0, 0,
    0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
    1, 1, 2, 3, 3, 2, 1, 1,
    5, 5, 5, 5, 5, 5, 5, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
KNIGHT_TABLE = [
    -5, -4, -3, -3, -3, -3, -4, -5,
    -4, -2, 0, 0, 0, 0, -2, -4,
    -3, 0, 1, 1.5, 1.5, 1, 0, -3,
    -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
    -3, 0, 1.5, 2, 2, 1.5, 0, -3,
    -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
    -4, -2, 0, 0.5, 0.5, 0, -2, -4,
    -5, -4, -3, -3, -3, -3, -4, -5
]
BISHOP_TABLE = [
    -2, -1, -1, -1, -1, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 1, 1, 0.5, 0, -1,
    -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
    -1, 0, 1, 1, 1, 1, 0, -1,
    -1, 1, 1, 1, 1, 1, 1, -1,
    -1, 0.5, 0, 0, 0, 0, 0.5, -1,
    -2, -1, -1, -1, -1, -1, -1, -2
]
ROOK_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0.5, 1, 1, 1, 1, 1, 1, 0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    0, 0, 0, 0.5, 0.5, 0, 0, 0
]
QUEEN_TABLE = [
    -2, -1, -1, -0.5, -0.5, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -1, 0, 0.5, 0, 0, 0, 0, -1,
    -2, -1, -1, -0.5, -0.5, -1, -1, -2
]
KING_TABLE = [
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -2, -3, -3, -4, -4, -3, -3, -2,
    -1, -2, -2, -2, -2, -2, -2, -1,
    2, 2, 0, 0, 0, 0, 2, 2,
    2, 3, 1, 0, 0, 1, 3, 2
]
PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE
}

def is_passed_pawn(board, square, color):
    """
    Checks if a pawn is a passed pawn (no enemy pawns can capture it on its way to promotion).
    """
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    enemy = not color
    
    if color == chess.WHITE:
        for r in range(rank + 1, 8):
            for f in [file - 1, file, file + 1]:
                if 0 <= f < 8:
                    sq = chess.square(f, r)
                    piece = board.piece_at(sq)
                    if piece and piece.piece_type == chess.PAWN and piece.color == enemy:
                        return False
        return True
    
    else:
        for r in range(rank - 1, -1, -1):
            for f in [file - 1, file, file + 1]:
                if 0 <= f < 8:
                    sq = chess.square(f, r)
                    piece = board.piece_at(sq)
                    if piece and piece.piece_type == chess.PAWN and piece.color == enemy:
                        return False
        return True

def piece_square_score(board, color):
    """
    Calculates the positional score based on piece-square tables.
    """
    score = 0
    for piece_type, table in PIECE_SQUARE_TABLES.items():
        for sq in board.pieces(piece_type, color):
            idx = sq if color == chess.WHITE else chess.square_mirror(sq)
            score += table[idx]
    return score

def advanced_evaluate(board, color):
    """
    Evaluates the board position considering material, piece positions, mobility, pawn structure, and king safety.
    """
    value = 0
    for piece_type in PIECE_VALUES:
        value += len(board.pieces(piece_type, color)) * PIECE_VALUES[piece_type]
        value -= len(board.pieces(piece_type, not color)) * PIECE_VALUES[piece_type]
    value += piece_square_score(board, color)
    value -= piece_square_score(board, not color)
    value += len([sq for sq in SQUARES_CENTER if board.piece_at(sq) and board.piece_at(sq).color == color]) * 0.2
    value += 0.05 * len(list(board.legal_moves))
    if len(board.pieces(chess.BISHOP, color)) >= 2:
        value += 0.3
    for rook in board.pieces(chess.ROOK, color):
        file_idx = chess.square_file(rook)
        if is_open_file(board, file_idx, not color):
            value += 0.2
    if board.fullmove_number < 15:
        king_square = board.king(color)
        if king_square and chess.square_file(king_square) not in [1, 6]:
            value -= 0.2
    for pawn in board.pieces(chess.PAWN, color):
        if is_passed_pawn(board, pawn, color):
            value += 0.2
    files = [chess.square_file(sq) for sq in board.pieces(chess.PAWN, color)]
    for f in set(files):
        if files.count(f) > 1:
            value -= 0.1 * (files.count(f) - 1)
    total_material = sum(len(board.pieces(pt, color)) * PIECE_VALUES[pt] for pt in PIECE_VALUES if pt != chess.KING)
    if total_material <= 10:
        king_sq = board.king(color)
        if king_sq:
            rank = chess.square_rank(king_sq)
            file = chess.square_file(king_sq)
            value += 0.05 * (3.5 - abs(rank - 3.5))
            value += 0.05 * (3.5 - abs(file - 3.5))
    for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        for sq in board.pieces(piece_type, color):
            if (color == chess.WHITE and chess.square_rank(sq) > 0) or (color == chess.BLACK and chess.square_rank(sq) < 7):
                value += 0.05
    return value

def is_open_file(board, file_index, color):
    """
    Checks if a file is open (no pawns of the given color on that file).
    """
    for rank in range(8):
        sq = chess.square(file_index, rank)
        piece = board.piece_at(sq)
        if piece and piece.piece_type == chess.PAWN and piece.color == color:
            return False
    return True

def is_draw(board):
    """
    Checks if the current position is a draw.
    """
    return board.is_stalemate() or board.is_insufficient_material() or board.can_claim_fifty_moves() or board.can_claim_threefold_repetition()

def minimax(board, depth, alpha, beta, maximizing, color, never_win=True, blunder_threshold=1.5):
    """
    Implements the minimax algorithm with alpha-beta pruning. When ahead, it tries to make suboptimal moves.
    """
    if depth == 0 or board.is_game_over():
        eval_score = advanced_evaluate(board, color)
        if is_draw(board):
            eval_score -= 0.5
        return eval_score, None

    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)

    if never_win:
        non_mate_moves = []
        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)
            if not test_board.is_checkmate():
                non_mate_moves.append(move)
        if non_mate_moves:
            legal_moves = non_mate_moves

    if maximizing and depth == 2:
        score = advanced_evaluate(board, color)
        if score > blunder_threshold:
            worst_score = float('inf')
            worst_moves = []
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)
                if test_board.is_check() or test_board.is_checkmate():
                    continue
                is_hanging = False
                if board.is_capture(move):
                    is_hanging = True
                else:
                    attackers = test_board.attackers(not color, move.to_square)
                    if attackers:
                        is_hanging = True
                material = sum(
                    len(test_board.pieces(pt, color)) * PIECE_VALUES[pt]
                    for pt in PIECE_VALUES
                )
                move_score = material - (5 if is_hanging else 0)
                if move_score < worst_score:
                    worst_score = move_score
                    worst_moves = [move]
                elif move_score == worst_score:
                    worst_moves.append(move)
            if worst_moves:
                return None, random.choice(worst_moves)

    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)
            if is_draw(test_board):
                continue
            eval, _ = minimax(test_board, depth-1, alpha, beta, False, color, never_win, blunder_threshold)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)
            if is_draw(test_board):
                continue
            eval, _ = minimax(test_board, depth-1, alpha, beta, True, color, never_win, blunder_threshold)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def eval_move(args):
    """
    Evaluates a single move using minimax search.
    """
    board_fen, move_uci, depth, color = args
    board = chess.Board(board_fen)
    move = chess.Move.from_uci(str(move_uci))
    board.push(move)
    eval, _ = minimax(board, depth-1, -float('inf'), float('inf'), False, color)
    return eval, move

def quiescence_search(board, alpha, beta, color, depth=2):
    """
    Performs quiescence search to handle tactical positions, focusing on captures and important moves.
    """
    stand_pat = advanced_evaluate(board, color)
    
    stand_pat += random.uniform(-0.3, 0.3)
    
    if stand_pat >= beta:
        return beta
    alpha = max(alpha, stand_pat)
    
    if depth == 0:
        return stand_pat
        
    for move in board.legal_moves:
        if not board.is_capture(move):
            continue
            
        if board.piece_at(move.to_square):
            piece_value = PIECE_VALUES[board.piece_at(move.to_square).piece_type]
            if piece_value > 3:
                continue
                
        board.push(move)
        score = -quiescence_search(board, -beta, -alpha, not color, depth-1)
        board.pop()
        
        if score >= beta:
            return beta
        alpha = max(alpha, score)
    
    return alpha

def get_minimax_move(board, depth=2):
    """
    Main function to get the next move. Uses a combination of minimax, quiescence search, and randomization
    to make the bot play worse when ahead while maintaining some challenge.
    """
    color = board.turn
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    
    current_score = advanced_evaluate(board, color)
    
    if current_score > 1.5:
        moves = []
        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)
            
            if test_board.is_checkmate():
                continue
                
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece and PIECE_VALUES[captured_piece.piece_type] > 3:
                    continue
                    
            if test_board.is_attacked_by(not color, move.to_square):
                continue
                
            if test_board.is_check():
                continue
                
            moves.append(move)
        
        if moves:
            if random.random() < 0.3:
                return random.choice(legal_moves)
            return random.choice(moves)
    
    board_fen = board.fen()
    args_list = [(board_fen, move.uci(), depth, color) for move in legal_moves]
    results = []
    
    for args in args_list:
        board = chess.Board(args[0])
        move = chess.Move.from_uci(str(args[1]))
        board.push(move)
        
        # Use minimax for deeper search with alpha-beta pruning
        eval_score, _ = minimax(board, depth-1, -float('inf'), float('inf'), False, color, 
                              never_win=True, blunder_threshold=1.5)
        
        # Add quiescence search for tactical positions
        if board.is_capture(move) or board.is_check():
            q_score = quiescence_search(board, -float('inf'), float('inf'), args[3])
            eval_score = (eval_score + q_score) / 2  # Average both evaluations
            
        results.append((eval_score, move))
    
    if current_score > 0:
        results.sort(key=lambda x: x[0])
        worst_moves = results[:max(1, len(results) // 3)]
        return random.choice(worst_moves)[1]
    else:
        results.sort(key=lambda x: x[0], reverse=True)
        best_moves = results[:max(1, len(results) // 3)]
        return random.choice(best_moves)[1] 
