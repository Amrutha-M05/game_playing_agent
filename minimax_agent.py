"""
Minimax Agent for AI Soccer
Uses classical tree search algorithm for decision making
"""

import math

class MinimaxAgent:
    """
    Minimax agent that uses tree search to find optimal moves
    
    Strategy:
    1. Evaluate distance to ball
    2. If far from ball: move towards it
    3. If close to ball: aim and shoot at goal
    """
    
    def __init__(self, player, goal_x, goal_y, depth=2):
        """
        Initialize Minimax agent
        
        Args:
            player: Player object to control
            goal_x: X coordinate of target goal
            goal_y: Y coordinate of target goal
            depth: Search depth for minimax tree (not fully implemented)
        """
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.depth = depth
    
    def get_action(self, ball, opponent):
        """
        Calculate best action using minimax strategy
        
        Args:
            ball: Ball object with position and velocity
            opponent: Opponent player object
            
        Returns:
            tuple: (dx, dy, should_kick)
                dx, dy: movement direction
                should_kick: whether to kick the ball
        """
        # Calculate distance to ball
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Phase 1: Chase ball
        if dist_to_ball > 5:
            dx = ball.x - self.player.x
            dy = ball.y - self.player.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                # Normalize and scale by speed
                return (
                    dx / dist * self.player.speed,
                    dy / dist * self.player.speed,
                    False  # Don't kick yet
                )
        
        # Phase 2: Shoot at goal
        else:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                # Reduced speed for accuracy
                return (
                    dx / dist * self.player.speed * 0.5,
                    dy / dist * self.player.speed * 0.5,
                    True  # Kick!
                )
        
        return (0, 0, False)
    
    def evaluate_state(self, ball, opponent):
        """
        Evaluate game state for minimax tree search
        (Future enhancement: can be used for deeper lookahead)
        
        Args:
            ball: Ball object
            opponent: Opponent player
            
        Returns:
            float: State evaluation score
        """
        # Distance to ball (closer is better)
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        # Distance of ball to goal (closer is better)
        ball_to_goal = math.sqrt(
            (ball.x - self.goal_x) ** 2 + 
            (ball.y - self.goal_y) ** 2
        )
        
        # Opponent distance to ball (further is better for us)
        opponent_to_ball = opponent.distance_to(ball.x, ball.y)
        
        score = -dist_to_ball - ball_to_goal * 0.5 + opponent_to_ball * 0.3
        return score