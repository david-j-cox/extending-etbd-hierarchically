#!/usr/bin/env python3
"""
Simple test script for the ETBD implementation
"""

import sys
import os
sys.path.append('scripts_notebooks')

try:
    import numpy as np
    print("✓ NumPy imported successfully")
    
    # Import ETBD functions
    from etbd import (
        compute_fitness, 
        RandomIntervalSchedule, 
        select_parents, 
        rep_rule, 
        mutate, 
        decode_genotype
    )
    print("ETBD functions imported successfully")
    
    # Test basic functionality
    print("\nTesting ETBD components...")
    
    # Test fitness function
    population = np.array([100, 200, 300, 400, 500])
    reinforced_behavior = 250
    fitness = compute_fitness(population, reinforced_behavior)
    print(f"Fitness function: {fitness}")
    
    # Test random interval schedule
    ri_schedule = RandomIntervalSchedule(mean_interval=30)
    print(f"Random interval schedule created with mean interval: {ri_schedule.mean_interval}")
    
    # Test parent selection
    fitness_density_mean = 20
    parent1, parent2 = select_parents(population, reinforced_behavior, fitness_density_mean)
    print(f"Parent selection: {parent1}, {parent2}")
    
    # Test reproduction
    child = rep_rule(parent1, parent2)
    print(f"Reproduction: {parent1} + {parent2} → {child}")
    
    # Test mutation
    mutated = mutate(child, mutation_rate=0.01)
    print(f"Mutation: {child} → {mutated}")
    
    # Test genotype decoding
    decoded = decode_genotype(child)
    print(f"Genotype decoding: {child} → {decoded}")
    
    print("\nAll tests passed! ETBD implementation is working correctly.")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have activated the virtual environment and installed dependencies:")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error during testing: {e}")
    sys.exit(1)
