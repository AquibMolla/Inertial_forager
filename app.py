# app.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import streamlit as st

def initialize_simulation(width, height):
    space = np.ones((width, height))
    food_sites = [(x, y) for x in range(width) for y in range(height)]
    return space, food_sites

def move_forager(x, y, energy, is_resting, space, width, height, max_energy, p):
    energy -= 1
    if energy <= 0:
        return x, y, energy, is_resting, True
    if is_resting:
        if random.random() > p:
            is_resting = False
    else:
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        x += dx
        y += dy
        if 0 <= x < width and 0 <= y < height and space[x, y] == 1:
            space[x, y] = 0
            energy = min(energy + max_energy, max_energy)
            if random.random() < p:
                is_resting = True
    return x, y, energy, is_resting, False

def simulate_forager(max_energy, laziness):
    width = height = 4 * max_energy
    space, food_sites = initialize_simulation(width+1, height+1)
    x, y = width//2, height//2
    energy, is_resting, is_dead = max_energy, True, False
    path = [(x, y)]
    energy_history = [energy]
    food_history = [food_sites.copy()]
    
    while not is_dead:
        x, y, energy, is_resting, is_dead = move_forager(
            x, y, energy, is_resting, space, width, height, max_energy, laziness
        )
        path.append((x, y))
        energy_history.append(energy)
        food_history.append([(i, j) for i in range(width) for j in range(height) if space[i, j] == 1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    def init():
        ax1.clear(), ax2.clear()
        ax1.set(xlim=(0, width), ylim=(0, height), title='Forager Movement')
        ax2.set(xlim=(0, len(energy_history)), ylim=(0, max_energy+2), title='Energy Level')
        ax1.grid(True, linestyle='--', alpha=0.3)
        return []
    
    def update(frame):
        ax1.clear(), ax2.clear()
        if food_history[frame]:
            fx, fy = zip(*food_history[frame])
            ax1.plot(fy, fx, 'go', markersize=5, alpha=0.7, label='Food')
        px, py = zip(*path[:frame+1])
        ax1.plot(py, px, 'b-', alpha=0.3, label='Path')
        ax1.plot(py[-1], px[-1], 'ro', markersize=10, label='Forager')
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.set(xlim=(0, width), ylim=(0, height), title='Forager Movement')
        ax2.plot(energy_history[:frame+1], 'r-', label='Energy')
        ax2.set(xlim=(0, len(energy_history)), ylim=(0, max_energy+2), title='Energy Level')
        if frame == len(path)-1:
            ax1.text(0.5, 0.5, 'Forager died!', ha='center', va='center', transform=ax1.transAxes, color='red', fontsize=15)
        return []
    
    anim = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=False, interval=50)
    html = anim.to_jshtml()
    plt.close(fig)

    return anim.to_jshtml(), len(path)-1, int((width * height) - np.sum(space))
    #return {"html": html, "lifetime": lifetime, "eaten": eaten}

def main():
#    st.title("Inertial Forager Simulation")
#    max_energy = st.slider("Full energy (1-20):", 1, 20, 10)
#    laziness = st.slider("Laziness (0-1):", 0.0, 1.0, 0.5)
#    Set page title
    st.set_page_config(page_title="Inertial Forager Simulation")
    
    # Create main title
    st.title("Inertial Forager Simulation")
    
    # Create sidebar for parameters
    with st.sidebar:
        max_energy = st.slider("Full energy (1-20):", 1, 20, 10)
        laziness = st.slider("Laziness (0-1):", 0.0, 1.0, 0.5)
    if st.button("Run Simulation"):
        result = simulate_forager(max_energy, laziness)
        with st.spinner('Simulating...'):
            html, lifetime, eaten = result #simulate_forager(max_energy, laziness)
        st.write(f"Lifetime: {lifetime} steps | Cabbages eaten: {eaten}")
        st.components.v1.html(html, height=1000, width = 1000, scrolling=True)
#    if st.button("Run Simulation"):
#        with st.spinner('Simulating...'):
#            html, lifetime, eaten = simulate_forager(max_energy, laziness)
#            if html and lifetime is not None and eaten is not None:
#                st.write(f"Lifetime: {lifetime} steps | Cabbages eaten: {eaten}")
#                st.components.v1.html(html, height=1000, scrolling=True)
#            else:
#                st.error("Simulation failed. Please try again.")
#    #    else:
#    #        st.error("Simulation failed. Please try again.")

#def main():
#    """
#    Main Streamlit application function.
#    """
#    # Set page title
#    st.set_page_config(page_title="Inertial Forager Simulation")
#    
#    # Create main title
#    st.title("Inertial Forager Simulation")
#    
#    # Create sidebar for parameters
#    with st.sidebar:
#        max_energy = st.slider("Full energy (1-20):", 1, 20, 10)
#        laziness = st.slider("Laziness (0-1):", 0.0, 1.0, 0.5)
#    
#    # Initialize session state if it doesn't exist
#    if 'simulation_results' not in st.session_state:
#        st.session_state.simulation_results = None
#    
#    # Create run button
#    if st.button("Run Simulation"):
#        # Show spinner while simulating
#        with st.spinner('Running simulation...'):
#            # Run simulation and store results
#            results = simulate_forager(max_energy, laziness)
#            st.session_state.simulation_results = results
#    
#    # Display results if they exist
#    if st.session_state.simulation_results is not None:
#        results = st.session_state.simulation_results
#        # Create columns for metrics
#        col1, col2 = st.columns(2)
#        with col1:
#            st.metric("Lifetime (steps)", results["lifetime"])
#        with col2:
#            st.metric("Cabbages eaten", results["eaten"])
#        
#        # Display animation
#        st.components.v1.html(results["html"], height=600)

if __name__ == "__main__":
    main()
