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

### Installation
#### Only follow these steps if you wish to run the front end application locally. 

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-traffic-sim.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ai-traffic-sim
   ```

3. Install the required packages:
   ```bash
   pip install pygame
   ```
4. Set constants and hyper-parameters as desired in `constants.py` and at the top of `run.py`

5. Run the algorithm:
   ```bash
   python3 run.py
   ```
