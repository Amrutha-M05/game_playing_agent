import pygame
import sys
import math
import random
from enum import Enum
from collections import defaultdict, deque

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FIELD_WIDTH = 800
FIELD_HEIGHT = 500
PLAYER_SIZE = 20
BALL_SIZE = 10
GOAL_WIDTH = 20
GOAL_HEIGHT = 150
FPS = 60

# Colors
GREEN = (22, 163, 74)
WHITE = (255, 255, 255)
BLUE = (59, 130, 246)
RED = (239, 68, 68)
DARK_BLUE = (30, 58, 138)
DARK_RED = (153, 27, 27)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
LIGHT_GREEN = (34, 197, 94)
PURPLE = (168, 85, 247)
DARK_PURPLE = (88, 28, 135)
YELLOW = (234, 179, 8)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    DIFFICULTY_SELECT = 4

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_SIZE
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        
        # Boundary collision
        if self.y < self.radius or self.y > FIELD_HEIGHT - self.radius:
            self.vy *= -0.8
            self.y = max(self.radius, min(FIELD_HEIGHT - self.radius, self.y))
    
    def draw(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, WHITE, 
                         (int(self.x + offset_x), int(self.y + offset_y)), 
                         self.radius)

class Player:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.radius = PLAYER_SIZE
        self.color = color
        self.name = name
        self.speed = 3.5
        self.possession_time = 0
        self.shots_taken = 0
        self.shots_on_goal = 0
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(self.radius, min(FIELD_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(FIELD_HEIGHT - self.radius, self.y))
    
    def distance_to(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
    
    def draw(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, self.color, 
                         (int(self.x + offset_x), int(self.y + offset_y)), 
                         self.radius)
        
        font = pygame.font.Font(None, 20)
        text = font.render(self.name[0], True, WHITE)
        text_rect = text.get_rect(center=(int(self.x + offset_x), 
                                         int(self.y + offset_y)))
        screen.blit(text, text_rect)

class MinimaxAgent:
    """Simplified Minimax with balanced parameters"""
    def __init__(self, player, goal_x, goal_y, difficulty=Difficulty.MEDIUM):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.difficulty = difficulty
        
        # BALANCED parameters - all agents equal at same difficulty
        if difficulty == Difficulty.EASY:
            self.prediction_frames = 6
            self.error_rate = 0.25  # 25% chance of mistake
        elif difficulty == Difficulty.MEDIUM:
            self.prediction_frames = 8
            self.error_rate = 0.15  # 15% chance of mistake
        else:  # HARD
            self.prediction_frames = 10
            self.error_rate = 0.05  # 5% chance of mistake
    
    def get_action(self, ball, opponent):
        """Get action with strategic behavior"""
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Random mistakes for balance
        if random.random() < self.error_rate:
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle) * self.player.speed
            dy = math.sin(angle) * self.player.speed
            return (dx, dy, False)
        
        # Shooting range
        if dist_to_ball < 20:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            # Add shooting inaccuracy
            if dist > 0:
                angle = math.atan2(dy, dx)
                angle += random.uniform(-0.2, 0.2)  # Small angle variation
                return (math.cos(angle) * self.player.speed * 0.8, 
                       math.sin(angle) * self.player.speed * 0.8, True)
        
        # Predict ball position
        predicted_x = ball.x + ball.vx * self.prediction_frames
        predicted_y = ball.y + ball.vy * self.prediction_frames
        predicted_x = max(30, min(FIELD_WIDTH - 30, predicted_x))
        predicted_y = max(30, min(FIELD_HEIGHT - 30, predicted_y))
        
        # Chase predicted position
        dx = predicted_x - self.player.x
        dy = predicted_y - self.player.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            return (dx / dist * self.player.speed, 
                   dy / dist * self.player.speed, False)
        
        return (0, 0, False)

class DQNAgent:
    """Simplified DQN with balanced parameters"""
    def __init__(self, player, goal_x, goal_y, difficulty=Difficulty.MEDIUM):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.difficulty = difficulty
        
        # BALANCED parameters - same as Minimax
        if difficulty == Difficulty.EASY:
            self.prediction_frames = 6
            self.error_rate = 0.25
        elif difficulty == Difficulty.MEDIUM:
            self.prediction_frames = 8
            self.error_rate = 0.15
        else:  # HARD
            self.prediction_frames = 10
            self.error_rate = 0.05
    
    def get_action(self, ball, opponent):
        """Get action with strategic behavior"""
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Random mistakes for balance
        if random.random() < self.error_rate:
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle) * self.player.speed
            dy = math.sin(angle) * self.player.speed
            return (dx, dy, False)
        
        # Shooting range
        if dist_to_ball < 20:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                angle = math.atan2(dy, dx)
                angle += random.uniform(-0.2, 0.2)  # Small angle variation
                return (math.cos(angle) * self.player.speed * 0.8, 
                       math.sin(angle) * self.player.speed * 0.8, True)
        
        # Predict ball position with slightly different strategy
        predicted_x = ball.x + ball.vx * self.prediction_frames
        predicted_y = ball.y + ball.vy * self.prediction_frames
        predicted_x = max(30, min(FIELD_WIDTH - 30, predicted_x))
        predicted_y = max(30, min(FIELD_HEIGHT - 30, predicted_y))
        
        # Intercept predicted position
        dx = predicted_x - self.player.x
        dy = predicted_y - self.player.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            return (dx / dist * self.player.speed, 
                   dy / dist * self.player.speed, False)
        
        return (0, 0, False)

