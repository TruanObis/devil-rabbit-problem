import random
from collections import Counter

def run_simulation(num_simulations=100000, num_turns=10):
    results = []

    for _ in range(num_simulations):
        # Initial State
        # List of adult rabbits (numbers represent box indices 0, 1, 2)
        # Initially, they are in different boxes (e.g., Box 0 and Box 1)
        adults = [0, 1]
        
        # Babies born this turn (cannot move or breed yet)
        # Stores the location (box index)
        babies = [] 

        for turn in range(num_turns):
            # 1. Growth Phase (Turn Start)
            # Babies from the previous turn become adults -> join the 'adults' list
            adults.extend(babies)
            babies = [] # Clear the nursery

            # 2. Move Phase
            # All adults must move to one of the other two boxes (not staying)
            next_positions = []
            for current_box in adults:
                # Identify possible moves (any box except the current one)
                possible_moves = [box for box in [0, 1, 2] if box != current_box]
                # Random choice (50/50)
                next_positions.append(random.choice(possible_moves))
            adults = next_positions

            # 3. Breeding Phase
            # Count rabbits in each box
            box_counts = Counter(adults)
            
            # Check breeding condition for each box
            for box in box_counts:
                # Rule: If 2 or more rabbits meet in a box, 1 baby is born.
                # Logic: floor(n/2) logic is applied as '1 baby per box event' here for simplicity,
                # but for exact match with the "Exact Solver", strict rules should be consistent.
                if box_counts[box] >= 2:
                    babies.append(box) # Add a baby to this box

        # After 10 turns, calculate total rabbits (Adults + Babies born in the last turn)
        total_rabbits = len(adults) + len(babies)
        results.append(total_rabbits)

    return results

def print_probabilities(results):
    total_runs = len(results)
    counts = Counter(results)
    
    # Sort by number of rabbits
    sorted_counts = sorted(counts.items())

    print(f"--- Simulation Results ({total_runs:,} runs) ---")
    print(f"{'Rabbits':<10} | {'Prob (%)':<15} | {'Count':<10}")
    print("-" * 40)

    expected_value = 0
    for rabbit_num, count in sorted_counts:
        prob = (count / total_runs) * 100
        print(f"{rabbit_num:<10} | {prob:>6.2f}%         | {count:,}")
        expected_value += rabbit_num * (count / total_runs)
    
    print("-" * 40)
    print(f"Expected Value: {expected_value:.2f} rabbits")

# Execution
if __name__ == "__main__":
    # For higher precision, increase num_simulations (e.g., to 1,000,000)
    sim_results = run_simulation(num_simulations=100000, num_turns=10)
    print_probabilities(sim_results)
