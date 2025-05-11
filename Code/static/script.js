let board = null;
let game = new Chess();
let $status = $('#status');
let $board = $('#board');
let playerColor = null;
let pendingPromotion = null;

function getOrientationStr() {
    return playerColor === 'b' ? 'black' : 'white';
}

function removeHighlights() {
    $('#board .square-55d63').removeClass('square-legal');
}

function highlightSquares(squares) {
    removeHighlights();
    squares.forEach(sq => {
        $('#board .square-' + sq).addClass('square-legal');
    });
}

function onMouseoverSquare(square, piece) {
    if (game.game_over() || game.turn() !== playerColor) return;
    const moves = game.moves({ square, verbose: true });
    if (moves.length === 0) return;
    const squaresToHighlight = moves.map(m => m.to);
    highlightSquares(squaresToHighlight);
}

function onMouseoutSquare(square, piece) {
    removeHighlights();
}

function onDragStart(source, piece) {
    // Only allow player's pieces to be moved and only on their turn
    if (
        game.game_over() ||
        (playerColor === 'w' && piece.search(/^b/) !== -1) ||
        (playerColor === 'b' && piece.search(/^w/) !== -1) ||
        (game.turn() !== playerColor)
    ) {
        return false;
    }
    // Only allow dragging if there are legal moves for this piece
    if (game.moves({ square: source, verbose: true }).length === 0) {
        return false;
    }
}

function showPromotionDialog(from, to, color) {
    const pieces = ['q', 'r', 'b', 'n'];
    const $dialog = $('#promotion-dialog');
    const $options = $('#promotion-options');
    $options.empty();
    pieces.forEach(piece => {
        const unicode = {
            'q': color === 'w' ? '\u2655' : '\u265B',
            'r': color === 'w' ? '\u2656' : '\u265C',
            'b': color === 'w' ? '\u2657' : '\u265D',
            'n': color === 'w' ? '\u2658' : '\u265E'
        }[piece];
        const btn = $(`<button>${String.fromCharCode(parseInt(unicode.substr(2), 16))}</button>`);
        btn.on('click', function() {
            $dialog.hide();
            doUserMove(from, to, piece);
        });
        $options.append(btn);
    });
    $dialog.show();
}

function doUserMove(from, to, promotion) {
    const move = game.move({
        from: from,
        to: to,
        promotion: promotion || 'q'
    });
    if (move === null) return 'snapback';
    updateStatus();
    if (game.turn() !== playerColor && !game.game_over()) {
        setTimeout(makeBotMove, 250);
    }
}

function onDrop(source, target) {
    // Check if the move is legal
    const moves = game.moves({ square: source, verbose: true });
    const legalTargets = moves.map(m => m.to);
    if (!legalTargets.includes(target)) {
        return 'snapback';
    }
    // Check for promotion
    const piece = game.get(source);
    if (piece && piece.type === 'p' && ((piece.color === 'w' && target[1] === '8') || (piece.color === 'b' && target[1] === '1'))) {
        // Show promotion dialog
        showPromotionDialog(source, target, piece.color);
        return;
    }
    // Normal move
    return doUserMove(source, target);
}

function onMoveEnd() {
    board.position(game.fen());
    board.orientation(getOrientationStr());
}

function onSnapEnd() {
    // No need to update board here if onMoveEnd is used
}

function updateStatus() {
    let status = '';
    let isPlayerTurn = (game.turn() === playerColor);

    if (game.in_checkmate()) {
        status = 'Game over, ' + (game.turn() === 'w' ? 'black' : 'white') + ' wins.';
        showGameOver();
    } else if (game.in_draw()) {
        status = 'Game over, drawn position';
        showGameOver();
    } else {
        status = (game.turn() === 'w' ? 'White' : 'Black') + ' to move';
        // Enable resign only on player's turn
        if (isPlayerTurn) {
            $('#resignBtn').prop('disabled', false);
        } else {
            $('#resignBtn').prop('disabled', true);
        }
    }

    $status.html(status);
}

function showGameOver() {
    $('#startBtn').show();
    $('#resignBtn').hide();
}

function resetGame() {
    // Reset the game state
    game = new Chess();
    playerColor = null;
    
    // Show color selection
    $('#color-selection').show();
    $('#startBtn').hide();
    $('#resignBtn').hide();
    $status.html('Select your color to start');
    
    // Reset the board
    if (board) {
        board.destroy();
    }
    
    // Initialize new board
    const config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        onMoveEnd: onMoveEnd,
        onMouseoverSquare: onMouseoverSquare,
        onMouseoutSquare: onMouseoutSquare,
        pieceTheme: 'https://chessboardjs.com/img/chesspieces/alpha/{piece}.png',
        orientation: 'white'
    };
    board = Chessboard('board', config);
}

function startNewGame() {
    game = new Chess();
    // Always destroy and recreate the board with correct orientation
    if (board) {
        board.destroy();
    }
    const orientationStr = getOrientationStr();
    const config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        onMoveEnd: onMoveEnd,
        onMouseoverSquare: onMouseoverSquare,
        onMouseoutSquare: onMouseoutSquare,
        pieceTheme: 'https://chessboardjs.com/img/chesspieces/alpha/{piece}.png',
        orientation: orientationStr
    };
    board = Chessboard('board', config);
    board.orientation(orientationStr); // Explicitly set orientation
    updateStatus();
    $('#resignBtn').show();
    $('#startBtn').hide();
    
    // If player is black, make bot's first move
    if (playerColor === 'b') {
        setTimeout(makeBotMove, 250);
    }
}

function selectColor(color) {
    playerColor = color;
    $('#color-selection').hide();
    $('#startBtn').show();
    $status.html('Click "New Game" to start playing as ' + (color === 'w' ? 'White' : 'Black'));
    // Do NOT create the board here!
}

// Initialize the board
const config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    onMoveEnd: onMoveEnd,
    onMouseoverSquare: onMouseoverSquare,
    onMouseoutSquare: onMouseoutSquare,
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/alpha/{piece}.png',
    orientation: 'white' // Default orientation
};
board = Chessboard('board', config);

// Add event listeners
$('#whiteBtn').on('click', () => selectColor('w'));
$('#blackBtn').on('click', () => selectColor('b'));
$('#startBtn').on('click', startNewGame);
$('#resignBtn').on('click', resetGame);

// Initial status update
updateStatus();

// Remove spinner functions and calls from makeBotMove
function makeBotMove() {
    $.ajax({
        url: '/api/move',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            fen: game.fen()
        }),
        success: function(data) {
            const move = data.move; // e.g., "c7c5"
            // Parse UCI move string to {from, to, promotion}
            const moveObj = {
                from: move.substring(0, 2),
                to: move.substring(2, 4)
            };
            if (move.length > 4) {
                moveObj.promotion = move[4];
            }
            game.move(moveObj);
            board.position(game.fen());
            board.orientation(getOrientationStr());
            updateStatus();
        },
        error: function(error) {
            console.error('Error making bot move:', error);
        }
    });
} 