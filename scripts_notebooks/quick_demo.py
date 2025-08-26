#!/usr/bin/env python3
"""
Quick demo of the ETBD simulation
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from etbd import run_etbd_simulation
from utils import save_plot

def main():
    print("=== ETBD Quick Demo ===\n")
    
    # Run a short simulation for demo purposes
    print("Running ETBD simulation (5 minutes)...")
    logs = run_etbd_simulation(
        population_size=50,
        mutation_rate=0.01,
        fitness_density_mean=20,
        phenotype_range=1023,
        mean_interval=30,
        scaling_factor=0.01,
        time_step=0.01,
        total_simulation_duration=300  # 5 minutes
    )
    
    # Analyze results
    df = pd.DataFrame(logs)
    
    if len(df) > 0:
        print(f"Simulation completed!")
        print(f"Total reinforcement events: {len(df)}")
        print(f"Mean phenotype: {df['phenotype'].mean():.2f}")
        print(f"Mean fitness: {df['fitness'].mean():.2f}")
        
        # Create a simple plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['generation'], df['phenotype'], 'b-', alpha=0.7, linewidth=1)
        plt.xlabel('Generation')
        plt.ylabel('Phenotype Value')
        plt.title('ETBD: Phenotype Evolution Over Generations')
        plt.grid(True, alpha=0.3)
        save_plot(plt.gcf(), 'etbd_demo_plot.png', dpi=150)
        plt.show()
        
        # Show first few events
        print("\nFirst 5 reinforcement events:")
        print(df[['generation', 'phenotype', 'fitness', 'reinforcer_count']].head())
        
    else:
        print("No reinforcement events occurred during the simulation.")
        print("This can happen with short simulation times or certain parameter combinations.")

if __name__ == "__main__":
    main()
