#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import plotly.graph_objects as go
from ipywidgets import interact, FloatSlider
import plotly.io as pio

# Define the grid size and initial parameters
grid_size = (100, 100)
initial_tumor_size = 5
cell_proliferation_rate = 0.1  # Change to a float
nutrient_availability = 0.1  # Change to a float
nutrient_availability_threshold = 0.05  # Adjust as needed
max_time_steps = 100

# Initialize the grid
grid = np.zeros(grid_size)

# Place the initial tumor
center = (grid_size[0]//2, grid_size[1]//2)
grid[center[0]-initial_tumor_size:center[0]+initial_tumor_size,
     center[1]-initial_tumor_size:center[1]+initial_tumor_size] = 1

# Define the update function
def update(frame_num, rate, nutrient):
    global grid  # Ensure we modify the global grid variable
    
    # Copy the grid to avoid modifying it while iterating
    new_grid = np.copy(grid)
    
    # Iterate over each cell in the grid
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            # Check if the current cell is a tumor cell
            if grid[i, j] == 1:
                # Check nutrient availability
                if nutrient > nutrient_availability_threshold:
                    # Proliferate into adjacent empty cells
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue  # Skip the current cell
                            # Calculate neighbor coordinates
                            ni, nj = i + dx, j + dy
                            # Check if neighbor is within grid bounds and empty
                            if 0 <= ni < grid_size[0] and 0 <= nj < grid_size[1] and grid[ni, nj] == 0:
                                # Proliferate with a probability determined by the cell proliferation rate
                                if np.random.random() < rate:
                                    new_grid[ni, nj] = 1
    
    # Update the grid with the new state
    grid = new_grid
    
    # Create 3D surface plot
    x, y = np.meshgrid(np.arange(grid_size[0]), np.arange(grid_size[1]))
    fig = go.Figure(data=[go.Surface(z=grid, colorscale='Viridis')])
    fig.update_layout(title=f'Time step: {frame_num}',
                      scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    
    pio.show(fig, renderer="iframe")  # Display the figure
    
    return fig  # Return the figure object

# Create interactive sliders
rate_slider = FloatSlider(min=0, max=1, step=0.1, value=cell_proliferation_rate)
nutrient_slider = FloatSlider(min=0, max=1, step=0.1, value=nutrient_availability)

# Set up the interactive plot
interact(update, frame_num=(0, max_time_steps, 1), rate=rate_slider, nutrient=nutrient_slider)


# In[ ]:




