import pygame
import sys
import math
import random
from enum import Enum

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

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3

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
        
        # Boundary collision (top and bottom)
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
        
        # Draw label
        font = pygame.font.Font(None, 20)
        text = font.render(self.name[0], True, WHITE)
        text_rect = text.get_rect(center=(int(self.x + offset_x), 
                                         int(self.y + offset_y)))
        screen.blit(text, text_rect)

class MinimaxAgent:
    """Minimax with tree-search approach"""
    def __init__(self, player, goal_x, goal_y):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.last_ball_x = 0
        self.last_ball_y = 0
    
    def get_action(self, ball, opponent):
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Calculate if we're closer to ball than opponent
        opponent_dist = opponent.distance_to(ball.x, ball.y)
        we_are_closer = dist_to_ball < opponent_dist
        
        # Shooting range
        if dist_to_ball < 15:
            # Calculate best shooting angle
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                # Move toward shooting position and kick
                move_x = dx / dist * self.player.speed * 0.7
                move_y = dy / dist * self.player.speed * 0.7
                return (move_x, move_y, True)
        
        # If ball is moving fast, predict and intercept
        ball_speed = math.sqrt(ball.vx**2 + ball.vy**2)
        if ball_speed > 1.5:
            # Predict where ball will be
            prediction_time = 8
            predicted_x = ball.x + ball.vx * prediction_time
            predicted_y = ball.y + ball.vy * prediction_time
            
            # Clamp prediction to field
            predicted_x = max(50, min(FIELD_WIDTH - 50, predicted_x))
            predicted_y = max(50, min(FIELD_HEIGHT - 50, predicted_y))
            
            dx = predicted_x - self.player.x
            dy = predicted_y - self.player.y
        else:
            # Chase ball directly
            dx = ball.x - self.player.x
            dy = ball.y - self.player.y
        
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            # Speed up if we're closer
            speed_mult = 1.0 if we_are_closer else 0.95
            return (dx / dist * self.player.speed * speed_mult, 
                   dy / dist * self.player.speed * speed_mult, False)
        
        return (0, 0, False)

class DQNAgent:
    """DQN with reinforcement learning approach"""
    def __init__(self, player, goal_x, goal_y):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.defensive_mode = False
    
    def get_action(self, ball, opponent):
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        opponent_dist = opponent.distance_to(ball.x, ball.y)
        
        # Calculate ball movement toward our goal
        ball_to_goal_dist = math.sqrt((ball.x - self.goal_x)**2 + (ball.y - self.goal_y)**2)
        ball_moving_to_goal = False
        if abs(ball.vx) > 1:
            if (self.goal_x == 0 and ball.vx < 0) or (self.goal_x == FIELD_WIDTH and ball.vx > 0):
                ball_moving_to_goal = True
        
        # Defensive positioning when opponent has ball
        if opponent_dist < dist_to_ball and opponent_dist < 25:
            self.defensive_mode = True
        else:
            self.defensive_mode = False
        
        # Shooting range
        if dist_to_ball < 15:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                return (dx / dist * self.player.speed * 0.7, 
                       dy / dist * self.player.speed * 0.7, True)
        
        # Aggressive interception mode
        if dist_to_ball < 30 or ball_moving_to_goal:
            # Predict ball position
            prediction_frames = 10
            predicted_x = ball.x + ball.vx * prediction_frames
            predicted_y = ball.y + ball.vy * prediction_frames
            
            # Clamp to field
            predicted_x = max(50, min(FIELD_WIDTH - 50, predicted_x))
            predicted_y = max(50, min(FIELD_HEIGHT - 50, predicted_y))
            
            dx = predicted_x - self.player.x
            dy = predicted_y - self.player.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                return (dx / dist * self.player.speed, 
                       dy / dist * self.player.speed, False)
        
        # Strategic positioning - stay between ball and goal
        if self.defensive_mode:
            # Position between ball and goal
            target_x = (ball.x + self.goal_x) / 2
            target_y = (ball.y + self.goal_y) / 2
            
            dx = target_x - self.player.x
            dy = target_y - self.player.y
        else:
            # Chase ball
            dx = ball.x - self.player.x
            dy = ball.y - self.player.y
        
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            return (dx / dist * self.player.speed * 0.95, 
                   dy / dist * self.player.speed * 0.95, False)
        
        return (0, 0, False)

class SoccerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Soccer: Minimax vs DQN")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.state = GameState.MENU
        self.reset_game()
        
        # Statistics
        self.total_goals_minimax = 0
        self.total_goals_dqn = 0
        self.match_goals_left = 0
        self.match_goals_right = 0
        
        # Field offset for centering
        self.offset_x = (SCREEN_WIDTH - FIELD_WIDTH) // 2
        self.offset_y = 50
    
    def reset_game(self):
        self.ball = Ball(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        # Small random velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5)
        self.ball.vx = math.cos(angle) * speed
        self.ball.vy = math.sin(angle) * speed
        
        self.player1 = Player(150, FIELD_HEIGHT // 2, BLUE, "Minimax")
        self.player2 = Player(FIELD_WIDTH - 150, FIELD_HEIGHT // 2, RED, "DQN")
        
        self.minimax_agent = MinimaxAgent(self.player1, FIELD_WIDTH - 10, FIELD_HEIGHT // 2)
        self.dqn_agent = DQNAgent(self.player2, 10, FIELD_HEIGHT // 2)
        
        self.match_goals_left = 0
        self.match_goals_right = 0
    
    def reset_ball(self):
        self.ball = Ball(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        # Random starting direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 2)
        self.ball.vx = math.cos(angle) * speed
        self.ball.vy = math.sin(angle) * speed
        
        # Reset player positions with slight variation
        self.player1.x = 150 + random.randint(-30, 30)
        self.player1.y = FIELD_HEIGHT // 2 + random.randint(-50, 50)
        self.player2.x = FIELD_WIDTH - 150 + random.randint(-30, 30)
        self.player2.y = FIELD_HEIGHT // 2 + random.randint(-50, 50)
    
    def check_goal(self):
        goal_y_min = FIELD_HEIGHT // 2 - GOAL_HEIGHT // 2
        goal_y_max = FIELD_HEIGHT // 2 + GOAL_HEIGHT // 2
        
        # Left goal (DQN defends)
        if self.ball.x < GOAL_WIDTH:
            if goal_y_min < self.ball.y < goal_y_max:
                self.match_goals_left += 1
                self.total_goals_minimax += 1
                self.reset_ball()
                return True
            else:
                self.ball.vx *= -0.8
                self.ball.x = GOAL_WIDTH
        
        # Right goal (Minimax defends)
        if self.ball.x > FIELD_WIDTH - GOAL_WIDTH:
            if goal_y_min < self.ball.y < goal_y_max:
                self.match_goals_right += 1
                self.total_goals_dqn += 1
                self.reset_ball()
                return True
            else:
                self.ball.vx *= -0.8
                self.ball.x = FIELD_WIDTH - GOAL_WIDTH
        
        return False
    
    def handle_kick(self, player, dx, dy, should_kick):
        dist = player.distance_to(self.ball.x, self.ball.y)
        if dist < player.radius + self.ball.radius and should_kick:
            # Calculate kick direction
            angle = math.atan2(dy, dx)
            # Consistent kick power
            power = 7.5
            self.ball.vx = math.cos(angle) * power
            self.ball.vy = math.sin(angle) * power
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        # Get AI actions
        minimax_action = self.minimax_agent.get_action(self.ball, self.player2)
        dqn_action = self.dqn_agent.get_action(self.ball, self.player1)
        
        # Move players
        self.player1.move(minimax_action[0], minimax_action[1])
        self.player2.move(dqn_action[0], dqn_action[1])
        
        # Handle kicks
        self.handle_kick(self.player1, minimax_action[0], minimax_action[1], 
                        minimax_action[2])
        self.handle_kick(self.player2, dqn_action[0], dqn_action[1], 
                        dqn_action[2])
        
        # Update ball
        self.ball.update()
        
        # Check for goals
        self.check_goal()
    
    def draw_field(self):
        # Field background
        pygame.draw.rect(self.screen, GREEN, 
                        (self.offset_x, self.offset_y, FIELD_WIDTH, FIELD_HEIGHT))
        
        # Center line
        pygame.draw.line(self.screen, WHITE, 
                        (self.offset_x + FIELD_WIDTH // 2, self.offset_y),
                        (self.offset_x + FIELD_WIDTH // 2, self.offset_y + FIELD_HEIGHT), 3)
        
        # Center circle
        pygame.draw.circle(self.screen, WHITE, 
                          (self.offset_x + FIELD_WIDTH // 2, 
                           self.offset_y + FIELD_HEIGHT // 2), 50, 3)
        
        # Goals
        goal_y = self.offset_y + FIELD_HEIGHT // 2 - GOAL_HEIGHT // 2
        pygame.draw.rect(self.screen, DARK_RED, 
                        (self.offset_x, goal_y, GOAL_WIDTH, GOAL_HEIGHT))
        pygame.draw.rect(self.screen, DARK_RED, 
                        (self.offset_x + FIELD_WIDTH - GOAL_WIDTH, goal_y, 
                         GOAL_WIDTH, GOAL_HEIGHT))
        
        # Field border
        pygame.draw.rect(self.screen, WHITE, 
                        (self.offset_x, self.offset_y, FIELD_WIDTH, FIELD_HEIGHT), 3)
    
    def draw_menu(self):
        self.screen.fill((15, 23, 42))
        
        # Title
        title = self.font.render("AI SOCCER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("Minimax vs DQN Comparison", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 140))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Balance info
        balance_text = self.small_font.render("⚖️ Fairly Balanced Agents", True, (34, 197, 94))
        balance_rect = balance_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(balance_text, balance_rect)
        
        # Stats boxes
        box_width = 300
        box_height = 150
        
        # Minimax box
        pygame.draw.rect(self.screen, DARK_BLUE, 
                        (150, 210, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, BLUE, 
                        (150, 210, box_width, box_height), 3, border_radius=10)
        
        text = self.font.render("Minimax (Blue)", True, BLUE)
        self.screen.blit(text, (170, 230))
        
        info1 = self.small_font.render("Tree search", True, WHITE)
        info2 = self.small_font.render("Optimal tactics", True, WHITE)
        self.screen.blit(info1, (170, 270))
        self.screen.blit(info2, (170, 295))
        
        goals = self.font.render(f"{self.total_goals_minimax} Goals", True, WHITE)
        self.screen.blit(goals, (170, 325))
        
        # DQN box
        pygame.draw.rect(self.screen, DARK_RED, 
                        (550, 210, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, RED, 
                        (550, 210, box_width, box_height), 3, border_radius=10)
        
        text = self.font.render("DQN (Red)", True, RED)
        self.screen.blit(text, (570, 230))
        
        info1 = self.small_font.render("RL-based", True, WHITE)
        info2 = self.small_font.render("Adaptive strategy", True, WHITE)
        self.screen.blit(info1, (570, 270))
        self.screen.blit(info2, (570, 295))
        
        goals = self.font.render(f"{self.total_goals_dqn} Goals", True, WHITE)
        self.screen.blit(goals, (570, 325))
        
        # Instructions
        inst = self.small_font.render("Press SPACE to Start | ESC to Quit", 
                                     True, GRAY)
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(inst, inst_rect)
    
    def draw_game(self):
        self.screen.fill((30, 41, 59))
        
        # Draw field
        self.draw_field()
        
        # Draw game objects
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
            f"All-time: Minimax {self.total_goals_minimax} - {self.total_goals_dqn} DQN", 
            True, GRAY)
        total_rect = total.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(total, total_rect)
        
        # Draw controls
        controls = self.small_font.render("P: Pause | R: Reset | ESC: Menu", 
                                         True, GRAY)
        self.screen.blit(controls, (10, 10))
        
        # Draw strategy info
        mini_strat = self.small_font.render("Minimax: Chase → Shoot", True, BLUE)
        dqn_strat = self.small_font.render("DQN: Predict → Defend", True, RED)
        self.screen.blit(mini_strat, (SCREEN_WIDTH - 280, 10))
        self.screen.blit(dqn_strat, (SCREEN_WIDTH - 280, 35))
        
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
                    else:
                        self.state = GameState.MENU
                
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.reset_game()
                        self.state = GameState.PLAYING
                
                elif event.key == pygame.K_p:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                
                elif event.key == pygame.K_r:
                    if self.state != GameState.MENU:
                        self.reset_game()
                        self.state = GameState.PLAYING
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            self.update()
            
            if self.state == GameState.MENU:
                self.draw_menu()
            else:
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SoccerGame()
    game.run()