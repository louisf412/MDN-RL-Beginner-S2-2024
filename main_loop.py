from main import *
from Q_Learning_Practice import *
import pyglet
from utils import plotLearning 

if __name__ == '__main__':
    qagent = QAgent(gamma = 0.99, epsilon=1.0, batch_size = 64, n_actions = 4, eps_end = 0.01, input_dims = [9], lr = 0.003)
    carAgent = Agent()

    window = CarGame(carAgent)
    
    scores, eps_history = [], []
    n_iterations = 500
    checkpoint_interval = 50 


    done  = False

    def update(dt):
        global done 

        # Get the current state of the car

        state = [
            carAgent.state[0], # X position
            carAgent.state[1], # y position
            carAgent.state[2], # Orientation
            carAgent.vel[0], # velocity
            *carAgent.projections[1] # Ray distances   
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
        
        # Observe new state and reward
        new_state = [
            carAgent.state[0],
            carAgent.state[1],
            carAgent.state[2],
            carAgent.vel[0],
            *carAgent.projections[1]
        ]

        # Calculating reward
        # Negative reward for collision, positive for moving forward
        reward = 0

        if carAgent.collision_cooldown > 0:
            # Negative reward for collision
            reward = -100
            # Moving forward
        elif action == 0:
            reward = 50
        elif carAgent.vel[0] < 3:
            reward = -5
        else:
            reward = 15
        done = False
        print("Too many collisions")

        qagent.store_transition(state, action, reward, new_state, done)

        # train q agent (updating the Q-network)
        qagent.learn()

        # update at 240 fps

    pyglet.clock.schedule_interval(update, 1/240)

    pyglet.app.run()

