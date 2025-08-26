import numpy as np

#Fitness Function
def compute_fitness(population, reinforced_behavior):
    fitness = np.abs(population - reinforced_behavior)
    return fitness

#Selection Rules
class RandomIntervalSchedule:
    def __init__(self, mean_interval, time_step=0.01):
        self.mean_interval = mean_interval
        self.time_step = time_step
        self.next_reinforcement_time = self._generate_next_interval()

    def _generate_next_interval(self):
        return np.random.exponential(self.mean_interval)

    def check_reinforcement(self, elapsed_time):
        if elapsed_time >= self.next_reinforcement_time:
            self.next_reinforcement_time += self._generate_next_interval()
            return True
        else:
            return False

def select_parents(population, reinforced_behavior, fitness_density_mean):
    fitness = compute_fitness(population, reinforced_behavior)
    
    # Build probability distribution inversely proportional to fitness
    selection_probs = np.exp(-fitness / fitness_density_mean)
    selection_probs /= np.sum(selection_probs)

    parent1 = np.random.choice(population, p=selection_probs)
    parent2 = np.random.choice(population, p=selection_probs)
    return parent1, parent2

def rep_rule(parent1, parent2):
    # Convert to 10-bit binary strings
    parent1_bits = np.array(list(np.binary_repr(parent1, width=10))).astype(int)
    parent2_bits = np.array(list(np.binary_repr(parent2, width=10))).astype(int)

    # Generate random mask
    mask = np.random.randint(0, 2, 10)

    # Recombine bits according to mask
    child_bits = np.where(mask == 1, parent1_bits, parent2_bits)

    # Convert back to integer
    child_behavior = int(''.join(child_bits.astype(str)), 2)

    return child_behavior

def mutate(phenotype, mutation_rate=0.01):
    bits = np.array(list(np.binary_repr(phenotype, width=10))).astype(int)
    for i in range(len(bits)):
        if np.random.rand() < mutation_rate:
            bits[i] = 1 - bits[i]  # Flip bit
    return int(''.join(bits.astype(str)), 2)

def decode_genotype(genotype, bin_length=10, mapping='identity'):
    bits = np.array(list(np.binary_repr(genotype, width=bin_length))).astype(int)

    if mapping == 'identity':
        return genotype
    elif mapping == 'normalized':
        # Normalize to range [0, 1]
        return int(''.join(bits.astype(str)), 2) / (2**bin_length - 1)
    elif mapping == 'vector':
        # Return vector of bits
        return bits
    else:
        raise ValueError(f"Unknown mapping strategy: {mapping}")

# Logging setup
logs = {
    "generation": [],
    "genotype": [],
    "phenotype": [],
    "reinforced": [],
    "reinforcer_count": [],
    "fitness": []
}

cumulative_reinforcers = 0

def log_event(gen, genotype, reinforced_behavior, reinforcer_obtained):
    global cumulative_reinforcers

    phenotype = decode_genotype(genotype)
    reinforced = reinforcer_obtained
    fitness = abs(genotype - reinforced_behavior)  # can adjust as needed

    if reinforced:
        cumulative_reinforcers += 1

    logs["generation"].append(gen)
    logs["genotype"].append(genotype)
    logs["phenotype"].append(phenotype)
    logs["reinforced"].append(reinforced)
    logs["reinforcer_count"].append(cumulative_reinforcers)
    logs["fitness"].append(fitness)

# Main simulation function
def run_etbd_simulation(
    population_size=100,
    mutation_rate=0.01,
    fitness_density_mean=20,
    phenotype_range=1023,
    mean_interval=30,
    scaling_factor=0.01,
    time_step=0.01,
    total_simulation_duration=3600
):
    """
    Run the ETBD simulation with specified parameters.
    
    Returns:
        dict: Simulation logs containing generation, genotype, phenotype, 
              reinforcement, reinforcer count, and fitness data.
    """
    # Initialize random population of phenotypes
    population = np.random.randint(0, phenotype_range+1, population_size)

    # Random Interval schedule: RI 30 sec
    ri_schedule = RandomIntervalSchedule(mean_interval=mean_interval)

    # Simulation variables
    simulation_time = 0
    generation = 0

    # Clear previous logs
    global logs, cumulative_reinforcers
    logs = {
        "generation": [],
        "genotype": [],
        "phenotype": [],
        "reinforced": [],
        "reinforcer_count": [],
        "fitness": []
    }
    cumulative_reinforcers = 0

    # Simulation Loop
    while simulation_time < total_simulation_duration:
        # Emit random behavior
        emitted_behavior = np.random.choice(population)
        
        # Determine response probability based on phenotype → response rate mapping
        response_rate = emitted_behavior * scaling_factor
        prob_response_per_step = response_rate * time_step

        if np.random.rand() < prob_response_per_step:
            # Response occurred
            if ri_schedule.check_reinforcement(simulation_time):
                # Reinforcement delivered -> Selection & Reproduction
                generation += 1
                
                # Select parents based on fitness
                parent1, parent2 = select_parents(population, emitted_behavior, fitness_density_mean)
                
                # Reproduce
                child = rep_rule(parent1, parent2)
                
                # Mutate
                child = mutate(child, mutation_rate=mutation_rate)
                
                # Replace random member of population with offspring
                replace_index = np.random.randint(0, population_size)
                population[replace_index] = child
                
                # Log the event
                log_event(generation, child, emitted_behavior, True)
        
        # Advance time
        simulation_time += time_step
    
    return logs

# Example usage and parameter setup
if __name__ == "__main__":
    # Parameters
    population_size = 100
    mutation_rate = 0.01
    fitness_density_mean = 20  # The smaller, the stronger selection pressure
    phenotype_range = 1023

    # Initialize random population of phenotypes
    population = np.random.randint(0, phenotype_range+1, population_size)

    # Random Interval schedule: RI 30 sec
    ri_schedule = RandomIntervalSchedule(mean_interval=30)

    # Response mapping: Map phenotype → response rate
    scaling_factor = 0.01  # 10 phenotype units = 0.1 responses/sec
    time_step = 0.01
    simulation_time = 0
    total_simulation_duration = 3600  # 1 hour

    # Simulation Loop
    while simulation_time < total_simulation_duration:

        # Emit random behavior
        emitted_behavior = np.random.choice(population)
        
        # Determine response probability based on phenotype → response rate mapping
        response_rate = emitted_behavior * scaling_factor
        prob_response_per_step = response_rate * time_step

        if np.random.rand() < prob_response_per_step:
            # Response occurred
            if ri_schedule.check_reinforcement(simulation_time):
                # Reinforcement delivered -> Selection & Reproduction
                
                # Select parents based on fitness
                parent1, parent2 = select_parents(population, emitted_behavior, fitness_density_mean)
                
                # Reproduce
                child = rep_rule(parent1, parent2)
                
                # Mutate
                child = mutate(child, mutation_rate=mutation_rate)
                
                # Replace random member of population with offspring
                replace_index = np.random.randint(0, population_size)
                population[replace_index] = child
        
        # Advance time
        simulation_time += time_step