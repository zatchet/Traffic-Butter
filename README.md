#  Traffic Butter: Genetic-Based Traffic Flow Optimization

See presentation [here](slides.pdf).

## Overview

This project provides a systematic strategy for optimizing the placement and configuration of various traffic measures in a simulated urban environment. We use a genetic algorithm with crossovers and mutations to iteratively find optimal configurations over many generations.
 
## Document Overview
- run.py: the genetic algorithm itself
- traffic_simulation.py: the implementation of the environment
- simulation_view.py: the GUI
- routefinder.py: the A* route-finding
  
## Getting Started

### Prerequisites

Ensure you have the following installed to run the front end application
- Python 3.10+
- pygame

### Usage

1. Set constants and hyper-parameters as desired in `constants.py` and at the top of `run.py`

2. ```bash
   pip install pygame
   python3 run.py
   ```
