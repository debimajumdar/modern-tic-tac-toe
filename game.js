const cells = [...document.querySelectorAll(".cell")];
const modeButtons = [...document.querySelectorAll(".mode-card")];
const turnLabel = document.getElementById("turn-label");
const statusPill = document.getElementById("status-pill");
const winningLine = document.getElementById("winning-line");
const winningLineElement = winningLine.querySelector("line");
const newRoundButton = document.getElementById("new-round");
const swapFirstButton = document.getElementById("swap-first");
const themeButton = document.getElementById("theme-toggle");
const soundButton = document.getElementById("sound-toggle");
const resetScoresButton = document.getElementById("reset-scores");
const toast = document.getElementById("toast");

let board = Array(9).fill("");
let currentPlayer = "X";
let mode = "medium";
let gameOver = false;
let aiThinking = false;
let aiStarts = false;
let soundEnabled = true;

const defaultStats = () => ({
  overall: { xWins: 0, oWins: 0, draws: 0, games: 0 },
  ai: {
    easy: { games: 0, humanWins: 0, aiWins: 0, draws: 0 },
    medium: { games: 0, humanWins: 0, aiWins: 0, draws: 0 },
    hard: { games: 0, humanWins: 0, aiWins: 0, draws: 0 },
    unbeatable: { games: 0, humanWins: 0, aiWins: 0, draws: 0 }
  }
});

let stats = loadStats();

function loadStats() {
  try {
    return JSON.parse(localStorage.getItem("modernTicTacToeStats")) || defaultStats();
  } catch {
    return defaultStats();
  }
}

function saveStats() {
  localStorage.setItem("modernTicTacToeStats", JSON.stringify(stats));
}

function playTone(frequency=420, duration=0.08) {
  if (!soundEnabled) return;
  try {
    const context = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.frequency.value = frequency;
    oscillator.type = "sine";
    gain.gain.setValueAtTime(0.05, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + duration);
    oscillator.connect(gain).connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + duration);
  } catch {}
}

function renderBoard() {
  cells.forEach((cell, index) => {
    cell.innerHTML = "";
    cell.disabled = Boolean(board[index]) || gameOver || aiThinking;

    if (board[index]) {
      const mark = document.createElement("span");
      mark.className = `mark ${board[index].toLowerCase()}`;
      cell.appendChild(mark);
    }
  });
}

function updateStatus(message) {
  if (message) {
    statusPill.textContent = message;
    return;
  }

  if (gameOver) return;

  if (mode === "human") {
    turnLabel.textContent = `Player ${currentPlayer}`;
    statusPill.textContent = "Your move";
  } else if (currentPlayer === "X") {
    turnLabel.textContent = "Player X";
    statusPill.textContent = "Your move";
  } else {
    turnLabel.textContent = `${capitalize(mode)} AI`;
    statusPill.textContent = aiThinking ? "Thinking..." : "AI turn";
  }
}

function makeMove(index) {
  if (gameOver || aiThinking || board[index]) return;

  board[index] = currentPlayer;
  playTone(currentPlayer === "X" ? 460 : 350);
  renderBoard();

  const result = getWinner(board);
  if (result) return finishGame(result.symbol, result.line);

  if (!availableMoves(board).length) return finishGame(null, null);

  currentPlayer = currentPlayer === "X" ? "O" : "X";
  updateStatus();

  if (mode !== "human" && currentPlayer === "O") {
    aiThinking = true;
    updateStatus();
    renderBoard();

    setTimeout(() => {
      const move = chooseAIMove(board, mode, "O");
      aiThinking = false;
      if (move !== null) makeMove(move);
    }, 500);
  }
}

function finishGame(winner, line) {
  gameOver = true;

  if (winner) {
    turnLabel.textContent = `Player ${winner} wins`;
    statusPill.textContent = winner === "X" ? "Victory!" : "Game over";
    drawWinningLine(line);
    playTone(winner === "X" ? 640 : 260, 0.18);
  } else {
    turnLabel.textContent = "Draw game";
    statusPill.textContent = "Well played";
    playTone(300, 0.15);
  }

  recordResult(winner);
  renderBoard();
}

