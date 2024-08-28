import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle



def run(episodes, render =False):

    env = gym.make('FrozenLake-v1', map_name = "8x8", is_slippery=False, render_mode='human' if render else None)

    q = np.zeros((env.observation_space.n, env.action_space.n))

    learning_rate_a = 0.9 # Learning rate or Alpha
    discount_factor_g = 0.9 # Gamma or discount factor

    # Episolon greedy algorithm
    epsilon = 1 # 1 = 100% random actions
    # Parameter and impacts the minimum number of episodes we have to train
    epsilon_decay_rate = 0.00001
    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)


    for i in range(episodes):
        state = env.reset()[0]
        terminated = False # True when falling into a hole or goal reached
        truncated = False # True when actions > 200

       

        while(not terminated and not truncated):
            # Basically moved the character untill it either is terminated or truncated
            if rng.random() < epsilon:
                action = env.action_space.sample() # actinos: 0 = left, 1 = down, 2 = right, 3 = up
            else:
                action = np.argmax(q[state,:])

            new_state,reward,terminated,truncated,_ = env.step(action)

            # q learning formula
            q[state,action] = q[state,action] + learning_rate_a * (reward + discount_factor_g * np.max(q[new_state,:]) - q[state,action])
            
            
            state = new_state


        epsilon = max(epsilon - epsilon_decay_rate, 0)

        if(epsilon == 0):
            learning_rate_a = 0.0001

        if reward == 1:
            rewards_per_episode[i] = 1

    env.close()


    sum_rewards = np.zeros(episodes)

    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig('frozen_lake8x8.png')

    f = open("frozen_lake8x8.pkl", "wb")
    pickle.dump(q, f)
    f.close()


if __name__ == '__main__':
    run(15000)