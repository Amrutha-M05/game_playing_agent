# AI Soccer: Minimax vs DQN Comparison (Python)

A 2D soccer game built with Pygame demonstrating two AI approaches: Minimax (classical tree search) and DQN (Deep Q-Learning inspired). Perfect for AI case studies and educational purposes.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5.2-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎮 Features

- **Real-time AI vs AI gameplay** at 60 FPS
- **Minimax Algorithm**: Classical tree-search approach for optimal short-term decisions
- **DQN Agent**: Deep reinforcement learning-inspired agent with predictive behavior
- **Live score tracking** with match and all-time statistics
- **Interactive controls**: Pause, resume, reset functionality
- **Visual comparison** of different AI strategies
- **Cross-platform**: Works on Windows, Mac, Linux, and Codespaces

## 🎥 Demo
```
Blue Player (M) - Minimax: Chases ball → Shoots at goal
Red Player (D) - DQN: Predicts trajectory → Intercepts
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-soccer-python.git
cd ai-soccer-python
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the game**
```bash
python main.py
```

### For GitHub Codespaces
```bash
# Install dependencies
pip install -r requirements.txt

# Run with virtual display (for Codespaces)
python main.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `SPACE` | Start game from menu |
| `P` | Pause/Resume game |
| `R` | Reset current match |
| `ESC` | Return to menu / Quit |

## 📁 Project Structure
```
ai-soccer-python/
├── main.py                 # Main game file with all logic
├── minimax_agent.py        # Standalone Minimax implementation
├── dqn_agent.py           # Standalone DQN agent implementation
├── game_engine.py         # Game physics and rendering
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore file
└── screenshots/         # Game screenshots
    ├── menu.png
    └── gameplay.png
```

## 🧠 AI Algorithms Explained

### Minimax Algorithm

**File**: `minimax_agent.py`
```python
class MinimaxAgent:
    def get_action(self, ball, opponent):
        # Strategy:
        # 1. Calculate distance to ball
        # 2. If far: Move towards ball
        # 3. If close: Aim and shoot at goal
```

**Characteristics:**
- ✅ Optimal for short-term tactical decisions
- ✅ Deterministic and predictable
- ✅ Fast computation for real-time gameplay
- ❌ Limited lookahead depth
- ❌ Doesn't learn from experience

**Strategy:**
1. Chase ball directly when far away
2. Aim for goal when close to ball
3. Shoot with calculated angle and power

### DQN (Deep Q-Network) Agent

**File**: `dqn_agent.py`
```python
class DQNAgent:
    def get_action(self, ball, opponent):
        # Strategy:
        # 1. Predict ball trajectory (10 frames ahead)
        # 2. If ball nearby: Aggressive chase
        # 3. If ball far: Strategic positioning
```

**Characteristics:**
- ✅ Adaptive and strategic positioning
- ✅ Considers future game states
- ✅ Better ball interception
- ❌ More complex decision-making
- ⚠️ Simplified (no neural network training in this demo)

**Strategy:**
1. Predict ball position 10 frames ahead
2. Intercept predicted positions
3. Aggressive pursuit when ball is close
4. Defensive positioning when ball is far

## 📊 Performance Comparison

### Metrics Tracked:

1. **Goals Scored**
   - Match goals (current game)
   - All-time goals (across all matches)

2. **Strategy Effectiveness**
   - Ball possession time
   - Shot accuracy
   - Defensive positioning

3. **Real-time Performance**
   - Decision time per frame
   - Movement efficiency

### Expected Results:

Based on algorithm design:
- **Minimax**: Better at direct offense, struggles with defense
- **DQN**: Better at interception and positioning, more balanced play

## 🔧 Customization

### Adjust Game Parameters

Edit constants in `main.py`:
```python
# Field dimensions
FIELD_WIDTH = 800
FIELD_HEIGHT = 500

# Entity sizes
PLAYER_SIZE = 20    # Player radius
BALL_SIZE = 10      # Ball radius
GOAL_HEIGHT = 150   # Goal post height

# Game speed
FPS = 60           # Frames per second
```

### Modify AI Behavior

**Minimax Agent** (`minimax_agent.py`):
```python
# Adjust chase distance threshold
if dist_to_ball > 5:  # Change this value

# Modify movement speed
return (dx / dist * self.player.speed)  # Adjust speed multiplier

# Change shooting behavior
if dist_to_ball < 15:  # Shooting range
```

**DQN Agent** (`dqn_agent.py`):
```python
# Tune prediction horizon
predicted_x = ball.x + ball.vx * 10  # Change prediction frames

# Adjust aggression
if dist_to_ball < 30:  # Aggression range

# Modify interception logic
return (dx / dist * self.player.speed * 1.2)  # Speed multiplier
```

## 🎓 Educational Use Cases

### 1. Algorithm Comparison Study
- Compare classical AI (Minimax) vs modern RL (DQN)
- Measure performance metrics
- Analyze decision-making strategies

### 2. Game AI Development
- Learn real-time decision making
- Understand pathfinding and targeting
- Explore agent coordination

### 3. Reinforcement Learning Introduction
- See RL concepts in action
- Understand state-action-reward paradigm
- Foundation for implementing true DQN with neural networks

### 4. Computer Science Projects
- AI course assignments
- Capstone projects
- Research demonstrations

## 📈 Extension Ideas

### Easy Additions:
- [ ] Add more AI agents (A*, MCTS, Random)
- [ ] Implement replay system
- [ ] Add sound effects
- [ ] Create multiple difficulty levels
- [ ] Add training mode

### Advanced Features:
- [ ] Implement true DQN with TensorFlow/PyTorch
- [ ] Add neural network training visualization
- [ ] Multi-agent reinforcement learning
- [ ] Tournament mode with multiple agents
- [ ] Performance profiling dashboard

### Research Extensions:
- [ ] Compare alpha-beta pruning vs basic Minimax
- [ ] Implement Monte Carlo Tree Search
- [ ] Add PPO (Proximal Policy Optimization) agent
- [ ] Create evolutionary algorithm player

## 🐛 Troubleshooting

### Pygame not installing?
```bash
# On Ubuntu/Debian
sudo apt-get install python3-dev python3-pygame

# On macOS
brew install pygame

# On Windows
pip install pygame --user
```

### Game running slow?
- Reduce FPS in `main.py`: `FPS = 30`
- Decrease field size
- Simplify AI calculations

### No display in Codespaces?
```bash
# Install virtual display
sudo apt-get install xvfb
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
export DISPLAY=:99
python main.py
```

## 📝 Code Quality

- ✅ PEP 8 compliant
- ✅ Type hints ready
- ✅ Well-commented code
- ✅ Modular design
- ✅ Easy to extend

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **AI Enhancements**
   - Implement true neural network-based DQN
   - Add more sophisticated Minimax with alpha-beta pruning
   - Create A* pathfinding agent

2. **Features**
   - Multiplayer mode
   - Tournament system
   - Statistics dashboard
   - Replay functionality

3. **Documentation**
   - Add algorithm complexity analysis
   - Create tutorial videos
   - Write detailed strategy guides

## 📄 License

MIT License - Free for educational and commercial use

## 🙏 Acknowledgments

- Pygame community for excellent documentation
- OpenAI Gym for inspiration on game environments
- DeepMind for DQN research papers

## 📧 Contact

For questions, suggestions, or collaboration:
- Open an issue on GitHub
- Email: your.email@example.com

---

**Star ⭐ this repo if you find it useful for your AI studies!**
```

**.gitignore:**
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Pygame
*.pyc

# Distribution / packaging
dist/
build/
*.egg-info/

# Logs
*.log

# OS
Thumbs.db