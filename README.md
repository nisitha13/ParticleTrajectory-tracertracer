This project focuses on accurately tracking the motion of individual bacterium or microscopic particles across video sequences, stacking the frame data, analyzing movement patterns, and providing data ready for machine learning models.
Highly applicable in the healthcare sector for studying micro-organism behavior, particle motion, and bio-diagnostics.

How It Works 🌟
Input:
The user provides the path to the root folder.
This root folder contains multiple subfolders (each representing a single video) with 60 frames per subfolder (images).

Processing:
Each set of frames from a subfolder is stacked to simulate a continuous video.
The user is prompted to select a Region of Interest (ROI) — focusing on a particular bacterium or particle.

Trajectory Tracking:
The movement of the selected bacterium across frames is tracked and plotted.
A trajectory plot is generated, visualizing the movement across time and space.

Output:
A .csv file is created, containing:
Frame Number
Timestamp (milliseconds)
X-coordinate
Y-coordinate
The dataset is structured to be readily used by machine learning models for predictive analysis.
Detailed trajectory plots are exported, showing the complete path of the tracked bacterium.

Key Features 🌍
📁 Supports large datasets with hundreds of subfolders and thousands of frames.
🖼️ Interactive Region of Interest (ROI) selection for precise tracking.
📊 Automatic generation of trajectory plots and coordinate datasets.
🤖 Outputs ML-ready CSV files for training predictive models on particle motion.
💉 Highly relevant for healthcare, biophysics, and nanotechnology research.

Applications 💡
Healthcare Diagnostics: Understanding bacterial behavior and dynamics.
Microbiology Research: Tracking micro-particles in fluidic environments.
AI/ML Modeling: Building predictive models for microorganism motion.
Bioengineering: Studying movement in synthetic biological constructs.

