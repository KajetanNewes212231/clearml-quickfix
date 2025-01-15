from stable_baselines3 import PPO
import gym
import time
import wandb
from wandb.integration.sb3 import WandbCallback
import os
from clearml import Task
from wrapper import OT2Env

# Replace Pendulum-v1/YourName with your own project name (Folder/YourName, e.g. 2022-Y2B-RoboSuite/Michael)
task = Task.init(project_name='Mentor Group A/Group 3', # NB: Replace YourName with your own name
                    task_name='Experiment1')

#copy these lines exactly as they are
#setting the base docker image
task.set_base_docker('deanis/2023y2b-rl:latest')
#setting the task to run remotely on the default queue
task.execute_remotely(queue_name="default")

os.environ['WANDB_API_KEY'] = 'fefb8c486145c4bbe0597532d8a05b449a49eb91'

wandb.login(key='fefb8c486145c4bbe0597532d8a05b449a49eb91')
env = OT2Env()

# initialize wandb project
run = wandb.init(project="OT2_RL1",sync_tensorboard=True)

# create wandb callback
wandb_callback = WandbCallback(model_save_freq=1000,
                                model_save_path=f"models/{run.id}",
                                verbose=2,
                                )

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--learning_rate", type=float, default=0.0003)
parser.add_argument("--batch_size", type=int, default=64)
parser.add_argument("--n_steps", type=int, default=2048)
parser.add_argument("--n_epochs", type=int, default=10)
parser.add_argument("--gamma", type=float, default=0.9)

args = parser.parse_args()

model = PPO('MlpPolicy', env, verbose=1, 
            learning_rate=args.learning_rate, 
            batch_size=args.batch_size, 
            n_steps=args.n_steps, 
            n_epochs=args.n_epochs, 
            gamma=args.gamma,
            tensorboard_log=f"runs/{run.id}",)

# variable for how often to save the model
time_steps = 100000
for i in range(100):
    # add the reset_num_timesteps=False argument to the learn function to prevent the model from resetting the timestep counter
    # add the tb_log_name argument to the learn function to log the tensorboard data to the correct folder
    model.learn(total_timesteps=time_steps, callback=wandb_callback, progress_bar=True, reset_num_timesteps=False,tb_log_name=f"runs/{run.id}")
    # save the model to the models folder with the run id and the current timestep
    if (i+1) % 10 == 0:
        model.save(f"models/{run.id}/{time_steps*(i+1)}")
