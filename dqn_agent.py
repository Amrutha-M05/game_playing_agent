"""
DQN-inspired Agent for AI Soccer
Uses predictive behavior and strategic positioning
"""

import math

class DQNAgent:
    """
    DQN-inspired agent with predictive behavior
    
    Note: This is a simplified rule-based version that mimics DQN behavior.
    A true DQN would use neural networks and reinforcement learning.
    
    Strategy:
    1. Predict ball trajectory
    2. Position strategically based on prediction
    3. Intercept ball path
    4. Aggressive pursuit when close
    """
    
    def __init__(self, player, goal_x, goal_y, prediction_steps=10):
        """
        Initialize DQN agent
        
        Args:
            player: Player object to control
            goal_x: X coordinate of target goal
            goal_y: Y coordinate of target goal
            prediction_steps: How many frames ahead to predict
        """
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.prediction_steps = prediction_steps
    
    def predict_ball_position(self, ball):
        """
        Predict future ball position based on current velocity
        
        Args:
            ball: Ball object with position and velocity
            
        Returns:
            tuple: (predicted_x, predicted_y)
        """
        predicted_x = ball.x + ball.vx * self.prediction_steps
        predicted_y = ball.y + ball.vy * self.prediction_steps
        
        return predicted_x, predicted_y
    
    def get_action(self, ball, opponent):
        """
        Calculate best action using DQN-inspired strategy
        
        Args:
            ball: Ball object with position and velocity
            opponent: Opponent player object
            
        Returns:
            tuple: (dx, dy, should_kick)
                dx, dy: movement direction
                should_kick: whether to kick the ball
        """
        # Predict ball trajectory
        predicted_x, predicted_y = self.predict_ball_position(ball)
        
        # Calculate distance to ball
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Phase 1: Aggressive chase (when ball is close)
        if dist_to_ball < 30:
            dx = ball.x - self.player.x
            dy = ball.y - self.player.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                # Aggressive speed multiplier
                speed_multiplier = 1.2
                should_kick = dist < 15
                
                return (
                    dx / dist * self.player.speed * speed_multiplier,
                    dy / dist * self.player.speed * speed_multiplier,
                    should_kick
                )
        
        # Phase 2: Strategic positioning (when ball is far)
        else:
            dx = predicted_x - self.player.x
            dy = predicted_y - self.player.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                return (
                    dx / dist * self.player.speed,
                    dy / dist * self.player.speed,
                    False
                )
        
        return (0, 0, False)
    
    def evaluate_q_value(self, state, action):
        """
        Placeholder for Q-value evaluation
        (Future enhancement: implement neural network for true DQN)
        
        Args:
            state: Game state representation
            action: Action to evaluate
            
        Returns:
            float: Estimated Q-value
        """
        # This would be replaced with neural network prediction
        # in a true DQN implementation
        pass
    
    def get_state_representation(self, ball, opponent):
        """
        Convert game state to feature vector for neural network
        (Future enhancement for true DQN)
        
        Args:
            ball: Ball object
            opponent: Opponent player
            
        Returns:
            list: State feature vector
        """
        return [
            self.player.x,
            self.player.y,
            ball.x,
            ball.y,
            ball.vx,
            ball.vy,
            opponent.x,
            opponent.y
        ]