from flask import Flask, request, jsonify
import chess
from Code.minimax_bot import get_minimax_move as get_worst_move

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.get_json()
    fen = data.get('fen')
    
    if not fen:
        return jsonify({'error': 'No FEN string provided'}), 400
    
    board = chess.Board(fen)
    
    worst_move = get_worst_move(board)
    
    if worst_move is None:
        return jsonify({'error': 'No legal moves available'}), 400
    
    board.push(worst_move)
    
    return jsonify({
        'move': str(worst_move),
        'fen': board.fen(),
        'is_check': board.is_check(),
        'is_checkmate': board.is_checkmate(),
        'is_stalemate': board.is_stalemate()
    })

if __name__ == '__main__':
    app.run(debug=True) 