function drawWinningLine(line) {
  const centers = [
    [50,50], [150,50], [250,50],
    [50,150], [150,150], [250,150],
    [50,250], [150,250], [250,250]
  ];

  const [start, , end] = line;
  const [x1,y1] = centers[start];
  const [x2,y2] = centers[end];

  winningLineElement.setAttribute("x1", x1);
  winningLineElement.setAttribute("y1", y1);
  winningLineElement.setAttribute("x2", x2);
  winningLineElement.setAttribute("y2", y2);
  winningLine.classList.add("show");
}

function recordResult(winner) {
  const overall = stats.overall;
  overall.games += 1;

  if (winner === "X") overall.xWins += 1;
  else if (winner === "O") overall.oWins += 1;
  else overall.draws += 1;

  if (mode !== "human") {
    const aiStats = stats.ai[mode];
    aiStats.games += 1;
    if (winner === "X") aiStats.humanWins += 1;
    else if (winner === "O") aiStats.aiWins += 1;
    else aiStats.draws += 1;
  }

  saveStats();
  renderStats();
}

function renderStats() {
  document.getElementById("x-wins").textContent = stats.overall.xWins;
  document.getElementById("o-wins").textContent = stats.overall.oWins;
  document.getElementById("draws").textContent = stats.overall.draws;
  document.getElementById("games").textContent = stats.overall.games;

  const container = document.getElementById("ai-stats");
  container.innerHTML = "";

  ["easy", "medium", "hard", "unbeatable"].forEach(level => {
    const s = stats.ai[level];
    const winRate = s.games ? Math.round((s.aiWins / s.games) * 100) : 0;

    const row = document.createElement("div");
    row.className = "stat-row";
    row.innerHTML = `
      <span>${capitalize(level)}</span>
      <div class="stat-track"><div class="stat-fill" style="width:${winRate}%"></div></div>
      <span class="stat-value">${winRate}%</span>
    `;
    container.appendChild(row);
  });
}

function newRound() {
  board = Array(9).fill("");
  gameOver = false;
  aiThinking = false;
  currentPlayer = aiStarts && mode !== "human" ? "O" : "X";
  winningLine.classList.remove("show");
  renderBoard();
  updateStatus();

  if (currentPlayer === "O") {
    aiThinking = true;
    updateStatus();
    setTimeout(() => {
      const move = chooseAIMove(board, mode, "O");
      aiThinking = false;
      makeMove(move);
    }, 500);
  }
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 1700);
}

function capitalize(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

cells.forEach(cell => {
  cell.addEventListener("click", () => makeMove(Number(cell.dataset.index)));
});

modeButtons.forEach(button => {
  button.addEventListener("click", () => {
    mode = button.dataset.mode;
    modeButtons.forEach(item => item.classList.toggle("active", item === button));
    swapFirstButton.hidden = mode === "human";
    newRound();
    showToast(`${button.querySelector("strong").textContent} selected`);
  });
});

newRoundButton.addEventListener("click", newRound);

swapFirstButton.addEventListener("click", () => {
  aiStarts = !aiStarts;
  swapFirstButton.textContent = aiStarts ? "You start" : "AI starts";
  newRound();
});

themeButton.addEventListener("click", () => {
  document.body.classList.toggle("light");
  const light = document.body.classList.contains("light");
  themeButton.textContent = light ? "🌙" : "☀️";
  localStorage.setItem("modernTicTacToeTheme", light ? "light" : "dark");
});

soundButton.addEventListener("click", () => {
  soundEnabled = !soundEnabled;
  soundButton.textContent = soundEnabled ? "🔊" : "🔇";
});

resetScoresButton.addEventListener("click", () => {
  if (!confirm("Reset all saved scores and AI statistics?")) return;
  stats = defaultStats();
  saveStats();
  renderStats();
  showToast("Scores reset");
});

if (localStorage.getItem("modernTicTacToeTheme") === "light") {
  document.body.classList.add("light");
  themeButton.textContent = "🌙";
}

renderBoard();
renderStats();
updateStatus();
