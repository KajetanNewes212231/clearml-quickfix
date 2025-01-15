import gymnasium as gym
import numpy as np
from wrapper import OT2Env

# Load your custom environment
env = OT2Env()

# Number of episodes
num_episodes = 5

for episode in range(num_episodes):
    obs = env.reset()
    done = False
    step = 0

    while not done:
        if step == 200:
            done = True
        # Take a random action from the environment's action space
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        print(f"Episode: {episode + 1}, Step: {step + 1}, Action: {action}, Reward: {reward}")

        step += 1
        if done:
            print(f"Episode finished after {step} steps. Info: {info}")
            break