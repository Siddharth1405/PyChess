# PyChess
♟️ Python chess game with Stockfish AI and Pygame GUI – play vs computer or friends locally!

---

# Chess Game with Pygame and Stockfish

![Chess Game Logo](screenshots/Main-menu.png)

A feature-rich chess implementation built with Python's Pygame library, powered by the Stockfish chess engine for AI gameplay. This project offers both single-player against computer and local two-player modes with intuitive graphical interface.

## Key Features

### Game Modes
- **Single Player**: Challenge the Stockfish AI at various difficulty levels  
  ![Chess Game Logo](screenshots/Difficulty-menu.png)
  ![Chess Game Logo](screenshots/Singleplayer.png)
- **Two Player**: Play locally against a friend with undo/redo functionality  
  ![Chess Game Logo](screenshots/Twoplayer.png)

### Gameplay Features
- Complete chess rules implementation including:
  - En passant
  - Castling
  - Pawn promotion with graphical selection menu  
    *(Screenshot 4: Promotion popup showing queen/rook/bishop/knight options)*
  - Check/checkmate detection
- Visual indicators:
  - Yellow highlight for selected pieces
  - Red highlight for king in checkmate  
    ![Chess Game Logo](screenshots/Checkmate.png)
- Turn indicator and game status display

## Installation

1. **Prerequisites**:
   ```bash
   pip install pygame python-chess
   ```

2. **Stockfish Setup**:
   - Download Stockfish from [official site](https://stockfishchess.org/download/)
   - Update engine path in code (line ~45):
     ```python
     engine_path = r"YOUR_PATH_TO\stockfish-windows-x86-64-avx2.exe"
     ```

3. **Run the game**:
   ```bash
   python my_chess_nubye.py
   ```

## How to Play

- **Piece Movement**: Click on a piece, then click on destination square
- **Special Moves**:
  - Castling: Move king two squares toward rook
  - Promotion: Automatic menu appears when pawn reaches back rank
   ![Chess Game Logo](screenshots/Pawn-promotion.png)
- **Game Controls**:
  - Undo/Redo available in two-player mode (bottom-right buttons)  
    ![Chess Game Logo](screenshots/Twoplayer.png)
  - After game ends, click to return to main menu

## Technical Details

- **Engine**: Uses Stockfish via python-chess UCI interface
- **AI Configuration**: Skill levels map to Stockfish's difficulty settings (0-20 scale)
- **Graphics**: All standard chess pieces with clean green/white board
