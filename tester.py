import random
import time

# Import your solve function from your main file!
from hackathon_squad import solve

def brute_force_mwis(n, skills, conflicts):
    """
    A mathematically perfect (but incredibly slow) algorithm.
    It checks every single valid combination to find the absolute max score.
    """
    adj = [set() for _ in range(n)]
    for u, v in conflicts:
        adj[u].add(v)
        adj[v].add(u)

    best_score = 0

    def dfs(idx, current_set, current_score):
        nonlocal best_score
        if idx == n:
            if current_score > best_score:
                best_score = current_score
            return

        # Path 1: Don't pick this coder
        dfs(idx + 1, current_set, current_score)

        # Path 2: Pick this coder (if they don't conflict with our current set)
        if adj[idx].isdisjoint(current_set):
            current_set.add(idx)
            dfs(idx + 1, current_set, current_score + skills[idx])
            current_set.remove(idx)

    dfs(0, set(), 0)
    return best_score

def generate_random_case(max_n=20, max_m=40):
    """Generates random hackathon scenarios."""
    n = random.randint(5, max_n)
    max_possible_edges = n * (n - 1) // 2
    m = random.randint(0, min(max_m, max_possible_edges))
    
    skills = [random.randint(10, 100) for _ in range(n)]
    
    edges = set()
    while len(edges) < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edges.add(tuple(sorted((u, v))))
            
    return n, m, skills, list(edges)

def run_stress_test():
    print("Starting Stress Test... Press Ctrl+C to stop.")
    test_case = 1
    
    # We set the CVM_TIME very low for testing so it runs fast
    import os
    os.environ["CVM_TIME"] = "0.5" 
    
    while True:
        n, m, skills, conflicts = generate_random_case()
        
        # 1. Get the perfect answer
        true_max = brute_force_mwis(n, skills, conflicts)
        
        # 2. Get your heuristic's answer
        _, heuristic_score = solve(n, m, skills, conflicts)
        
        if heuristic_score < true_max:
            print(f"\n❌ FAILED ON TEST CASE {test_case}!")
            print(f"N: {n}, M: {m}")
            print(f"Skills: {skills}")
            print(f"Conflicts: {conflicts}")
            print(f"Brute Force Found: {true_max}")
            print(f"Your Code Found:   {heuristic_score}")
            break
        else:
            print(f"✅ Test {test_case} Passed (Score: {heuristic_score})")
            
        test_case += 1

if __name__ == "__main__":
    run_stress_test()
