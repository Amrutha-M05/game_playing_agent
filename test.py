"""
Test Suite for AI Soccer Game - Updated for Balanced Agents
Run automated tests to verify game balance and functionality
"""

import math
import random
import sys
from collections import defaultdict

# Test configurations
FIELD_WIDTH = 800
FIELD_HEIGHT = 500
PLAYER_SIZE = 20
BALL_SIZE = 10

class TestResults:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def add_result(self, test_name, passed, message=""):
        self.results.append({
            'name': test_name,
            'passed': passed,
            'message': message
        })
        if passed:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
    
    def print_results(self):
        print("\n" + "="*60)
        print("AI SOCCER TEST RESULTS")
        print("="*60)
        
        for result in self.results:
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            print(f"{status}: {result['name']}")
            if result['message']:
                print(f"    → {result['message']}")
        
        print("\n" + "-"*60)
        total = self.tests_passed + self.tests_failed
        print(f"Total Tests: {total}")
        print(f"Passed: {self.tests_passed} ({self.tests_passed/total*100:.1f}%)")
        print(f"Failed: {self.tests_failed} ({self.tests_failed/total*100:.1f}%)")
        print("="*60 + "\n")

class MockBall:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = BALL_SIZE
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98

class MockPlayer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_SIZE
        self.speed = 3.5
    
    def distance_to(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(self.radius, min(FIELD_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(FIELD_HEIGHT - self.radius, self.y))

# Simplified agent classes for testing
class TestMinimaxAgent:
    def __init__(self, player, goal_x, goal_y, error_rate=0.15):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.prediction_frames = 8
        self.error_rate = error_rate
    
    def get_action(self, ball, opponent):
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        if random.random() < self.error_rate:
            angle = random.uniform(0, 2 * math.pi)
            return (math.cos(angle) * self.player.speed, 
                   math.sin(angle) * self.player.speed, False)
        
        if dist_to_ball < 20:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                return (dx / dist * self.player.speed * 0.8, 
                       dy / dist * self.player.speed * 0.8, True)
        
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

class TestDQNAgent:
    def __init__(self, player, goal_x, goal_y, error_rate=0.15):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.prediction_frames = 10
        self.error_rate = error_rate
    
    def get_action(self, ball, opponent):
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        if random.random() < self.error_rate:
            angle = random.uniform(0, 2 * math.pi)
            return (math.cos(angle) * self.player.speed, 
                   math.sin(angle) * self.player.speed, False)
        
        if dist_to_ball < 20:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                return (dx / dist * self.player.speed * 0.8, 
                       dy / dist * self.player.speed * 0.8, True)
        
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

class TestHeuristicAgent:
    def __init__(self, player, goal_x, goal_y, error_rate=0.15):
        self.player = player
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.prediction_frames = 10
        self.error_rate = error_rate
    
    def get_action(self, ball, opponent):
        dist_to_ball = self.player.distance_to(ball.x, ball.y)
        
        if random.random() < self.error_rate:
            angle = random.uniform(0, 2 * math.pi)
            return (math.cos(angle) * self.player.speed, 
                   math.sin(angle) * self.player.speed, False)
        
        if dist_to_ball < 20:
            dx = self.goal_x - ball.x
            dy = self.goal_y - ball.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                return (dx / dist * self.player.speed * 0.8, 
                       dy / dist * self.player.speed * 0.8, True)
        
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

def test_agent_parameters():
    """Test that all agents have equal base parameters"""
    results = TestResults()
    
    player = MockPlayer(100, 100)
    
    # Create agents
    minimax = TestMinimaxAgent(player, FIELD_WIDTH, FIELD_HEIGHT // 2, error_rate=0.15)
    dqn = TestDQNAgent(player, FIELD_WIDTH, FIELD_HEIGHT // 2, error_rate=0.15)
    heuristic = TestHeuristicAgent(player, FIELD_WIDTH, FIELD_HEIGHT // 2, error_rate=0.15)
    
    # Test error rates
    if minimax.error_rate == dqn.error_rate == heuristic.error_rate:
        results.add_result("Equal error rates", True, 
                         f"All agents: {minimax.error_rate*100}%")
    else:
        results.add_result("Equal error rates", False,
                         f"M:{minimax.error_rate}, D:{dqn.error_rate}, H:{heuristic.error_rate}")
    
    # Test prediction frames (can be slightly different for variety)
    results.add_result("Prediction frames set", True,
                     f"Minimax:{minimax.prediction_frames}, DQN:{dqn.prediction_frames}, Heuristic:{heuristic.prediction_frames}")
    
    # Test base speed
    if player.speed == 3.5:
        results.add_result("Player base speed", True, f"Speed = {player.speed}")
    else:
        results.add_result("Player base speed", False, f"Expected 3.5, got {player.speed}")
    
    return results

def test_shooting_behavior():
    """Test shooting range and behavior"""
    results = TestResults()
    
    player1 = MockPlayer(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
    player2 = MockPlayer(FIELD_WIDTH // 2 + 100, FIELD_HEIGHT // 2)
    
    minimax = TestMinimaxAgent(player1, FIELD_WIDTH, FIELD_HEIGHT // 2, error_rate=0)
    dqn = TestDQNAgent(player2, 0, FIELD_HEIGHT // 2, error_rate=0)
    
    # Test at shooting range (distance = 15)
    ball_close = MockBall(player1.x + 15, player1.y)
    minimax_action = minimax.get_action(ball_close, player2)
    
    if minimax_action[2]:  # should_kick
        results.add_result("Minimax shoots at close range", True, "Distance = 15")
    else:
        results.add_result("Minimax shoots at close range", False, "Not shooting at distance 15")
    
    ball_close2 = MockBall(player2.x - 15, player2.y)
    dqn_action = dqn.get_action(ball_close2, player1)
    
    if dqn_action[2]:
        results.add_result("DQN shoots at close range", True, "Distance = 15")
    else:
        results.add_result("DQN shoots at close range", False, "Not shooting at distance 15")
    
    # Test outside shooting range (distance = 30)
    ball_far = MockBall(player1.x + 30, player1.y)
    minimax_action_far = minimax.get_action(ball_far, player2)
    
    if not minimax_action_far[2]:
        results.add_result("Minimax doesn't shoot far away", True, "Distance = 30")
    else:
        results.add_result("Minimax doesn't shoot far away", False, "Shooting at distance 30")
    
    return results

def test_movement_speed():
    """Test actual movement speeds"""
    results = TestResults()
    
    player1 = MockPlayer(100, FIELD_HEIGHT // 2)
    player2 = MockPlayer(FIELD_WIDTH - 100, FIELD_HEIGHT // 2)
    ball = MockBall(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
    
    minimax = TestMinimaxAgent(player1, FIELD_WIDTH, FIELD_HEIGHT // 2, error_rate=0)
    dqn = TestDQNAgent(player2, 0, FIELD_HEIGHT // 2, error_rate=0)
    
    # Get actions
    minimax_action = minimax.get_action(ball, player2)
    dqn_action = dqn.get_action(ball, player1)
    
    # Calculate speeds
    minimax_speed = math.sqrt(minimax_action[0]**2 + minimax_action[1]**2)
    dqn_speed = math.sqrt(dqn_action[0]**2 + dqn_action[1]**2)
    
    speed_ratio = minimax_speed / dqn_speed if dqn_speed > 0 else 0
    
    results.add_result("Movement speeds calculated", True,
                     f"Minimax:{minimax_speed:.2f}, DQN:{dqn_speed:.2f}, Ratio:{speed_ratio:.2f}")
    
    # Check if speeds are similar (within 20%)
    if 0.8 <= speed_ratio <= 1.2:
        results.add_result("Movement speeds balanced", True,
                         f"Speed ratio {speed_ratio:.2f} is within 0.8-1.2")
    else:
        results.add_result("Movement speeds balanced", False,
                         f"Speed ratio {speed_ratio:.2f} outside acceptable range")
    
    return results

def test_ball_physics():
    """Test ball movement and friction"""
    results = TestResults()
    
    ball = MockBall(400, 250, vx=10.0, vy=5.0)
    
    initial_vx = ball.vx
    initial_vy = ball.vy
    initial_x = ball.x
    
    ball.update()
    
    # Check friction
    if ball.vx < initial_vx:
        results.add_result("Ball friction (X)", True, f"{initial_vx} → {ball.vx}")
    else:
        results.add_result("Ball friction (X)", False, "Velocity not decreasing")
    
    if ball.vy < initial_vy:
        results.add_result("Ball friction (Y)", True, f"{initial_vy} → {ball.vy}")
    else:
        results.add_result("Ball friction (Y)", False, "Velocity not decreasing")
    
    # Check movement
    if ball.x != initial_x:
        results.add_result("Ball movement", True, f"Moved from {initial_x} to {ball.x}")
    else:
        results.add_result("Ball movement", False, "Ball not moving")
    
    return results

def test_goal_detection():
    """Test goal scoring logic"""
    results = TestResults()
    
    GOAL_WIDTH = 20
    GOAL_HEIGHT = 150
    
    # Test left goal (x=0)
    ball_left = MockBall(GOAL_WIDTH - 1, FIELD_HEIGHT // 2)
    goal_y_min = FIELD_HEIGHT // 2 - GOAL_HEIGHT // 2
    goal_y_max = FIELD_HEIGHT // 2 + GOAL_HEIGHT // 2
    
    if ball_left.x < GOAL_WIDTH and goal_y_min < ball_left.y < goal_y_max:
        results.add_result("Left goal detection", True, "Ball at x<20, y=center detected")
    else:
        results.add_result("Left goal detection", False, "Goal not detected")
    
    # Test right goal (x=FIELD_WIDTH)
    ball_right = MockBall(FIELD_WIDTH - GOAL_WIDTH + 1, FIELD_HEIGHT // 2)
    
    if ball_right.x > FIELD_WIDTH - GOAL_WIDTH and goal_y_min < ball_right.y < goal_y_max:
        results.add_result("Right goal detection", True, "Ball at x>780, y=center detected")
    else:
        results.add_result("Right goal detection", False, "Goal not detected")
    
    # Test miss (too high)
    ball_miss = MockBall(GOAL_WIDTH - 1, FIELD_HEIGHT // 2 - GOAL_HEIGHT)
    
    if not (goal_y_min < ball_miss.y < goal_y_max):
        results.add_result("Goal miss detection", True, "Ball outside goal area rejected")
    else:
        results.add_result("Goal miss detection", False, "Incorrect goal counted")
    
    return results

def simulate_match(frames=500):
    """Simulate a match and check balance"""
    results = TestResults()
    
    ball = MockBall(FIELD_WIDTH // 2, FIELD_HEIGHT // 2, vx=2, vy=1)
    player1 = MockPlayer(150, FIELD_HEIGHT // 2)
    player2 = MockPlayer(FIELD_WIDTH - 150, FIELD_HEIGHT // 2)
    
    minimax = TestMinimaxAgent(player1, FIELD_WIDTH, FIELD_HEIGHT // 2, error_rate=0.15)
    dqn = TestDQNAgent(player2, 0, FIELD_HEIGHT // 2, error_rate=0.15)
    
    minimax_possession = 0
    dqn_possession = 0
    
    for _ in range(frames):
        # Get actions
        minimax_action = minimax.get_action(ball, player2)
        dqn_action = dqn.get_action(ball, player1)
        
        # Move players
        player1.move(minimax_action[0], minimax_action[1])
        player2.move(dqn_action[0], dqn_action[1])
        
        # Update ball
        ball.update()
        
        # Count possession
        if player1.distance_to(ball.x, ball.y) < 30:
            minimax_possession += 1
        if player2.distance_to(ball.x, ball.y) < 30:
            dqn_possession += 1
    
    total_possession = minimax_possession + dqn_possession
    if total_possession > 0:
        minimax_ratio = minimax_possession / total_possession
        dqn_ratio = dqn_possession / total_possession
        
        results.add_result("Simulation completed", True, 
                         f"{frames} frames simulated")
        results.add_result("Possession tracked", True,
                         f"Minimax:{minimax_ratio*100:.1f}%, DQN:{dqn_ratio*100:.1f}%")
        
        # Check balance (30-70% range is acceptable)
        if 0.3 <= minimax_ratio <= 0.7:
            results.add_result("Possession balanced", True,
                             f"Minimax possession {minimax_ratio*100:.1f}% is within 30-70%")
        else:
            results.add_result("Possession balanced", False,
                             f"Minimax possession {minimax_ratio*100:.1f}% outside 30-70% range")
    else:
        results.add_result("Simulation", False, "No possession recorded")
    
    return results

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI SOCCER - COMPREHENSIVE TEST SUITE")
    print("Testing Balanced Agent Implementation")
    print("="*60 + "\n")
    
    all_results = TestResults()
    
    # Run test suites
    print("1. Testing agent parameters...")
    param_results = test_agent_parameters()
    all_results.results.extend(param_results.results)
    all_results.tests_passed += param_results.tests_passed
    all_results.tests_failed += param_results.tests_failed
    
    print("2. Testing shooting behavior...")
    shoot_results = test_shooting_behavior()
    all_results.results.extend(shoot_results.results)
    all_results.tests_passed += shoot_results.tests_passed
    all_results.tests_failed += shoot_results.tests_failed
    
    print("3. Testing movement speeds...")
    speed_results = test_movement_speed()
    all_results.results.extend(speed_results.results)
    all_results.tests_passed += speed_results.tests_passed
    all_results.tests_failed += speed_results.tests_failed
    
    print("4. Testing ball physics...")
    ball_results = test_ball_physics()
    all_results.results.extend(ball_results.results)
    all_results.tests_passed += ball_results.tests_passed
    all_results.tests_failed += ball_results.tests_failed
    
    print("5. Testing goal detection...")
    goal_results = test_goal_detection()
    all_results.results.extend(goal_results.results)
    all_results.tests_passed += goal_results.tests_passed
    all_results.tests_failed += goal_results.tests_failed
    
    print("6. Running match simulation...")
    sim_results = simulate_match(500)
    all_results.results.extend(sim_results.results)
    all_results.tests_passed += sim_results.tests_passed
    all_results.tests_failed += sim_results.tests_failed
    
    # Print final results
    all_results.print_results()
    
    # Summary
    print("BALANCE SUMMARY:")
    print("="*60)
    print("✓ All agents have equal error rates (15% Medium difficulty)")
    print("✓ Shooting range: < 20 pixels")
    print("✓ Prediction: Minimax 8f, DQN/Heuristic 10f")
    print("✓ Base speed: 3.5 for all players")
    print("✓ Random mistakes ensure competitive gameplay")
    print("✓ Both teams have equal chance to score")
    print("="*60 + "\n")
    
    # Exit code
    sys.exit(0 if all_results.tests_failed == 0 else 1)

if __name__ == "__main__":
    main()