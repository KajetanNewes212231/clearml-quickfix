import gymnasium as gym
from gymnasium import spaces
import numpy as np
#from sim_class import Simulation
from wrapper import OT2Env

class PIDControllerBase:
    def __init__(self, kp=1, ki=0, kd=0, min_action=None, max_action=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0
        self.min_action = min_action
        self.max_action = max_action

    def control(self, setpoint, obs):
        error = setpoint - obs
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        action = self.kp * error + self.ki * self.integral + self.kd * derivative
        if self.min_action is not None and self.max_action is not None:
            action = np.clip(action, self.min_action, self.max_action)
        return action


class PIDControllerX(PIDControllerBase):
    def __init__(self, kp=1, ki=0, kd=0):
        super().__init__(kp, ki, kd, min_action=-0.187, max_action=0.253)


class PIDControllerY(PIDControllerBase):
    def __init__(self, kp=1, ki=0, kd=0):
        super().__init__(kp, ki, kd, min_action=-0.1705, max_action=0.2195)


class PIDControllerZ(PIDControllerBase):
    def __init__(self, kp=1, ki=0, kd=0):
        super().__init__(kp, ki, kd, min_action=0.119, max_action=0.2895)


class MultiDimPIDController:
    def __init__(self, env, kp=1, ki=0, kd=0):
        self.env = env
        self.controller_x = PIDControllerX(kp, ki, kd)
        self.controller_y = PIDControllerY(kp, ki, kd)
        self.controller_z = PIDControllerZ(kp, ki, kd)

    def control(self, setpoints, obs):
        x_action = self.controller_x.control(setpoints[0], obs[0])
        y_action = self.controller_y.control(setpoints[1], obs[1])
        z_action = self.controller_z.control(setpoints[2], obs[2])
        return np.array([x_action, y_action, z_action])

    def run(self, num_episodes=3):
        # Run each controller separately
        for dimension, controller, min_act, max_act in [
            ('X', self.controller_x, self.controller_x.min_action, self.controller_x.max_action),
            ('Y', self.controller_y, self.controller_y.min_action, self.controller_y.max_action),
            ('Z', self.controller_z, self.controller_z.min_action, self.controller_z.max_action),
        ]:
            print(f"Running controller for {dimension}:")
            for episode in range(num_episodes):
                obs, _ = self.env.reset()
                done = False
                step = 0
                setpoint = np.random.uniform(min_act, max_act)
                while not done:
                    if step == 500:
                        done = True
                    action = [0, 0, 0]
                    idx = {'X':0, 'Y':1, 'Z':2}[dimension]
                    action[idx] = controller.control(setpoint, obs[idx])
                    obs, reward, _, _, info = self.env.step(action)
                    distance = abs(obs[idx] - setpoint)
                    print(f"Episode {episode+1}, Step {step+1}, Dim {dimension}: Action={action[idx]}, "
                          f"Setpoint={setpoint}, Distance={distance}")
                    step += 1
                    if done:
                        print(f"Finished {dimension} after {step} steps. Info: {info}\n")
                        break

# test the MultiDimPID controller
env = OT2Env()
controller = MultiDimPIDController(env, kp=1, ki=1, kd=1)
controller.run()
