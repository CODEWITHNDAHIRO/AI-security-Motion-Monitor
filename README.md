# AI Security Motion Monitor

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer--Vision-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A real-time security surveillance system that utilizes **Frame Differencing** and **Gaussian Blur pre-processing** to identify movement. This project is designed as a modular AI vision lab to explore motion tracking and automated event logging.

## Key Features
- **Intelligent Motion Detection:** Implements absolute difference calculation (`absdiff`) between a static background and live frames.
- **Automated Event Logging:** Generates timestamped `.jpg` snapshots in the `/alerts` directory upon detecting significant movement.
- **Live HUD (Heads-Up Display):** Features a dynamic status bar that updates in real-time to indicate "IDLE" or "MOTION DETECTED" states.
- **Noise Reduction:** Optimized using 21x21 Gaussian kernels to prevent false positives from light flickering or camera sensor noise.

##  Technical Workflow

1. **Grayscale Conversion:** Reduces data complexity for faster processing.
2. **Background Modeling:** Establishes a baseline "static" environment.
3. **Delta Calculation:** Subtracts current frame from background to isolate changes.
4. **Thresholding & Dilation:** Converts subtle changes into solid binary masks for contour detection.

##  Project Structure
```text
AI-Security-Motion-Monitor/
├── alerts/               # Local storage for motion-triggered captures
├── main.py               # Core application and vision loop
├── requirements.txt      # Dependency management
└── README.md             # Project documentation
