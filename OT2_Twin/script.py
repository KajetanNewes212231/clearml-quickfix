from sim_class import Simulation
import random
# Initialize the simulation with a specified number of agents
sim = Simulation(num_agents=1)  # For two robots

start = 1
last_pipette_position = [None, None]
x_movement = 'down'
y_movement = 'right'
count = 0
# Run the simulation for a specified number of steps
for i in range(1500):
    count += 1
    position = sim.get_states()
    pipette_position = position['robotId_1']['pipette_position']
    print(pipette_position)

    velocity_x = -0.4
    velocity_y = 0.4
    velocity_z = -0.4
    drop_command = 0
    actions = [[velocity_x, velocity_y, velocity_z, drop_command],
            [velocity_x, velocity_y, velocity_z, drop_command]]
    sim.run(actions)
    

# for i in range(1000):
#     count += 1
#     position = sim.get_states()
#     pipette_position = position['robotId_1']['pipette_position']
#     #print(pipette_position)
#     if start == 1 or (last_pipette_position[0] != pipette_position[0] and x_movement == 'down'):       
#         #coords_before = coords
#         # move to the edge until it hits the wall
#         velocity_x = 0.4
#         velocity_y = 0
#         velocity_z = 0
#         drop_command = 0
#         actions = [[velocity_x, velocity_y, velocity_z, drop_command],
#                 [velocity_x, velocity_y, velocity_z, drop_command]]
#         sim.run(actions)
#         start = 0
#         x_movement = 'down'
#         last_pipette_position = pipette_position
#         print(f'pipette position during down phase: {pipette_position}')
#     # change state when pipette hits the wall

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # # Example action: Move joints with specific velocities
    # velocity_x = random.uniform(-0.5, 0.5)
    # velocity_y = random.uniform(-0.5, 0.5)
    # velocity_z = random.uniform(-0.5, 0.5)
    # drop_command = random.randint(0, 1)

    # actions = [[velocity_x, velocity_y, velocity_z, drop_command],
    #         [velocity_x, velocity_y, velocity_z, drop_command]]

    # sim.run(actions)
