


###############################################################################################
import os
from Game_engine import *
from Q_Learning_Practice import *
import pyglet
from utils import plotLearning 
import numpy as np
import matplotlib.pyplot as plt


if not os.path.exists('models'):
    os.makedirs('models')

if not os.path.exists('plots'):
    os.makedirs('plots')

def plot_learning(scores, eps_history, filename='plots/learning_progress.png'):
    episodes = [i+1 for i in range(len(scores))]
    plt.figure(figsize=(12, 6))

    # Plot scores
    plt.subplot(2, 1, 1)
    plt.plot(episodes, scores, label='Score per Episode', color='b')
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.title('Score Progression Over Time')
    plt.legend()

    # Plot epsilon history
    plt.subplot(2, 1, 2)
    plt.plot(episodes, eps_history, label='Epsilon', color='r')
    plt.xlabel('Episode')
    plt.ylabel('Epsilon')
    plt.title('Epsilon Decay Over Time')
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename)
    plt.show()



if __name__ == '__main__':
    qagent = QAgent(gamma = 0.99, epsilon=1.0, batch_size = 64, n_actions = 4, eps_end = 0.01, input_dims = [9], lr = 0.003)
    carAgent = Agent()
    model_file = ""

    if os.path.exists(model_file):
        print("MODEL EXISTS")
        qagent.load_model(model_file)
    else:
        print("Model doesn't exist")


    window = CarGame(carAgent)
    
    scores, eps_history = [], []
    n_iterations = 500
    checkpoint_interval = 5
    episode_counter = 0
    score = 0
    done  = False
    max_steps = 1000
    best_score = -np.inf
    episode_steps = 0

    ## Check
    current_active_goal = window.goals[0]
    prev_distance = 1000

    def update(dt):
        global done, score, episode_steps, prev_distance, current_active_goal, best_score, episode_counter

        # Get the current state of the car
        episode_steps += 1

        # state = [
        #     carAgent.state[0], # X position
        #     carAgent.state[1], # y position
        #     carAgent.state[2], # Orientation
        #     carAgent.vel[0], # velocity
        #     *carAgent.projections[1] # Ray distances   
        # ]

        state = [
            carAgent.state[0] / WINDOW_WIDTH,  # Normalized x position
            carAgent.state[1] / WINDOW_HEIGHT,  # Normalized y position
            carAgent.state[2] / (2 * np.pi),  # Normalized orientation
            carAgent.vel[0] / carAgent.maxvel,  # Normalized velocity
            *(dist / 10000 for dist in carAgent.projections[1])  # Normalized projections
        ]

        # Choose action using QAgent
        action = qagent.choose_action(state)

        if action == 0: # Move forward
            window.on_key_press(pyglet.window.key.W, None)
        elif action == 1: # Move backward
            window.on_key_press(pyglet.window.key.S, None)
        elif action == 2: # Left turn
            window.on_key_press(pyglet.window.key.A, None)
        elif action == 3: # Right turn
            window.on_key_press(pyglet.window.key.D, None)
        
        # # Observe new state and reward
        # new_state = [
        #     carAgent.state[0],
        #     carAgent.state[1],
        #     carAgent.state[2],
        #     carAgent.vel[0],
        #     *carAgent.projections[1]
        # ]
        # Calculating reward
        # Negative reward for collision, positive for moving forward

        new_state = [
            carAgent.state[0] / WINDOW_WIDTH,
            carAgent.state[1] / WINDOW_HEIGHT,
            carAgent.state[2] / (2 * np.pi),
            carAgent.vel[0] / carAgent.maxvel,
            *(dist / 10000 for dist in carAgent.projections[1])
        ]


        reward = -1
        for goal in window.goals:
            if goal.is_active and goal.check_goal_passed(dt):
                reward = 200  
                score += reward
                print("goal passed")
                # Activate the next goal in the sequence (this can be part of the Goal class logic)
                window.activate_next_goal(goal)
                current_active_goal = goal
                break  # Only one goal can be passed at a time


        if carAgent.collision_cooldown > 0:
            # Negative reward for collision
            reward = -100
            done = True


        
        if prev_distance is not None:
            current_distance = np.linalg.norm([carAgent.state[0] - current_active_goal.start.x, carAgent.state[1] - current_active_goal.start.y])
            if current_distance < prev_distance:
                reward += 20
            prev_distance = current_distance
        
            # Moving forward
        if action == 0:
            reward = 5
        elif carAgent.vel[0] < 4:
            reward = -5
        qagent.store_transition(state, action, reward, new_state, done)
        # train q agent (updating the Q-network)
        qagent.learn()
        score += reward


        if done or episode_steps > max_steps:
            print(f"Episode {episode_counter + 1} finished with score {score}")
            scores.append(score)
            eps_history.append(qagent.epsilon)

            if score > best_score:
                best_score = score
                qagent.save_model("best_model.pth")
                print(f"Best model saved with score {best_score}")

                
            if (episode_counter + 1) % checkpoint_interval == 0:
                model_filename = f"trained_model_eps_{episode_counter + 1}.pth"
                qagent.save_model(model_filename)
                print(f"Model saved as {model_filename}")

            window.reset_game()
            carAgent.reset()
            score = 0
            done = False
            episode_counter += 1
            episode_steps = 0


        # Need a resetter here
        # update at 240 fps

    pyglet.clock.schedule_interval(update, 1/240)
    pyglet.app.run()

    plot_learning
