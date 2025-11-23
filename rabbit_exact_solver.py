from collections import defaultdict
from math import comb

def solve_rabbit_exact():
    # State Definition: (Rabbits in Box A, Rabbits in Box B, Rabbits in Box C)
    # Initial State: 1 rabbit in A, 1 rabbit in B, 0 in C
    # We use a dictionary to store probability of each state
    current_states = {(1, 1, 0): 1.0}
    
    total_turns = 10
    
    print(f"--- Starting Exact Calculation (Total {total_turns} Turns) ---")

    for turn in range(1, total_turns + 1):
        next_states = defaultdict(float)
        
        # Iterate through all existing states
        for state, prob in current_states.items():
            # Skip negligible probabilities for optimization
            if prob < 1e-15: continue
                
            a, b, c = state
            
            # [Move Phase]
            # Calculate transition probabilities based on Binomial Distribution
            # Rabbits in A move to B or C (50/50 chance each)
            moves_from_a = []
            for i in range(a + 1):
                p = comb(a, i) * (0.5 ** a)
                moves_from_a.append((i, a - i, p)) # (to_B, to_C, prob)
                
            # Rabbits in B move to A or C
            moves_from_b = []
            for j in range(b + 1):
                p = comb(b, j) * (0.5 ** b)
                moves_from_b.append((j, b - j, p)) # (to_C, to_A, prob) -- destination index careful!
                
            # Rabbits in C move to A or B
            moves_from_c = []
            for k in range(c + 1):
                p = comb(c, k) * (0.5 ** c)
                moves_from_c.append((k, c - k, p)) # (to_A, to_B, prob)
                
            # Convolve all moves
            for (a_to_b, a_to_c, p_a) in moves_from_a:
                for (b_to_c, b_to_a, p_b) in moves_from_b:
                    for (c_to_a, c_to_b, p_c) in moves_from_c:
                        
                        trans_prob = prob * p_a * p_b * p_c
                        
                        # Count rabbits after move
                        new_a = b_to_a + c_to_a
                        new_b = a_to_b + c_to_b
                        new_c = a_to_c + b_to_c
                        
                        # [Breeding Phase]
                        # Rule: n + floor(n/2)
                        final_a = new_a + (new_a // 2)
                        final_b = new_b + (new_b // 2)
                        final_c = new_c + (new_c // 2)
                        
                        # Store next state
                        # Note: We do NOT sort the tuple to preserve structural integrity
                        next_state = (final_a, final_b, final_c)
                        next_states[next_state] += trans_prob
        
        current_states = next_states

    # Aggregate results by total rabbit count
    final_distribution = defaultdict(float)
    for state, prob in current_states.items():
        total_rabbits = sum(state)
        final_distribution[total_rabbits] += prob
        
    return final_distribution

# Execution and Output
if __name__ == "__main__":
    result = solve_rabbit_exact()

    print("\n=== Probability Distribution after 10 Turns (Exact Solution) ===")
    print(f"{'Rabbits':<10} | {'Probability (%)':<20}")
    print("-" * 35)

    sorted_keys = sorted(result.keys())
    cumulative = 0.0

    for k in sorted_keys:
        prob = result[k] * 100
        cumulative += prob
        # Show only significant probabilities or edge cases
        if prob > 0.01 or k == 94 or k == 2: 
            print(f"{k:<10} | {prob:.4f}%")
        elif k == 93:
            print(f"{'...':<10} | {'...':<20}")

    print("-" * 35)
    print(f"Total Probability Sum: {cumulative:.4f}%")
    print(f"Max Possible Rabbits: {max(result.keys())}")
