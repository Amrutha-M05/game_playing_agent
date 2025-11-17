# 🤖⚽ AI Soccer - Algorithm Comparison Game

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

An AI soccer game showcasing different artificial intelligence algorithms competing against each other in real-time. Watch **Minimax**, **DQN**, and **Heuristic** agents battle it out on the field!

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [AI Algorithms](#ai-algorithms)
- [Game Mechanics](#game-mechanics)
- [Testing](#testing)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)


## 🎯 Overview

AI Soccer is an interactive demonstration of different AI decision-making algorithms in a competitive environment. The game features three distinct AI agents, each using different strategies to control virtual soccer players. All agents are **carefully balanced** to ensure fair and competitive matches.

### Key Highlights

- ✅ **Three AI Algorithms**: Minimax, DQN-inspired, and Heuristic agents
- ✅ **Balanced Gameplay**: All agents have equal parameters for fair competition
- ✅ **Educational**: Perfect for studying AI algorithms in action
- ✅ **Interactive**: Real-time statistics and match tracking
- ✅ **Three Difficulty Levels**: Easy, Medium, and Hard
- ✅ **Comprehensive Testing**: Full test suite included

## ✨ Features

### 🤖 AI Agents

1. **Minimax Agent** (Blue)
   - Uses game tree search principles
   - 8-frame ball trajectory prediction
   - Strategic positioning and optimal moves
   
2. **DQN Agent** (Purple)
   - Inspired by Deep Q-Network principles
   - 10-frame ball trajectory prediction
   - Adaptive learning-based behavior
   
3. **Heuristic Agent** (Red)
   - Rule-based decision making
   - 10-frame ball trajectory prediction
   - Defensive and offensive positioning

### 🎮 Game Features

- **Multiple Match Types**: 
  - Minimax vs DQN
  - Minimax vs Heuristic
  - DQN vs Heuristic
  
- **Difficulty Levels**:
  - **Easy**: 25% error rate, 6-frame prediction
  - **Medium**: 15% error rate, 8-frame prediction
  - **Hard**: 5% error rate, 10-frame prediction

- **Real-time Statistics**:
  - Live score tracking
  - Possession percentages
  - Shots taken vs shots on goal
  - All-time match history

- **Game Controls**:
  - Pause/Resume functionality
  - Match reset
  - Difficulty selection
  - Mode switching

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Amrutha-M05/ai-soccer.git
cd ai-soccer
```

### Step 2: Install Dependencies

```bash
pip install pygame
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Game

```bash
python ai_soccer_complete.py
```

## 🎮 Usage

### Controls

**Main Menu:**
- `1/2/3` - Select match type
- `D` - Open difficulty settings
- `SPACE` - Start game
- `ESC` - Quit

**In-Game:**
- `P` - Pause/Resume
- `R` - Reset match
- `ESC` - Return to menu

**Difficulty Selection:**
- `UP/DOWN` - Change difficulty
- `SPACE` - Confirm
- `ESC` - Back to menu

### Running Tests

Run the comprehensive test suite:

```bash
python test.py
```

The test suite validates:
- Agent parameter balance
- Shooting behavior
- Movement speeds
- Ball physics
- Goal detection
- Match simulations

## 🧠 AI Algorithms

### Minimax Agent

**Strategy**: Tree search with lookahead planning

```python
# Key characteristics
- Prediction frames: 8 (Medium difficulty)
- Error rate: 15% (Medium difficulty)
- Shooting range: < 20 pixels
- Approach: Predicts opponent moves and ball trajectory
```

**Decision Process**:
1. Evaluate current game state
2. Predict ball and opponent positions
3. Calculate optimal move direction
4. Execute movement and shooting

### DQN Agent

**Strategy**: Q-Learning inspired decision making

```python
# Key characteristics
- Prediction frames: 10 (Medium difficulty)
- Error rate: 15% (Medium difficulty)
- Shooting range: < 20 pixels
- Approach: Trajectory prediction with adaptive behavior
```

**Decision Process**:
1. Analyze ball velocity and position
2. Predict future ball location
3. Intercept predicted position
4. Shoot when in range

### Heuristic Agent

**Strategy**: Rule-based tactical decisions

```python
# Key characteristics
- Prediction frames: 10 (Medium difficulty)
- Error rate: 15% (Medium difficulty)
- Shooting range: < 20 pixels
- Approach: Hand-crafted rules and positioning
```

**Decision Process**:
1. Check distance to ball
2. Predict ball trajectory
3. Chase or defend based on situation
4. Shoot when opportunity arises

## ⚙️ Game Mechanics

### Ball Physics

```python
# Ball movement
- Velocity decay: 0.98 per frame (2% friction)
- Boundary collision: 80% velocity retention
- Kick power: 6.5-8.5 (variable)
- Starting speed: 2-4 units
```

### Player Movement

```python
# Player properties
- Base speed: 3.5 units/frame
- Player radius: 20 pixels
- Shooting range: < 20 pixels
- Kick detection: 8 pixels from ball
```

### Scoring System

```python
# Goal detection
- Goal width: 20 pixels
- Goal height: 150 pixels
- Left goal (x=0): Right team scores
- Right goal (x=800): Left team scores
```

### Balance System

All agents share equal parameters at the same difficulty:

| Parameter  | Easy | Medium| Hard  |
|----------- |------|-------|------ |
| Error Rate | 25% | 15%    | 5%    |
| Prediction | 6f  | 8-10f  | 10-12f|
| Base Speed | 3.5 | 3.5    | 3.5   |
| Shoot Range|<20px| <20px  | <20px |

## 🧪 Testing

### Test Suite Coverage

```bash
# Run all tests
python test.py

# Test categories:
✓ Agent parameter balance (3 tests)
✓ Shooting behavior (3 tests)
✓ Movement speeds (2 tests)
✓ Ball physics (3 tests)
✓ Goal detection (3 tests)
✓ Match simulation (3 tests)
```

### Expected Test Results

```
Total Tests: 15
Passed: 15 (100.0%)
Failed: 0 (0.0%)
```

## 📸 Screenshots

```
Main Menu:
┌─────────────────────────────────────┐
│           AI SOCCER                 │
│   Balanced AI Competition           │
│                                     │
│  Difficulty: MEDIUM                 │
│                                     │
│  ► 1: Minimax vs DQN                │
│     All-time: 5 - 4                 │
│                                     │
│    2: Minimax vs Heuristic          │
│     All-time: 3 - 3                 │
│                                     │
│    3: DQN vs Heuristic              │
│     All-time: 4 - 5                 │
│                                     │
│  SPACE: Start | D: Difficulty       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Minimax        3 - 2        DQN    │
│  ┌─────────────────────────────┐    │
│  │         [Soccer Field]      │    │
│  │  🔵         ⚪      🟣     │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│  Possession: 52.3% - 47.7%          │
│  All-time: Minimax 15 - 13 DQN      │
└─────────────────────────────────────┘
```

## 📁 Project Structure

```
ai-soccer/
│
├── ai_soccer_complete.py    # Main game file
├── test.py                  # Test suite
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
│
└── screenshots/       # Game screenshots
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   python test.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR
- Keep agents balanced (equal parameters)

## 🐛 Known Issues

- Occasionally players may get stuck at field boundaries
- Very fast ball speeds may cause collision detection issues
- Goal detection may fail if ball moves too quickly

## 🔮 Future Enhancements

- [ ] Add neural network-based DQN implementation
- [ ] Implement true minimax with alpha-beta pruning
- [ ] Add replay system
- [ ] Include training mode for agents
- [ ] Add sound effects and music
- [ ] Multiplayer mode (human vs AI)
- [ ] Tournament mode with brackets
- [ ] Save/load game statistics
- [ ] Export match recordings

## 📖 References

- [Minimax Algorithm](https://en.wikipedia.org/wiki/Minimax)
- [Deep Q-Networks (DQN)](https://arxiv.org/abs/1312.5602)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python AI Game Development](https://realpython.com/pygame-a-primer/)


