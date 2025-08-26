#!/usr/bin/env python3
"""
Quick Parameter Testing for ETBD

A simple script for quickly testing different parameter combinations
without the full interactive menu.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from etbd import run_etbd_simulation
from utils import save_plot, save_data
import time

def test_parameters(params, description=""):
    """Test a specific parameter combination"""
    print(f"\n🧪 Testing: {description}")
    print(f"Parameters: {params}")
    
    start_time = time.time()
    
    logs = run_etbd_simulation(**params)
    
    end_time = time.time()
    print(f"✅ Completed in {end_time - start_time:.1f} seconds")
    
    df = pd.DataFrame(logs)
    
    if len(df) > 0:
        print(f"📊 Results: {len(df)} events, mean phenotype: {df['phenotype'].mean():.1f}")
        
        # Create simple plot
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        plt.plot(df['generation'], df['phenotype'], 'b-', alpha=0.7)
        plt.title('Phenotype Evolution')
        plt.xlabel('Generation')
        plt.ylabel('Phenotype')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 3, 2)
        plt.plot(df['generation'], df['fitness'], 'r-', alpha=0.7)
        plt.title('Fitness Evolution')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 3, 3)
        plt.hist(df['phenotype'], bins=20, alpha=0.7, color='purple')
        plt.title('Phenotype Distribution')
        plt.xlabel('Phenotype')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        plot_filename = f'parameter_test_{description.replace(" ", "_")}_{timestamp}.png'
        save_plot(plt.gcf(), plot_filename, dpi=150)
        plt.show()
        
        # Save data
        data_filename = f'parameter_test_{description.replace(" ", "_")}_{timestamp}.csv'
        save_data(df, data_filename)
        
        return df
    else:
        print("❌ No reinforcement events occurred")
        return None

def main():
    """Run parameter tests"""
    print("🧬 ETBD Parameter Testing")
    print("=" * 50)
    
    # Test 1: Default parameters
    default_params = {
        'population_size': 100,
        'mutation_rate': 0.01,
        'fitness_density_mean': 20,
        'phenotype_range': 1023,
        'mean_interval': 30,
        'scaling_factor': 0.01,
        'time_step': 0.01,
        'total_simulation_duration': 300  # 5 minutes
    }
    
    test_parameters(default_params, "Default Parameters")
    
    # Test 2: High mutation rate
    high_mutation_params = default_params.copy()
    high_mutation_params['mutation_rate'] = 0.1
    high_mutation_params['total_simulation_duration'] = 180  # 3 minutes
    
    test_parameters(high_mutation_params, "High Mutation Rate")
    
    # Test 3: Large population
    large_pop_params = default_params.copy()
    large_pop_params['population_size'] = 500
    large_pop_params['total_simulation_duration'] = 180  # 3 minutes
    
    test_parameters(large_pop_params, "Large Population")
    
    # Test 4: Fast reinforcement
    fast_reinforcement_params = default_params.copy()
    fast_reinforcement_params['mean_interval'] = 10
    fast_reinforcement_params['total_simulation_duration'] = 180  # 3 minutes
    
    test_parameters(fast_reinforcement_params, "Fast Reinforcement")
    
    # Test 5: Strong selection pressure
    strong_selection_params = default_params.copy()
    strong_selection_params['fitness_density_mean'] = 5
    strong_selection_params['total_simulation_duration'] = 180  # 3 minutes
    
    test_parameters(strong_selection_params, "Strong Selection")
    
    print(f"\n🎉 Parameter testing completed!")
    print(f"Check the figures/ and data/ directories for results.")

if __name__ == "__main__":
    main()
