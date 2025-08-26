# Evolutionary Theory of Behavioral Dynamics (ETBD)

This repository contains implementations of Jack McDowell's Evolutionary Theory of Behavioral Dynamics, a computational model that applies evolutionary principles to explain operant behavior.

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `scripts_notebooks/` - Contains the main ETBD implementation and analysis scripts
- `figures/` - Output plots and visualizations (automatically generated)
- `data/` - Simulation data and results (automatically generated)
- `venv/` - Virtual environment (created during setup)
- `requirements.txt` - Python package dependencies

## Usage

The main ETBD implementation is in `scripts_notebooks/etbd.py`. This script includes:

- Fitness function computation
- Random interval reinforcement schedules
- Parent selection based on fitness
- Evolutionary reproduction and mutation
- Genotype-phenotype mapping
- Event logging and data collection

## Key Components

- **Fitness Function**: Computes fitness based on distance from reinforced behavior
- **Selection**: Parents selected inversely proportional to fitness
- **Reproduction**: Crossover recombination of binary genotypes
- **Mutation**: Random bit flipping with specified mutation rate
- **Reinforcement Schedules**: Random interval schedules for operant conditioning

## Running Simulations

To run the ETBD simulation:

```bash
cd scripts_notebooks
python etbd.py
```

To run the example with analysis and plotting:

```bash
cd scripts_notebooks
python example_usage.py
```

To run a quick demo:

```bash
cd scripts_notebooks
python quick_demo.py
```

For interactive exploration, you can also use Jupyter notebooks:

```bash
jupyter notebook
```

## Output Organization

The scripts automatically organize outputs:
- **Plots** are saved to the `figures/` directory with timestamps
- **Data** is saved to the `data/` directory with timestamps
- Files are automatically timestamped to prevent overwriting

## References

This implementation is based on Jack McDowell's Evolutionary Theory of Behavioral Dynamics, which applies evolutionary algorithms to model operant behavior and reinforcement learning.
