const WINNING_LINES = [
  [0,1,2], [3,4,5], [6,7,8],
  [0,3,6], [1,4,7], [2,5,8],
  [0,4,8], [2,4,6]
];

function getWinner(board) {
  for (const [a,b,c] of WINNING_LINES) {
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return { symbol: board[a], line: [a,b,c] };
    }
  }
  return null;
}

function availableMoves(board) {
  return board.map((value, index) => value ? null : index).filter(v => v !== null);
}

function findWinningMove(board, symbol) {
  for (const move of availableMoves(board)) {
    board[move] = symbol;
    const result = getWinner(board);
    board[move] = "";
    if (result && result.symbol === symbol) return move;
  }
  return null;
}

function chooseAIMove(board, difficulty, symbol="O") {
  const moves = availableMoves(board);
  if (!moves.length) return null;

  if (difficulty === "easy") {
    return moves[Math.floor(Math.random() * moves.length)];
  }

  if (difficulty === "medium") {
    return (
      findWinningMove(board, symbol) ??
      findWinningMove(board, symbol === "X" ? "O" : "X") ??
      moves[Math.floor(Math.random() * moves.length)]
    );
  }

  if (difficulty === "hard") {
    const opponent = symbol === "X" ? "O" : "X";
    const tactical = findWinningMove(board, symbol) ?? findWinningMove(board, opponent);
    if (tactical !== null) return tactical;
    if (moves.includes(4)) return 4;

    const corners = [0,2,6,8].filter(i => moves.includes(i));
    if (corners.length) return corners[Math.floor(Math.random() * corners.length)];
    return moves[Math.floor(Math.random() * moves.length)];
  }

  let bestScore = -Infinity;
  let bestMoves = [];

  for (const move of moves) {
    board[move] = symbol;
    const score = minimax(board, false, symbol, 0, -Infinity, Infinity);
    board[move] = "";

    if (score > bestScore) {
      bestScore = score;
      bestMoves = [move];
    } else if (score === bestScore) {
      bestMoves.push(move);
    }
  }

  return bestMoves[Math.floor(Math.random() * bestMoves.length)];
}

function minimax(board, maximizing, aiSymbol, depth, alpha, beta) {
  const result = getWinner(board);
  const opponent = aiSymbol === "X" ? "O" : "X";

  if (result?.symbol === aiSymbol) return 10 - depth;
  if (result?.symbol === opponent) return depth - 10;
  if (!availableMoves(board).length) return 0;

  if (maximizing) {
    let best = -Infinity;
    for (const move of availableMoves(board)) {
      board[move] = aiSymbol;
      best = Math.max(best, minimax(board, false, aiSymbol, depth + 1, alpha, beta));
      board[move] = "";
      alpha = Math.max(alpha, best);
      if (beta <= alpha) break;
    }
    return best;
  }

  let best = Infinity;
  for (const move of availableMoves(board)) {
    board[move] = opponent;
    best = Math.min(best, minimax(board, true, aiSymbol, depth + 1, alpha, beta));
    board[move] = "";
    beta = Math.min(beta, best);
    if (beta <= alpha) break;
  }
  return best;
}
