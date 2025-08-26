#!/usr/bin/env python3
"""
Interactive ETBD Experimentation Script

This script allows users to easily experiment with different ETBD parameters
and examine the results interactively.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from etbd import run_etbd_simulation
from utils import save_plot, save_data
import time

def print_banner():
    """Print a welcome banner"""
    print("=" * 60)
    print("ETBD Interactive Experimentation Tool")
    print("=" * 60)
    print("Explore Jack McDowell's Evolutionary Theory of Behavioral Dynamics")
    print("Modify parameters, run simulations, and analyze results!")
    print("=" * 60)

def get_user_parameters():
    """Get simulation parameters from user input"""
    print("\nSimulation Parameters")
    print("-" * 30)
    
    # Population parameters
    print("\nPopulation Settings:")
    population_size = int(input("Population size (default: 100): ") or "100")
    phenotype_range = int(input("Phenotype range (0 to X, default: 1023): ") or "1023")
    
    # Evolutionary parameters
    print("\nEvolutionary Settings:")
    mutation_rate = float(input("Mutation rate (0.0-1.0, default: 0.01): ") or "0.01")
    fitness_density_mean = float(input("Fitness density mean (default: 20): ") or "20")
    
    # Reinforcement parameters
    print("\nReinforcement Settings:")
    mean_interval = float(input("Mean interval for RI schedule (seconds, default: 30): ") or "30")
    scaling_factor = float(input("Scaling factor (default: 0.01): ") or "0.01")
    
    # Target range parameters
    print("\nTarget Range Settings:")
    use_target_range = input("Use target response range? (y/n, default: n): ").strip().lower() or "n"
    
    if use_target_range in ['y', 'yes']:
        target_min = int(input("Target range minimum (default: 200): ") or "200")
        target_max = int(input("Target range maximum (default: 250): ") or "250")
        target_range = (target_min, target_max)
        print(f"Target range: {target_min}-{target_max}")
    else:
        target_range = None
        print("No target range - all responses will be reinforced")
    
    # Simulation parameters
    print("\nSimulation Settings:")
    time_step = float(input("Time step (seconds, default: 0.01): ") or "0.01")
    duration_minutes = float(input("Simulation duration (minutes, default: 5): ") or "5")
    total_simulation_duration = duration_minutes * 60
    
    return {
        'population_size': population_size,
        'phenotype_range': phenotype_range,
        'mutation_rate': mutation_rate,
        'fitness_density_mean': fitness_density_mean,
        'mean_interval': mean_interval,
        'scaling_factor': scaling_factor,
        'time_step': time_step,
        'total_simulation_duration': total_simulation_duration,
        'target_range': target_range
    }

def run_simulation(params):
    """Run the ETBD simulation with given parameters"""
    print(f"\nRunning simulation...")
    print(f"Duration: {params['total_simulation_duration']/60:.1f} minutes")
    print(f"Population: {params['population_size']} individuals")
    print(f"Mutation rate: {params['mutation_rate']}")
    print(f"RI schedule: {params['mean_interval']}s mean interval")
    
    start_time = time.time()
    
    logs = run_etbd_simulation(
        population_size=params['population_size'],
        mutation_rate=params['mutation_rate'],
        fitness_density_mean=params['fitness_density_mean'],
        phenotype_range=params['phenotype_range'],
        mean_interval=params['mean_interval'],
        scaling_factor=params['scaling_factor'],
        time_step=params['time_step'],
        total_simulation_duration=params['total_simulation_duration']
    )
    
    end_time = time.time()
    print(f"Simulation completed in {end_time - start_time:.1f} seconds")
    
    return logs

def analyze_results(logs, params):
    """Analyze and display simulation results"""
    df = pd.DataFrame(logs)
    
    if len(df) == 0:
        print("\nNo reinforcement events occurred during simulation.")
        print("Try increasing the simulation duration or adjusting parameters.")
        return None
    
    print(f"\nResults Summary:")
    print(f"Total reinforcement events: {len(df)}")
    print(f"Total reinforcers: {df['reinforcer_count'].iloc[-1]}")
    print(f"Reinforcement rate: {len(df) / (params['total_simulation_duration']/params['mean_interval']):.2f} reinforcers per hour")
    
    if params.get('target_range') is not None:
        target_min, target_max = params['target_range']
        print(f"Target range: {target_min}-{target_max}")
        # Calculate percentage of responses in target range
        in_target = df[df['reinforced'] == True]
        if len(df) > 0:
            target_percentage = (len(in_target) / len(df)) * 100
            print(f"Responses in target range: {len(in_target)}/{len(df)} ({target_percentage:.1f}%)")
    
    print(f"\nStatistics:")
    print(f"Mean phenotype: {df['phenotype'].mean():.2f}")
    print(f"Std phenotype: {df['phenotype'].std():.2f}")
    print(f"Min phenotype: {df['phenotype'].min():.2f}")
    print(f"Max phenotype: {df['phenotype'].max():.2f}")
    print(f"Mean fitness: {df['fitness'].mean():.2f}")
    
    return df

def create_plots(df, params):
    """Create and display plots"""
    if df is None or len(df) == 0:
        return
    
    print(f"\nCreating visualizations...")
    
    # Create a comprehensive figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Create title with target range info
    title = f'ETBD Simulation Results\nParameters: Pop={params["population_size"]}, μ={params["mutation_rate"]}, RI={params["mean_interval"]}s'
    if params.get('target_range') is not None:
        target_min, target_max = params['target_range']
        title += f', Target: {target_min}-{target_max}'
    
    fig.suptitle(title, fontsize=16)
    
    # Plot 1: Phenotype evolution with target range
    axes[0, 0].plot(df['generation'], df['phenotype'], 'b-', alpha=0.7, linewidth=1)
    if params.get('target_range') is not None:
        target_min, target_max = params['target_range']
        axes[0, 0].axhspan(target_min, target_max, alpha=0.3, color='green', label=f'Target Range ({target_min}-{target_max})')
        axes[0, 0].legend()
    axes[0, 0].set_xlabel('Generation')
    axes[0, 0].set_ylabel('Phenotype Value')
    axes[0, 0].set_title('Phenotype Evolution')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Fitness evolution
    axes[0, 1].plot(df['generation'], df['fitness'], 'r-', alpha=0.7, linewidth=1)
    axes[0, 1].set_xlabel('Generation')
    axes[0, 1].set_ylabel('Fitness')
    axes[0, 1].set_title('Fitness Evolution')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Cumulative reinforcers
    axes[0, 2].plot(df['generation'], df['reinforcer_count'], 'g-', alpha=0.7, linewidth=1)
    axes[0, 2].set_xlabel('Generation')
    axes[0, 2].set_ylabel('Cumulative Reinforcers')
    axes[0, 2].set_title('Reinforcement Accumulation')
    axes[0, 2].grid(True, alpha=0.3)
    
    # Plot 4: Phenotype distribution with target range
    axes[1, 0].hist(df['phenotype'], bins=20, alpha=0.7, color='purple', edgecolor='black', label='All Responses')
    if params.get('target_range') is not None:
        target_min, target_max = params['target_range']
        # Highlight reinforced responses
        reinforced_responses = df[df['reinforced'] == True]['phenotype']
        if len(reinforced_responses) > 0:
            axes[1, 0].hist(reinforced_responses, bins=20, alpha=0.8, color='green', edgecolor='black', label='Reinforced Responses')
        axes[1, 0].axvspan(target_min, target_max, alpha=0.2, color='green', label=f'Target Range ({target_min}-{target_max})')
        axes[1, 0].legend()
    axes[1, 0].set_xlabel('Phenotype Value')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Phenotype Distribution')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 5: Response distribution over time (first vs last half)
    if len(df) > 10:
        mid_point = len(df) // 2
        first_half = df[:mid_point]['phenotype']
        second_half = df[mid_point:]['phenotype']
        
        axes[1, 1].hist(first_half, bins=15, alpha=0.6, color='blue', label='First Half', density=True)
        axes[1, 1].hist(second_half, bins=15, alpha=0.6, color='red', label='Second Half', density=True)
        if params.get('target_range') is not None:
            target_min, target_max = params['target_range']
            axes[1, 1].axvspan(target_min, target_max, alpha=0.2, color='green', label=f'Target Range ({target_min}-{target_max})')
        axes[1, 1].legend()
        axes[1, 1].set_xlabel('Phenotype Value')
        axes[1, 1].set_ylabel('Density')
        axes[1, 1].set_title('Response Distribution: First vs Second Half')
        axes[1, 1].grid(True, alpha=0.3)
    else:
        # Fallback to fitness distribution if not enough data
        axes[1, 1].hist(df['fitness'], bins=20, alpha=0.7, color='orange', edgecolor='black')
        axes[1, 1].set_xlabel('Fitness')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Fitness Distribution')
        axes[1, 1].grid(True, alpha=0.3)
    
    # Plot 6: Scatter plot of phenotype vs fitness with reinforcement status
    if params.get('target_range') is not None:
        # Color by reinforcement status
        reinforced = df[df['reinforced'] == True]
        not_reinforced = df[df['reinforced'] == False]
        
        if len(not_reinforced) > 0:
            axes[1, 2].scatter(not_reinforced['phenotype'], not_reinforced['fitness'], 
                             alpha=0.6, s=20, color='red', label='Not Reinforced')
        if len(reinforced) > 0:
            axes[1, 2].scatter(reinforced['phenotype'], reinforced['fitness'], 
                             alpha=0.8, s=25, color='green', label='Reinforced')
        axes[1, 2].legend()
    else:
        axes[1, 2].scatter(df['phenotype'], df['fitness'], alpha=0.6, s=20)
    
    axes[1, 2].set_xlabel('Phenotype')
    axes[1, 2].set_ylabel('Fitness')
    axes[1, 2].set_title('Phenotype vs Fitness')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plot
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f'etbd_experiment_{timestamp}.png'
    save_plot(plt.gcf(), filename, dpi=300)
    
    plt.show()
    
    return filename

def save_results(df, params):
    """Save results to file"""
    if df is None or len(df) == 0:
        return
    
    # Add parameter information to the dataframe
    for key, value in params.items():
        df[f'param_{key}'] = value
    
    # Save to CSV
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f'etbd_experiment_{timestamp}.csv'
    save_data(df, filename)
    
    return filename

def show_sample_data(df):
    """Show a sample of the data"""
    if df is None or len(df) == 0:
        return
    
    print(f"\nSample Data (first 5 events):")
    print(df[['generation', 'phenotype', 'fitness', 'reinforcer_count']].head())
    
    if len(df) > 10:
        print(f"\nSample Data (last 5 events):")
        print(df[['generation', 'phenotype', 'fitness', 'reinforcer_count']].tail())

def main():
    """Main experimentation interface"""
    print_banner()
    
    while True:
        print(f"\nChoose an option:")
        print("1. Run new experiment")
        print("2. Run with default parameters")
        print("3. Quick demo (2 minutes)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Get custom parameters
            params = get_user_parameters()
            
        elif choice == '2':
            # Use default parameters
            params = {
                'population_size': 100,
                'phenotype_range': 1023,
                'mutation_rate': 0.01,
                'fitness_density_mean': 20,
                'mean_interval': 30,
                'scaling_factor': 0.01,
                'time_step': 0.01,
                'total_simulation_duration': 300,  # 5 minutes
                'target_range': None
            }
            print(f"\nUsing default parameters (5-minute simulation)")
            
        elif choice == '3':
            # Quick demo
            params = {
                'population_size': 50,
                'phenotype_range': 1023,
                'mutation_rate': 0.01,
                'fitness_density_mean': 20,
                'mean_interval': 30,
                'scaling_factor': 0.01,
                'time_step': 0.01,
                'total_simulation_duration': 120,  # 2 minutes
                'target_range': None
            }
            print(f"\nRunning quick demo (2-minute simulation)")
            
        elif choice == '4':
            print(f"\nThanks for experimenting with ETBD!")
            break
            
        else:
            print(f"\nInvalid choice. Please enter 1-4.")
            continue
        
        # Run simulation
        logs = run_simulation(params)
        
        # Analyze results
        df = analyze_results(logs, params)
        
        # Show sample data
        show_sample_data(df)
        
        # Create plots
        plot_filename = create_plots(df, params)
        
        # Save results
        data_filename = save_results(df, params)
        
        print(f"\nFiles saved:")
        if plot_filename:
            print(f"    Plot: {plot_filename}")
        if data_filename:
            print(f"    Data: {data_filename}")
        
        # Ask if user wants to continue
        try:
            continue_choice = input(f"\nRun another experiment? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print(f"\nThanks for experimenting with ETBD!")
                break
        except (EOFError, KeyboardInterrupt):
            print(f"\nThanks for experimenting with ETBD!")
            break

if __name__ == "__main__":
    main()
