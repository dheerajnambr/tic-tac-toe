import os
import tempfile
import webbrowser

# There are no external dependencies required for this script!
# It relies entirely on Python's standard library.

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Tic-Tac-Toe</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --accent-1: #38bdf8;
            --accent-2: #c084fc;
            --x-color: #f43f5e;
            --o-color: #10b981;
        }

        body {
            font-family: 'Outfit', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,0.5) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,0.5) 0, transparent 50%);
            color: var(--text-main);
            overflow: hidden;
        }

        .container {
            text-align: center;
            background: var(--glass-bg);
            padding: 3rem;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            animation: fadeIn 1s ease-out;
            position: relative;
            z-index: 10;
        }

        h1 {
            margin-top: 0;
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(to right, var(--accent-1), var(--accent-2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .ttt-icon {
            width: 55px;
            height: 55px;
            filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.5));
            animation: float-icon 3s ease-in-out infinite;
        }

        .grid-lines line {
            stroke-dasharray: 80;
            stroke-dashoffset: 80;
            animation: drawStroke 1s ease-out forwards;
        }
        
        .grid-lines line:nth-child(2) { animation-delay: 0.2s; }
        .grid-lines line:nth-child(3) { animation-delay: 0.4s; }
        .grid-lines line:nth-child(4) { animation-delay: 0.6s; }

        .x-mark line {
            stroke-dasharray: 30;
            stroke-dashoffset: 30;
            animation: drawStroke 0.5s ease-out forwards;
            animation-delay: 1.2s;
        }
        .x-mark line:nth-child(2) { animation-delay: 1.4s; }

        .o-mark {
            stroke-dasharray: 60;
            stroke-dashoffset: 60;
            animation: drawStroke 0.6s ease-out forwards;
            animation-delay: 1.6s;
        }

        @keyframes drawStroke {
            to { stroke-dashoffset: 0; }
        }

        @keyframes float-icon {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-8px) rotate(8deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        .status {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            font-weight: 500;
            min-height: 2rem;
            transition: all 0.3s ease;
        }

        .board {
            display: grid;
            grid-template-columns: repeat(3, 110px);
            grid-template-rows: repeat(3, 110px);
            gap: 15px;
            margin: 0 auto 2rem;
        }

        .cell {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            font-family: 'Outfit', sans-serif;
            font-size: 4rem;
            font-weight: 700;
            color: white;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
            padding: 0;
        }

        .cell:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2), inset 0 0 0 1px rgba(255, 255, 255, 0.2);
        }

        .cell:active {
            transform: translateY(0) scale(0.95);
        }

        .cell.x {
            color: var(--x-color);
            text-shadow: 0 0 20px rgba(244, 63, 94, 0.6);
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        .cell.o {
            color: var(--o-color);
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        .cell.win {
            background: rgba(255, 255, 255, 0.15);
            animation: pulseWin 1.5s infinite;
        }

        .reset-btn {
            padding: 12px 32px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(192, 132, 252, 0.4);
        }

        .reset-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(192, 132, 252, 0.6);
        }

        .watermark {
            position: fixed;
            bottom: 20px;
            right: 30px;
            font-size: 1.1rem;
            font-weight: 300;
            color: rgba(255, 255, 255, 0.4);
            letter-spacing: 2px;
            pointer-events: none;
            animation: fadeIn 2s ease-in 1s forwards;
            opacity: 0;
            z-index: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        .watermark span {
            font-weight: 700;
            color: rgba(255, 255, 255, 0.6);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes popIn {
            0% { opacity: 0; transform: scale(0.5) rotate(-15deg); }
            50% { transform: scale(1.1) rotate(5deg); }
            100% { opacity: 1; transform: scale(1) rotate(0); }
        }

        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(5deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        @keyframes pulseWin {
            0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); transform: scale(1); }
            50% { box-shadow: 0 0 20px 10px rgba(255, 255, 255, 0); transform: scale(1.05); }
            100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); transform: scale(1); }
        }

        /* Background floating orbs */
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            z-index: 1;
            opacity: 0.5;
            animation: floatOrb 20s infinite alternate;
        }

        .orb-1 {
            width: 300px;
            height: 300px;
            background: var(--accent-1);
            top: -100px;
            left: -100px;
        }

        .orb-2 {
            width: 400px;
            height: 400px;
            background: var(--accent-2);
            bottom: -150px;
            right: -150px;
            animation-delay: -5s;
        }

        @keyframes floatOrb {
            0% { transform: translate(0, 0); }
            100% { transform: translate(100px, 50px); }
        }
    </style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    
    <div class="container">
        <h1>
            <svg class="ttt-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="gridGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="var(--accent-1)" />
                        <stop offset="100%" stop-color="var(--accent-2)" />
                    </linearGradient>
                </defs>
                <g class="grid-lines" stroke="url(#gridGradient)" stroke-width="8" stroke-linecap="round">
                    <line x1="33" y1="15" x2="33" y2="85" />
                    <line x1="67" y1="15" x2="67" y2="85" />
                    <line x1="15" y1="33" x2="85" y2="33" />
                    <line x1="15" y1="67" x2="85" y2="67" />
                </g>
                <g class="x-mark" stroke="var(--x-color)" stroke-width="7" stroke-linecap="round">
                    <line x1="15" y1="15" x2="28" y2="28" />
                    <line x1="28" y1="15" x2="15" y2="28" />
                </g>
                <circle class="o-mark" cx="77" cy="77" r="8" stroke="var(--o-color)" stroke-width="7" fill="none"/>
            </svg>
            Tic-Tac-Toe
        </h1>
        <div class="status" id="status">Player X's turn</div>
        <div class="board" id="board">
            <button class="cell" data-index="0"></button>
            <button class="cell" data-index="1"></button>
            <button class="cell" data-index="2"></button>
            <button class="cell" data-index="3"></button>
            <button class="cell" data-index="4"></button>
            <button class="cell" data-index="5"></button>
            <button class="cell" data-index="6"></button>
            <button class="cell" data-index="7"></button>
            <button class="cell" data-index="8"></button>
        </div>
        <button class="reset-btn" id="reset">Reset Game</button>
    </div>

    <div class="watermark">Designed by <span>Dheeraj PT</span></div>

    <script>
        const cells = document.querySelectorAll('.cell');
        const statusText = document.getElementById('status');
        const resetBtn = document.getElementById('reset');
        
        let board = ["", "", "", "", "", "", "", "", ""];
        let currentPlayer = "X";
        let gameActive = true;

        const winningConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        function handleCellClick(e) {
            const cell = e.target;
            const index = parseInt(cell.getAttribute('data-index'));

            if (board[index] !== "" || !gameActive) return;

            board[index] = currentPlayer;
            cell.textContent = currentPlayer;
            cell.classList.add(currentPlayer.toLowerCase());

            checkWin();
        }

        function checkWin() {
            let roundWon = false;
            let winningCells = [];

            for (let i = 0; i < winningConditions.length; i++) {
                const [a, b, c] = winningConditions[i];
                if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                    roundWon = true;
                    winningCells = [a, b, c];
                    break;
                }
            }

            if (roundWon) {
                statusText.innerHTML = `Player <span style="color: var(--${currentPlayer.toLowerCase()}-color)">${currentPlayer}</span> Wins! 🎉`;
                winningCells.forEach(index => {
                    cells[index].classList.add('win');
                });
                gameActive = false;
                return;
            }

            if (!board.includes("")) {
                statusText.textContent = "It's a Draw! 🤝";
                gameActive = false;
                return;
            }

            currentPlayer = currentPlayer === "X" ? "O" : "X";
            statusText.textContent = `Player ${currentPlayer}'s turn`;
        }

        function restartGame() {
            board = ["", "", "", "", "", "", "", "", ""];
            currentPlayer = "X";
            gameActive = true;
            statusText.textContent = `Player ${currentPlayer}'s turn`;
            cells.forEach(cell => {
                cell.textContent = "";
                cell.classList.remove("x", "o", "win");
            });
        }

        cells.forEach(cell => cell.addEventListener('click', handleCellClick));
        resetBtn.addEventListener('click', restartGame);
    </script>
</body>
</html>
"""

def check_dependencies():
    """
    Since this script uses only standard libraries to generate an HTML file,
    there are no pip dependencies required!
    """
    print("Checking system dependencies...")
    print("✓ Standard library 'os' is available.")
    print("✓ Standard library 'tempfile' is available.")
    print("✓ Standard library 'webbrowser' is available.")
    print("All dependencies are built-in. Ready to run!\n")

def display_gui():
    check_dependencies()
    
    # Create a temporary HTML file
    fd, path = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, 'w') as f:
        f.write(HTML_CONTENT)
    
    # Open the file in the default web browser
    print(f"Launching the modern Tic-Tac-Toe GUI in your web browser...")
    webbrowser.open('file://' + os.path.realpath(path))

if __name__ == "__main__":
    display_gui()
