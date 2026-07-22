# Modern Tic-Tac-Toe

A polished browser-based Tic-Tac-Toe game built with HTML, CSS, and JavaScript.

## Features

- Responsive mouse-click interface
- Human vs. Human mode
- Easy, Medium, Hard, and Unbeatable AI
- Minimax with alpha-beta pruning
- Animated X and O marks
- Animated winning line
- Dark and light themes
- Sound effects using the Web Audio API
- Persistent scoreboard using `localStorage`
- Per-difficulty AI win-rate statistics
- Optional AI-first mode
- No external packages required

## Run locally

Open `index.html` directly, or run a small local server:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Deploy with GitHub Pages

1. Push the project to GitHub.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose the `main` branch and `/root`.
5. Save.

GitHub will provide a public URL for the game.

## Project structure

```text
index.html
styles.css
game.js
ai.js
README.md
```
