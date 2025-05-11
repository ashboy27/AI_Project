# Worst Chess Bot

A chess bot that intentionally makes the worst possible legal moves. Play against it and try to win!

## Features

- Interactive chess board interface
- Bot that makes the worst possible legal moves
- Real-time game status updates
- Responsive design

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy!

## How to Play

1. You play as White
2. The bot plays as Black
3. Make your moves by dragging and dropping pieces
4. The bot will automatically respond with the worst possible legal move
5. Try to checkmate the bot!

## Technologies Used

- Backend: Flask, Python-chess
- Frontend: HTML, CSS, JavaScript
- Chess Interface: chessboard.js, chess.js
- Deployment: Render
