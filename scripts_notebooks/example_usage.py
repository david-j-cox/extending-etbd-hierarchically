#!/usr/bin/env python3
"""
Example usage of the ETBD simulation
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from etbd import run_etbd_simulation
from utils import save_plot, save_data

def analyze_simulation_results(logs):
    """Analyze and plot simulation results"""
    
    # Convert logs to DataFrame for easier analysis
    df = pd.DataFrame(logs)
    
    print(f"Simulation completed!")
    print(f"Total generations: {len(df)}")
    print(f"Total reinforcers: {df['reinforcer_count'].iloc[-1] if len(df) > 0 else 0}")
    
    if len(df) == 0:
        print("No reinforcement events occurred during simulation.")
        return
    
    # Create plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('ETBD Simulation Results', fontsize=16)
    
    # Plot 1: Phenotype evolution over generations
    axes[0, 0].plot(df['generation'], df['phenotype'], 'b-', alpha=0.7)
    axes[0, 0].set_xlabel('Generation')
    axes[0, 0].set_ylabel('Phenotype Value')
    axes[0, 0].set_title('Phenotype Evolution')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Fitness over generations
    axes[0, 1].plot(df['generation'], df['fitness'], 'r-', alpha=0.7)
    axes[0, 1].set_xlabel('Generation')
    axes[0, 1].set_ylabel('Fitness')
    axes[0, 1].set_title('Fitness Evolution')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Cumulative reinforcers
    axes[1, 0].plot(df['generation'], df['reinforcer_count'], 'g-', alpha=0.7)
    axes[1, 0].set_xlabel('Generation')
    axes[1, 0].set_ylabel('Cumulative Reinforcers')
    axes[1, 0].set_title('Reinforcement Accumulation')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Phenotype distribution (histogram)
    axes[1, 1].hist(df['phenotype'], bins=20, alpha=0.7, color='purple', edgecolor='black')
    axes[1, 1].set_xlabel('Phenotype Value')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Phenotype Distribution')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_plot(plt.gcf(), 'etbd_simulation_results.png', dpi=300)
    plt.show()
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Mean phenotype: {df['phenotype'].mean():.2f}")
    print(f"Std phenotype: {df['phenotype'].std():.2f}")
    print(f"Min phenotype: {df['phenotype'].min():.2f}")
    print(f"Max phenotype: {df['phenotype'].max():.2f}")
    print(f"Mean fitness: {df['fitness'].mean():.2f}")
    print(f"Reinforcement rate: {len(df) / (3600/30):.2f} reinforcers per hour")

def main():
    """Run example ETBD simulation"""
    
    print("Running ETBD Simulation...")
    print("Parameters:")
    print("- Population size: 100")
    print("- Mutation rate: 0.01")
    print("- Fitness density mean: 20")
    print("- Mean interval: 30 seconds")
    print("- Simulation duration: 1 hour")
    print()
    
    # Run simulation with default parameters
    logs = run_etbd_simulation(
        population_size=100,
        mutation_rate=0.01,
        fitness_density_mean=20,
        phenotype_range=1023,
        mean_interval=30,
        scaling_factor=0.01,
        time_step=0.01,
        total_simulation_duration=3600  # 1 hour
    )
    
    # Analyze and plot results
    analyze_simulation_results(logs)
    
    # Save results to CSV
    df = pd.DataFrame(logs)
    save_data(df, 'etbd_simulation_data.csv')

if __name__ == "__main__":
    main()
