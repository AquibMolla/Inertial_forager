import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import streamlit as st

# Set page title
st.set_page_config(page_title="Inertial Forager Simulation")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Header with description
st.markdown("""
    <h2 style='text-align: center;'>Welcome to the Inertial Forager Simulation!</h2>
    <p style='text-align: center;'>
        This simulation models the behavior of a forager searching for food in a grid world.
        Adjust the parameters in the sidebar and click "Run Simulation" to see the forager in action!
    </p>
""", unsafe_allow_html=True)

# Display image
st.image("app.jpeg", caption="Illustration of the Forager Model", use_column_width=True)

# Sidebar for parameters
with st.sidebar:
    st.header("Simulation Parameters")
    max_energy = st.slider("Full energy (1-20):", 1, 20, 10, help="Maximum energy the forager can have.")
    laziness = st.slider("Laziness (0-1):", 0.0, 1.0, 0.5, help="Probability of the forager resting after finding food.")st.slider("Laziness (0-1):", 0.0, 1.0, 0.5)

if st.button("Run Simulation"):
    width = height = 4 * max_energy
    space = np.ones((width + 1, height + 1))
    space[width // 2, height // 2] = 0
    food_sites = [(x, y) for x in range(width + 1) for y in range(height + 1)]
    x, y = width // 2, height // 2
    energy, is_resting, is_dead = max_energy, True, False
    path = [(x, y)]
    energy_history = [energy]
    food_history = [food_sites.copy()]

    while not is_dead:
        energy -= 1
        if energy <= 0:
            is_dead = True
        elif is_resting:
            if random.random() > laziness:
                is_resting = False
        else:
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            x += dx
            y += dy
            # Ensure forager stays within bounds
            x = max(0, min(x, width))
            y = max(0, min(y, height))
            if 0 <= x <= width and 0 <= y <= height and space[x, y] == 1:
                space[x, y] = 0
                energy = min(energy + max_energy, max_energy)
                if random.random() < laziness:
                    is_resting = True
        path.append((x, y))
        energy_history.append(energy)
        food_history.append([(i, j) for i in range(width + 1) for j in range(height + 1) if space[i, j] == 1])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    # Animation logic
    frames = len(path)
    anim = FuncAnimation(
        fig,
        lambda frame: [
            ax1.clear(),
            ax2.clear(),
            ax1.set(xlim=(0, width), ylim=(0, height), title="Forager Movement"),
            ax2.set(xlim=(0, len(energy_history)), ylim=(0, max_energy + 2), title="Energy Level"),
            ax1.grid(True, linestyle="--", alpha=0.3),
            # Plot food sites
            ax1.plot(*zip(*[(fy, fx) for fx, fy in food_history[frame]]), "go", markersize=5, alpha=0.7, label="Food"),
            # Plot forager path
            ax1.plot(*zip(*[(py, px) for px, py in path[: frame + 1]]), "b-", alpha=0.3, label="Path"),
            # Plot forager position
            ax1.plot(path[frame][1], path[frame][0], "bo", markersize=10, label="Forager"),
            # Plot energy history
            ax2.plot(energy_history[: frame + 1], "r-", label="Energy"),
            # Display "Forager died!" message
            ax1.text(
                0.5,
                0.7,
                "Forager died!",
                ha="center",
                va="center",
                transform=ax1.transAxes,
                color="red",
                fontsize=20,
            )
            if frame == len(path) - 1
            else None,
        ],
        frames=frames,
        init_func=lambda: [
            ax1.clear(),
            ax2.clear(),
            ax1.set(xlim=(0, width), ylim=(0, height), title="Forager Movement"),
            ax2.set(xlim=(0, len(energy_history)), ylim=(0, max_energy + 2), title="Energy Level"),
            ax1.grid(True, linestyle="--", alpha=0.3),
        ],
        blit=False,
        interval=120,
    )

    html = anim.to_jshtml()
    plt.close(fig)

    lifetime = len(path) - 1
    eaten = 0 + int(((width + 1) * (height + 1)) - np.sum(space))

    with st.spinner("Simulating..."):
        st.write(f"Lifetime: {lifetime} steps | Cabbages eaten: {eaten}")
        st.components.v1.html(html, height=1000, width=1000, scrolling=True)
