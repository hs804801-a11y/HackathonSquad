"""
HACKATHON SQUAD - Maximum Weight Independent Set Solver
IIT Guwahati Coding Club - Even Semester Project 2026

Problem: 
Given a graph of N nodes (coders) and M edges (conflicts), find the Maximum Weight 
Independent Set (MWIS). Since MWIS is NP-Hard, this solution uses a hybrid heuristic 
approach: Multi-Greedy Initialization followed by Simulated Annealing Local Search.
"""

import sys
import time
import random
import os

def solve(n, m, skills, conflicts):
    # 1. Build adjacency list using sets for O(1) lookups
    adj = [set() for _ in range(n)]
    degrees = [0] * n
    for u, v in conflicts:
        adj[u].add(v)
        adj[v].add(u)
        degrees[u] += 1
        degrees[v] += 1

    def get_greedy(order):
        """Generates a valid team given a specific checking order."""
        selected = set()
        score = 0
        for i in order:
            # isdisjoint is extremely fast for checking overlap
            if adj[i].isdisjoint(selected):
                selected.add(i)
                score += skills[i]
        return selected, score

    # ── PHASE 1: Multi-Heuristic Initialization ─────────────────────────────
    # Instead of just one greedy approach, we race four different strategies
    # to guarantee we don't fall for obvious traps (like the Star Graph).
    
    orders = [
        # Heuristic 1: Maximize pure skill
        sorted(range(n), key=lambda i: skills[i], reverse=True),
        
        # Heuristic 2: Minimize conflicts (find highly cooperative subgraphs)
        sorted(range(n), key=lambda i: degrees[i]),
        
        # Heuristic 3: Balance skill vs. conflict footprint (density optimization)
        sorted(range(n), key=lambda i: skills[i] / (degrees[i] + 1), reverse=True),
        
        # Heuristic 4: Heavy penalty for high-degree nodes
        sorted(range(n), key=lambda i: skills[i] / (degrees[i]**2 + 1), reverse=True)
    ]

    best_set = set()
    best_score = -1

    # Establish the best baseline score before beginning local search
    for order in orders:
        s, score = get_greedy(order)
        if score > best_score:
            best_score = score
            best_set = set(s)

    # ── PHASE 2: Local Search via Simulated Annealing ───────────────────────
    # We attempt to iteratively improve the baseline set by swapping nodes.
    # Execution is strictly bound to the environment time limit.
    TIME_LIMIT = float(os.environ.get("CVM_TIME", "270"))
    start_time = time.time()
    
    current = set(best_set)
    current_score = best_score
    iteration = 0
    
    while time.time() - start_time < TIME_LIMIT:
        iteration += 1
        
        # Select candidate node in O(1) time
        candidate = random.randint(0, n - 1)
        
        if candidate not in current:
            # Identify all nodes in the current set that conflict with the candidate
            blockers = adj[candidate].intersection(current)
            
            if not blockers:
                # No conflict! Add them to the squad.
                current.add(candidate)
                current_score += skills[candidate]
            else:
                # Conflict detected. Are they worth firing the blockers for?
                # This fixes the trap: We compare against ALL blockers combined.
                blockers_score = sum(skills[b] for b in blockers)
                
                if skills[candidate] > blockers_score:
                    # The new coder is better than all their enemies combined. Swap them!
                    for b in blockers:
                        current.remove(b)
                        current_score -= skills[b]
                    current.add(candidate)
                    current_score += skills[candidate]
                    
        else:
            # Annealing mechanism: Introduce a 2% probability to drop a node currently
            # in the set. This allows the algorithm to temporarily accept a worse state
            # to escape local maxima and explore different graph neighborhoods.
            if random.random() < 0.02:
                current.remove(candidate)
                current_score -= skills[candidate]

        # Track the global maximum found across all iterations
        if current_score > best_score:
            best_score = current_score
            best_set = set(current)
            
        # Periodic reset to the global maximum prevents the annealing process
        # from diverging too far into sub-optimal states over millions of iterations.
        if iteration % 20000 == 0:
            current = set(best_set)
            current_score = best_score

    return best_set, best_score

def main():
    # Fast I/O to handle 200,000+ lines instantly
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1
    
    skills = []
    for _ in range(n):
        skills.append(int(input_data[idx])); idx += 1
        
    conflicts = []
    for _ in range(m):
        u = int(input_data[idx]) - 1; idx += 1
        v = int(input_data[idx]) - 1; idx += 1
        conflicts.append((u, v))
        
    selected, score = solve(n, m, skills, conflicts)
    
    # Required Output Format
    print(score)
    print(" ".join(str(i + 1) for i in sorted(selected)))

if __name__ == "__main__":
    main()
