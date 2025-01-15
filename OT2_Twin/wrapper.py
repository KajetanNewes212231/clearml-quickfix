import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sim_class import Simulation

class OT2Env(gym.Env):
    def __init__(self, render=False, max_steps=1000):
        super(OT2Env, self).__init__()
        self.render = render
        self.max_steps = max_steps

        # Create the simulation environment
        self.sim = Simulation(num_agents=1)

        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Box(low=np.array([-0.187, -0.1705, 0.119], dtype=np.float32), high=np.array([0.253, 0.2195, 0.2895], dtype=np.float32), shape=(3,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)

        # keep track of the number of steps
        self.steps = 0

    def reset(self, seed=None):
        # being able to set a seed is required for reproducibility
        if seed is not None:
            np.random.seed(seed)

        # Reset the state of the environment to an initial state
        # set a random goal position for the agent, consisting of x, y, and z coordinates within the working area (you determined these values in the previous datalab task)
        self.goal_position = np.random.uniform(low=-1, high=1, size=(3,)).astype(np.float32)
        # Call the environment reset function
        observation = self.sim.reset(num_agents=1)
        #print(f'OBSERVATION!!!!!!:{observation}')
        # now we need to process the observation and extract the relevant information, the pipette position, convert it to a numpy array, and append the goal position and make sure the array is of type np.float32
        try:
            observation = np.concatenate([observation['robotId_2']['pipette_position'], self.goal_position]).astype(np.float32)
        except:
            observation = np.concatenate([observation['robotId_1']['pipette_position'], self.goal_position]).astype(np.float32)
            
        # Reset the number of steps
        self.steps = 0

        #print(f'Observation: {observation}')
        return observation, {}

    def step(self, action):
        # Execute one time step within the environment
        # since we are only controlling the pipette position, we accept 3 values for the action and need to append 0 for the drop action
        action = np.append(action, 0).astype(np.float32)

        # Call the environment step function
        observation = self.sim.run([action]) # Why do we need to pass the action as a list? Think about the simulation class.

        # now we need to process the observation and extract the relevant information, the pipette position, convert it to a numpy array, and append the goal position and make sure the array is of type np.float32
        try:
            observation = np.concatenate([observation['robotId_1']['pipette_position'], self.goal_position]).astype(np.float32)
        except:
            observation = np.concatenate([observation['robotId_2']['pipette_position'], self.goal_position]).astype(np.float32)
        #print(f'Observation: {observation}, Goal Position: {self.goal_position}')
        # Calculate the reward, this is something that you will need to experiment with to get the best results
        def reward_function(observation, goal_position):
            # Calculate the distance between the pipette position and the goal position
            distance = np.linalg.norm(observation[:3] - goal_position)
            # Calculate the reward as the negative of the distance
            reward = -distance
            if distance < 0.01:
                reward += 100
            return reward
        
        reward = reward_function(observation, self.goal_position)
        #print(f'Reward: {reward}')
        # next we need to check if the if the task has been completed and if the episode should be terminated
        # To do this we need to calculate the distance between the pipette position and the goal position and if it is below a certain threshold, we will consider the task complete. 
        # What is a reasonable threshold? Think about the size of the pipette tip and the size of the plants.
        if reward > -0.01:
            terminated = True
            # we can also give the agent a positive reward for completing the task
        else:
            terminated = False

        # next we need to check if the episode should be truncated, we can check if the current number of steps is greater than the maximum number of steps
        if self.steps >= self.max_steps:
            truncated = True
        else:
            truncated = False

        info = {} # we don't need to return any additional information

        # increment the number of steps
        self.steps += 1

        #print(f'Observation: {observation}, Reward: {reward}, Terminated: {terminated}, Truncated: {truncated}, Info: {info}')
        return observation, reward, terminated, truncated, info

    def render(self, mode='human'):
        pass
    
    def close(self):
        self.sim.close()