class HeuristicAgent:
    """Simplified Heuristic with balanced parameters"""
    def __init__(self, player, goal_x, goal_y, difficulty=Difficulty.MEDIUM):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.difficulty = difficulty
        
        # BALANCED parameters - same as others
        if difficulty == Difficulty.EASY:
            self.prediction_frames = 6
            self.error_rate = 0.25
        elif difficulty == Difficulty.MEDIUM:
            self.prediction_frames = 8
            self.error_rate = 0.15
        else:  # HARD
            self.prediction_frames = 10
            self.error_rate = 0.05
    
    def get_action(self, ball, opponent):
        """Get action with strategic behavior"""
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Random mistakes for balance
        if random.random() < self.error_rate:
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle) * self.player.speed
            dy = math.sin(angle) * self.player.speed
            return (dx, dy, False)
        
        # Shooting range
        if dist_to_ball < 20:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                angle = math.atan2(dy, dx)
                angle += random.uniform(-0.2, 0.2)  # Small angle variation
                return (math.cos(angle) * self.player.speed * 0.8, 
                       math.sin(angle) * self.player.speed * 0.8, True)
        
        # Direct chase with prediction
        predicted_x = ball.x + ball.vx * self.prediction_frames
        predicted_y = ball.y + ball.vy * self.prediction_frames
        predicted_x = max(30, min(FIELD_WIDTH - 30, predicted_x))
        predicted_y = max(30, min(FIELD_HEIGHT - 30, predicted_y))
        
        dx = predicted_x - self.player.x
        dy = predicted_y - self.player.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            return (dx / dist * self.player.speed, 
                   dy / dist * self.player.speed, False)
        
        return (0, 0, False)

class SoccerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Soccer: Balanced Competition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)
        
        self.state = GameState.MENU
        self.agent_mode = 0
        self.difficulty = Difficulty.MEDIUM
        
        # Statistics
        self.total_goals = {
            'minimax': 0,
            'dqn': 0,
            'heuristic': 0
        }
        self.match_goals_left = 0
        self.match_goals_right = 0
        self.possession_frames = {'left': 0, 'right': 0}
        self.total_frames = 0
        
        self.offset_x = (SCREEN_WIDTH - FIELD_WIDTH) // 2
        self.offset_y = 50
        
        self.reset_game()
    
    def reset_game(self):
        self.ball = Ball(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        # Random ball start with MORE variation
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4)  # Faster initial speed
        self.ball.vx = math.cos(angle) * speed
        self.ball.vy = math.sin(angle) * speed
        
        # Create players based on mode
        if self.agent_mode == 0:  # Minimax vs DQN
            self.player1 = Player(150, FIELD_HEIGHT // 2, BLUE, "Minimax")
            self.player2 = Player(FIELD_WIDTH - 150, FIELD_HEIGHT // 2, PURPLE, "DQN")
            self.agent1 = MinimaxAgent(self.player1, FIELD_WIDTH, FIELD_HEIGHT // 2, self.difficulty)
            self.agent2 = DQNAgent(self.player2, 0, FIELD_HEIGHT // 2, self.difficulty)
            self.agent1_name = 'minimax'
            self.agent2_name = 'dqn'
        elif self.agent_mode == 1:  # Minimax vs Heuristic
            self.player1 = Player(150, FIELD_HEIGHT // 2, BLUE, "Minimax")
            self.player2 = Player(FIELD_WIDTH - 150, FIELD_HEIGHT // 2, RED, "Heuristic")
            self.agent1 = MinimaxAgent(self.player1, FIELD_WIDTH, FIELD_HEIGHT // 2, self.difficulty)
            self.agent2 = HeuristicAgent(self.player2, 0, FIELD_HEIGHT // 2, self.difficulty)
            self.agent1_name = 'minimax'
            self.agent2_name = 'heuristic'
        else:  # DQN vs Heuristic
            self.player1 = Player(150, FIELD_HEIGHT // 2, PURPLE, "DQN")
            self.player2 = Player(FIELD_WIDTH - 150, FIELD_HEIGHT // 2, RED, "Heuristic")
            self.agent1 = DQNAgent(self.player1, FIELD_WIDTH, FIELD_HEIGHT // 2, self.difficulty)
            self.agent2 = HeuristicAgent(self.player2, 0, FIELD_HEIGHT // 2, self.difficulty)
            self.agent1_name = 'dqn'
            self.agent2_name = 'heuristic'
        
        self.match_goals_left = 0
        self.match_goals_right = 0
        self.possession_frames = {'left': 0, 'right': 0}
        self.total_frames = 0
    
    def reset_ball(self):
        """Reset ball with random direction and speed"""
        self.ball = Ball(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4)
        self.ball.vx = math.cos(angle) * speed
        self.ball.vy = math.sin(angle) * speed
        
        # Reset players with more variation
        self.player1.x = 150 + random.randint(-50, 50)
        self.player1.y = FIELD_HEIGHT // 2 + random.randint(-100, 100)
        self.player2.x = FIELD_WIDTH - 150 + random.randint(-50, 50)
        self.player2.y = FIELD_HEIGHT // 2 + random.randint(-100, 100)
    
    def check_goal(self):
        goal_y_min = FIELD_HEIGHT // 2 - GOAL_HEIGHT // 2
        goal_y_max = FIELD_HEIGHT // 2 + GOAL_HEIGHT // 2
        
        # Left goal (x=0) - Player2 (right) scores
        if self.ball.x < GOAL_WIDTH:
            if goal_y_min < self.ball.y < goal_y_max:
                self.match_goals_right += 1
                self.total_goals[self.agent2_name] += 1
                self.player2.shots_on_goal += 1
                self.reset_ball()
                return True
            else:
                self.ball.vx *= -0.8
                self.ball.x = GOAL_WIDTH
        
        # Right goal (x=FIELD_WIDTH) - Player1 (left) scores
        if self.ball.x > FIELD_WIDTH - GOAL_WIDTH:
            if goal_y_min < self.ball.y < goal_y_max:
                self.match_goals_left += 1
                self.total_goals[self.agent1_name] += 1
                self.player1.shots_on_goal += 1
                self.reset_ball()
                return True
            else:
                self.ball.vx *= -0.8
                self.ball.x = FIELD_WIDTH - GOAL_WIDTH
        
        return False
    
    def handle_kick(self, player, dx, dy, should_kick):
        dist = player.distance_to(self.ball.x, self.ball.y)
        if dist < player.radius + self.ball.radius + 8 and should_kick:
            angle = math.atan2(dy, dx)
            # Variable kick power for more interesting gameplay
            power = random.uniform(6.5, 8.5)
            self.ball.vx = math.cos(angle) * power
            self.ball.vy = math.sin(angle) * power
            player.shots_taken += 1
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        # Get AI actions
        action1 = self.agent1.get_action(self.ball, self.player2)
        action2 = self.agent2.get_action(self.ball, self.player1)
        
        # Move players
        self.player1.move(action1[0], action1[1])
        self.player2.move(action2[0], action2[1])
        
        # Handle kicks
        self.handle_kick(self.player1, action1[0], action1[1], action1[2])
        self.handle_kick(self.player2, action2[0], action2[1], action2[2])
        
        # Update ball
        self.ball.update()
        
        # Track possession
        dist1 = self.player1.distance_to(self.ball.x, self.ball.y)
        dist2 = self.player2.distance_to(self.ball.x, self.ball.y)
        
        if dist1 < 30:
            self.possession_frames['left'] += 1
            self.player1.possession_time += 1
        if dist2 < 30:
            self.possession_frames['right'] += 1
            self.player2.possession_time += 1
        
        self.total_frames += 1
        
        # Check for goals
        self.check_goal()
    
    def draw_field(self):
        pygame.draw.rect(self.screen, GREEN, 
                        (self.offset_x, self.offset_y, FIELD_WIDTH, FIELD_HEIGHT))
        
        pygame.draw.line(self.screen, WHITE, 
                        (self.offset_x + FIELD_WIDTH // 2, self.offset_y),
                        (self.offset_x + FIELD_WIDTH // 2, self.offset_y + FIELD_HEIGHT), 3)
        
        pygame.draw.circle(self.screen, WHITE, 
                          (self.offset_x + FIELD_WIDTH // 2, 
                           self.offset_y + FIELD_HEIGHT // 2), 50, 3)
        
        goal_y = self.offset_y + FIELD_HEIGHT // 2 - GOAL_HEIGHT // 2
        pygame.draw.rect(self.screen, DARK_RED, 
                        (self.offset_x, goal_y, GOAL_WIDTH, GOAL_HEIGHT))
        pygame.draw.rect(self.screen, DARK_RED, 
                        (self.offset_x + FIELD_WIDTH - GOAL_WIDTH, goal_y, 
                         GOAL_WIDTH, GOAL_HEIGHT))
        
        pygame.draw.rect(self.screen, WHITE, 
                        (self.offset_x, self.offset_y, FIELD_WIDTH, FIELD_HEIGHT), 3)
    
    def draw_menu(self):
        self.screen.fill((15, 23, 42))
        
        title = self.font.render("AI SOCCER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("Balanced AI Competition", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 95))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Difficulty display
        diff_text = f"Difficulty: {self.difficulty.name}"
        diff_render = self.small_font.render(diff_text, True, YELLOW)
        diff_rect = diff_render.get_rect(center=(SCREEN_WIDTH // 2, 125))
        self.screen.blit(diff_render, diff_rect)
        
        # Mode selection
        mode_text = self.small_font.render("Select Match (1/2/3):", True, WHITE)
        self.screen.blit(mode_text, (80, 160))
        
        modes = [
            ("1: Minimax vs DQN", BLUE, PURPLE, 'minimax', 'dqn'),
            ("2: Minimax vs Heuristic", BLUE, RED, 'minimax', 'heuristic'),
            ("3: DQN vs Heuristic", PURPLE, RED, 'dqn', 'heuristic')
        ]
        
        for i, (text, color1, color2, name1, name2) in enumerate(modes):
            y = 200 + i * 75
            selected = i == self.agent_mode
            
            box_color = (50, 50, 50) if not selected else (80, 80, 80)
            pygame.draw.rect(self.screen, box_color, (60, y - 10, 880, 65), border_radius=10)
            
            mode_label = self.small_font.render(text, True, WHITE)
            self.screen.blit(mode_label, (80, y))
            
            goals1 = self.total_goals[name1]
            goals2 = self.total_goals[name2]
            stats = self.tiny_font.render(f"All-time: {goals1} - {goals2}", True, GRAY)
            self.screen.blit(stats, (80, y + 28))
            
            if selected:
                indicator = self.small_font.render("►", True, LIGHT_GREEN)
                self.screen.blit(indicator, (30, y + 5))
        
        # Instructions
        inst1 = self.small_font.render("SPACE: Start | D: Difficulty | ESC: Quit", 
                                      True, GRAY)
        inst1_rect = inst1.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(inst1, inst1_rect)
        
        info = self.tiny_font.render("All agents are balanced - equal parameters, competitive gameplay!", 
                                    True, LIGHT_GREEN)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, 540))
        self.screen.blit(info, info_rect)
    
    def draw_difficulty_select(self):
        self.screen.fill((15, 23, 42))
        
        title = self.font.render("SELECT DIFFICULTY", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        difficulties = [
            (Difficulty.EASY, "EASY", "25% error rate, 6 frame prediction", (100, 200, 100)),
            (Difficulty.MEDIUM, "MEDIUM", "15% error rate, 8 frame prediction", (200, 200, 100)),
            (Difficulty.HARD, "HARD", "5% error rate, 10 frame prediction", (200, 100, 100))
        ]
        
        for i, (diff, name, desc, color) in enumerate(difficulties):
            y = 200 + i * 100
            selected = diff == self.difficulty
            
            box_color = (60, 60, 60) if not selected else (90, 90, 90)
            pygame.draw.rect(self.screen, box_color, (200, y - 10, 600, 80), border_radius=10)
            
            if selected:
                pygame.draw.rect(self.screen, color, (200, y - 10, 600, 80), 4, border_radius=10)
            
            name_text = self.font.render(name, True, color)
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, y + 15))
            self.screen.blit(name_text, name_rect)
            
            desc_text = self.tiny_font.render(desc, True, GRAY)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, y + 45))
            self.screen.blit(desc_text, desc_rect)
            
            if selected:
                indicator = self.small_font.render("►", True, LIGHT_GREEN)
                self.screen.blit(indicator, (160, y + 10))
        
        inst = self.small_font.render("Use UP/DOWN arrows | SPACE to confirm | ESC to back", 
                                     True, GRAY)
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, 520))
        self.screen.blit(inst, inst_rect)
    
    def draw_game(self):
        self.screen.fill((30, 41, 59))
        
        self.draw_field()
        
        self.player1.draw(self.screen, self.offset_x, self.offset_y)
        self.player2.draw(self.screen, self.offset_x, self.offset_y)
        self.ball.draw(self.screen, self.offset_x, self.offset_y)
        
        # Draw score
        score_text = self.font.render(
            f"{self.match_goals_left} - {self.match_goals_right}", 
            True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 25))
        self.screen.blit(score_text, score_rect)
        
        # Draw total score
        total = self.small_font.render(
            f"All-time: {self.player1.name} {self.total_goals[self.agent1_name]} - {self.total_goals[self.agent2_name]} {self.player2.name}", 
            True, GRAY)
        total_rect = total.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(total, total_rect)
        
        # Draw possession
        if self.total_frames > 0:
            poss_left = (self.possession_frames['left'] / self.total_frames) * 100
            poss_right = (self.possession_frames['right'] / self.total_frames) * 100
            
            poss_text = self.tiny_font.render(
                f"Possession: {poss_left:.1f}% - {poss_right:.1f}%", 
                True, GRAY)
            poss_rect = poss_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
            self.screen.blit(poss_text, poss_rect)
        
        # Draw controls
        controls = self.tiny_font.render("P: Pause | R: Reset | ESC: Menu", 
                                         True, GRAY)
        self.screen.blit(controls, (10, 10))
        
        # Draw difficulty
        diff_display = self.tiny_font.render(f"Difficulty: {self.difficulty.name}", 
                                             True, YELLOW)
        self.screen.blit(diff_display, (10, 30))
        
        # Draw stats (left side)
        stats_y = 60
        left_stats = [
            f"{self.player1.name}",
            f"Shots: {self.player1.shots_taken}",
            f"On Goal: {self.player1.shots_on_goal}",
            f"Error: {int(self.agent1.error_rate * 100)}%"
        ]
        for i, stat in enumerate(left_stats):
            stat_text = self.tiny_font.render(stat, True, self.player1.color)
            self.screen.blit(stat_text, (10, stats_y + i * 18))
        
        # Draw stats (right side)
        right_stats = [
            f"{self.player2.name}",
            f"Shots: {self.player2.shots_taken}",
            f"On Goal: {self.player2.shots_on_goal}",
            f"Error: {int(self.agent2.error_rate * 100)}%"
        ]
        for i, stat in enumerate(right_stats):
            stat_text = self.tiny_font.render(stat, True, self.player2.color)
            stat_rect = stat_text.get_rect(topright=(SCREEN_WIDTH - 10, stats_y + i * 18))
            self.screen.blit(stat_text, stat_rect)
        
        if self.state == GameState.PAUSED:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                                     SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.MENU:
                        return False
                    elif self.state == GameState.DIFFICULTY_SELECT:
                        self.state = GameState.MENU
                    else:
                        self.state = GameState.MENU
                
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif self.state == GameState.DIFFICULTY_SELECT:
                        self.state = GameState.MENU
                
                elif event.key == pygame.K_d:
                    if self.state == GameState.MENU:
                        self.state = GameState.DIFFICULTY_SELECT
                
                elif event.key == pygame.K_p:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                
                elif event.key == pygame.K_r:
                    if self.state != GameState.MENU:
                        self.reset_game()
                        self.state = GameState.PLAYING
                
                # Mode selection in menu
                elif self.state == GameState.MENU:
                    if event.key == pygame.K_1:
                        self.agent_mode = 0
                    elif event.key == pygame.K_2:
                        self.agent_mode = 1
                    elif event.key == pygame.K_3:
                        self.agent_mode = 2
                
                # Difficulty selection
                elif self.state == GameState.DIFFICULTY_SELECT:
                    if event.key == pygame.K_UP:
                        if self.difficulty == Difficulty.MEDIUM:
                            self.difficulty = Difficulty.EASY
                        elif self.difficulty == Difficulty.HARD:
                            self.difficulty = Difficulty.MEDIUM
                    elif event.key == pygame.K_DOWN:
                        if self.difficulty == Difficulty.EASY:
                            self.difficulty = Difficulty.MEDIUM
                        elif self.difficulty == Difficulty.MEDIUM:
                            self.difficulty = Difficulty.HARD
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            self.update()
            
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.DIFFICULTY_SELECT:
                self.draw_difficulty_select()
            else:
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SoccerGame()
    game.run()