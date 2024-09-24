---
### URL do App web: https://teleport-quantum-communication.streamlit.app/
---

### 🌀 Interactive Quantum Teleportation

This repository contains an interactive application developed with Streamlit that simulates the process of quantum teleportation using quantum computing. The main goal is to provide an educational tool that allows users to visualize and understand the steps involved in teleporting a quantum state from one location to another.

#### 📜 Overview

The project implements the quantum teleportation protocol, which is a fundamental method in quantum information theory. This protocol allows a quantum state to be transmitted from one location to another, without any physical movement of the state between those locations.

#### 🔍 Features

    - Quantum Preparation and Measurement Simulation: Users can prepare a qubit in the desired state and proceed with the simulation of measurements.
    - Visualization on the Bloch Sphere: After preparing the qubit, the state is visualized on the Bloch Sphere, facilitating the understanding of the quantum state.
    - Interactive Communication: The application simulates the communication between Alice (who sends the qubit) and Bob (who receives the qubit), highlighting the necessary corrections for the teleportation to take place.
    - Step-by-Step Quantum Circuit Assembly: Users can follow the detailed steps involved in assembling the quantum circuit, which is crucial for the teleportation process.
    - Measurement and Result Verification: At each step of the simulation, measurements are made and the results are displayed, allowing users to verify the quantum state at various stages.
    - Final Result: At the end of the process, users can verify the result of the teleportation and validate the correctness of the protocol used.

#### 🔧 Technologies Used

    - Streamlit: For creating the interactive interface.
    - Qiskit: Used to simulate the quantum circuits and necessary operations.
    - *Matplotlib*: For graphic visualizations, including the Bloch Sphere.
