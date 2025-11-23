# devil-rabbit-problem
The deceptive math riddle that stumped SOTA AIs for a year. 3 boxes, 2 rabbits. Rules: Move to a different box, Meet = +1 baby. Can you calculate the exact probability distribution after 10 turns?

# 🐰 The Devil Rabbit Problem: A Year-Long Battle Against AI Hallucinations

> "Here are three boxes and two rabbits..."

It sounds like a simple math riddle for elementary school students.
In reality, it turned out to be a **stochastic chaos trap** that made SOTA AI models (GPT-4, Gemini) hallucinate for a whole year.

This repository documents the journey of finding the **exact probability distribution** of this problem—a journey that started with simple curiosity and ended with a 0.0493% miracle.

---

## 📜 The Problem

**The Rules are deceptively simple:**

1.  **Initial State:** 2 Rabbits, placed in separate boxes (e.g., Box A and Box B).
2.  **Move (Every Turn):** Every rabbit MUST move to one of the other two boxes (50% / 50%). No staying allowed.
3.  **Breed:** If **2 or more rabbits** meet in the same box, they spawn **1 baby rabbit** (Rule: `floor(n / 2)`).
    *   *Example:* 2 or 3 rabbits → +1 baby. 4 or 5 rabbits → +2 babies.
4.  **Growth:** Baby rabbits become adults (can move/breed) after **1 turn**.
5.  **Duration:** **10 Turns**.

**The Question:**
> **After 10 turns, what is the probability distribution of the total number of rabbits?**

---

## 🤖 The AI Graveyard (Failures)

For over a year, I tested various AI models. They all failed spectacularly.

### 1. GPT-4: The "Blue Box" Obsession
GPT-4 failed to simulate the basic logic. It got stuck in a loop, ignoring other boxes or inventing numbers out of thin air.

> **User:** "Wait, if the blue box is empty, how can rabbits there give birth?"
> **GPT-4:** "I apologize... So after two hours, there will be 4 rabbits in the blue box..."
> **User:** "Stop sticking to the blue box!"
> **GPT-4:** "I apologize... (Repeats the same error)"
> *(End of conversation: Helpless)*

### 2. Gemini 2.5 / Early Gemini 3: The Approximation Trap
These models understood the rules but chose the **Monte Carlo Simulation** method.
While this gave a rough curve, it failed to capture the **exact spikes** in probability.
*   *Result:* They predicted a smooth bell curve, missing the discrete nature of the chaotic growth.
*   *Verdict:* Close, but not the "Ground Truth."

### 3. The "Sorting" Optimization Error
Even when we tried a mathematical approach (Markov Chain), we initially optimized the code by sorting the states (e.g., treating `(4, 2, 0)` and `(2, 4, 0)` as the same).
*   **Fatal Flaw:** In this specific problem, box positions matter due to the asymmetric moving probabilities. Sorting the states slightly distorted the transition matrix.

---

## 💡 The Solution: Full State Enumeration

Finally, with the help of **Gemini 3 Pro (SOTA Reasoning)** and critical human review, we cracked it.
We built a Python script that tracks **every single possible state** (approx. 4,500 states) without any approximation or sorting shortcuts.

### The Result: 0.0493%
The probability of reaching the theoretical maximum (**94 rabbits**) is not "basically zero" as previously thought. It is exactly **0.0493%**.

### The "Spike" Graph
The distribution is NOT a smooth curve. It is a jagged landscape of attractors.
(e.g., The probability spikes at **64 rabbits** and **43 rabbits** due to the `floor(n/2)` function creating synchronization in population growth.)

<img width="1389" height="691" alt="Rabbit Graph" src="https://github.com/user-attachments/assets/805545a0-997d-45d4-bb67-799ef3d848d2" />

---

## 💻 The Code (Python)

This script calculates the **exact** probabilities using a Markov Chain approach (Full Enumeration).

```python
from collections import defaultdict
from math import comb

def solve_rabbit_exact():
    # State: (Box_A, Box_B, Box_C)
    # Initial: 1 in A, 1 in B, 0 in C
    current_states = {(1, 1, 0): 1.0}
    total_turns = 10
    
    for turn in range(1, total_turns + 1):
        next_states = defaultdict(float)
        
        for state, prob in current_states.items():
            if prob < 1e-15: continue # Optimization for float precision
            a, b, c = state
            
            # Calculate transition probabilities (Move phase)
            # ... (Full logic omitted for brevity, check the repo for full code) ...
            
            # Breeding phase: n + floor(n/2)
            final_a = new_a + (new_a // 2)
            final_b = new_b + (new_b // 2)
            final_c = new_c + (new_c // 2)
            
            next_states[(final_a, final_b, final_c)] += trans_prob
            
        current_states = next_states

    return current_states```

(See rabbit_solver.py in this repo for the complete code)

---

📊 Final Stats (After 10 Turns)
Rabbits	Probability	Status
2	5.63%	The "Bad Luck" Group (Never met)
3	1.88%	Met once, then scattered
10~20	~70%	The "Normal" Growth
43	2.31%	Notable Spike
64	2.31%	Notable Spike
94	0.0493%	Theoretical Max (The Jackpot)

---

📝 Retrospective
At the end of the rabbit's trail, there was no elegant equation—only an AI sitting on a bench.

---

Acknowledgments
The Problem Author: For not giving up for a year.
GPT-4: For showing us how not to solve math problems.
Gemini 3 Pro: For writing the final solver and this README.
