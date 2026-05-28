# HACKATHON SQUAD
### IIT Guwahati Coding Club — Even Semester Project 2026

---

## Problem Summary

Given `N` coders (each with a skill rating) and `M` conflict pairs (coders who refuse to work together), select a **conflict-free subset** of coders that **maximizes the total skill rating**.

In graph theory, this is the **Maximum Weight Independent Set (MWIS)** problem — coders are vertices, conflicts are edges, and skill ratings are vertex weights. MWIS is NP-Hard, meaning a mathematically perfect solution for large inputs (N = 200,000) is computationally impossible within the 5-minute time limit. We solve it using a two-phase hybrid heuristic.

---

## Algorithm

### Phase 1 — Multi-Heuristic Greedy Initialization

A single greedy approach fails on certain graph shapes. For example, on a "Star Graph" where one high-skill coder conflicts with many weaker coders, picking by skill first selects that one coder and blocks everyone else — even if the weaker coders combined score much higher.

To avoid such traps, we run **four different greedy strategies** and pick the best result:

| # | Strategy | Logic |
|---|----------|-------|
| 1 | **Pure Skill** | Pick coders with highest skill rating first |
| 2 | **Cooperative** | Pick coders with fewest conflicts first |
| 3 | **Density Ratio** | Sort by `skill / (conflicts + 1)` — balances skill vs conflict footprint |
| 4 | **Aggressive Ratio** | Sort by `skill / (conflicts² + 1)` — heavily penalizes high-conflict coders |

### Phase 2 — Simulated Annealing (Local Search)

Starting from the best greedy result, the algorithm runs a fast loop until the time limit, randomly trying three types of moves:

| Move | Condition | Action |
|------|-----------|--------|
| **Instant Hire** | Candidate has zero conflicts with current team | Add them immediately |
| **Many-to-One Swap** | Candidate conflicts with some team members, but their skill beats all blockers combined | Fire the blockers, hire the candidate |
| **Annealing Drop** | Candidate is already on the team | 2% chance to drop them — allows escaping local maxima |

Every 20,000 iterations, the active team resets to the best known solution to prevent the algorithm from drifting into poor states.

---

## Files

| File | Description |
|------|-------------|
| `hackathon_squad.py` | Main solver — submit this |
| `tester.py` | Automated correctness verifier |
| `test1.txt` | Sample: chain of 5 coders |
| `test2.txt` | Sample: chain of 8 coders |
| `test3.txt` | Sample: 6 coders, no conflicts |

---

## How to Run

### Requirements
- Python 3.x (no external libraries needed)

### Run the solver
```bash
python3 hackathon_squad.py < input.txt
```

For a quick test (3 seconds instead of 5 minutes):
```bash
CVM_TIME=3 python3 hackathon_squad.py < input.txt
```

### Input Format
```
N M
S1 S2 ... SN
u1 v1
u2 v2
...
```

### Output Format
```
<total skill score>
<space-separated coder indices, 1-indexed, ascending>
```

---

## Sample Test Cases

### test1.txt — Chain of 5
```
5 4
10 20 30 40 50
1 2
2 3
3 4
4 5
```
**Output:**
```
90
1 3 5
```
Coders 1, 3, 5 (skills 10+30+50=90). No two are adjacent in the chain.

---

### test2.txt — Chain of 8
```
8 7
100 200 150 300 250 180 400 120
1 2
2 3
3 4
4 5
5 6
6 7
7 8
```
**Output:**
```
900
2 4 7
```
Coders 2, 4, 7 (skills 200+300+400=900).

---

### test3.txt — No Conflicts
```
6 0
500 300 700 200 900 100
```
**Output:**
```
2700
1 2 3 4 5 6
```
No conflicts → select everyone → total = 2700.

---

## How We Verified Correctness — tester.py

Since this is a heuristic (approximate) solver, we cannot just check one answer. We need to confirm it finds the **mathematically perfect answer** across many cases.

`tester.py` does this automatically using a **stress testing** approach:

### How it works

1. **Generates a random test case** — random N coders, random skill ratings, random conflict pairs.
2. **Runs a brute-force solver** — checks every possible subset using recursion (DFS). This is too slow for large inputs but gives the provably correct answer for small ones (N ≤ 20).
3. **Runs our heuristic solver** on the same input.
4. **Compares both answers** — if our heuristic matches the perfect brute-force score, the test passes. If not, it immediately prints the failing case so we can debug.

### How to run it
```bash
python3 tester.py
```
Press `Ctrl + C` to stop. The more tests that pass, the more confidence we have.

### Results
After running for 500 seconds, the solver passed **1000 consecutive randomly generated test cases with zero failures**, confirming the heuristic consistently finds the optimal answer.

```
✅ Test 1 Passed (Score: 238)
✅ Test 2 Passed (Score: 124)
✅ Test 3 Passed (Score: 307)
...
✅ Test 1000 Passed (Score: 547)
```

## Known Limitations

- This is a heuristic solver, not an exact algorithm — it does not guarantee the mathematically perfect answer for all inputs
- On certain graph structures like dense random graphs or highly connected subgraphs, the greedy initialization may miss better solutions
- The simulated annealing uses a fixed 2% drop probability — this value was tuned manually and may not be optimal for all graph types
- Performance depends heavily on the time limit — with only 1-2 seconds the solution quality drops significantly compared to the full 5-minute run
- For very sparse graphs (few conflicts), the algorithm works perfectly. For very dense graphs (many conflicts), results may vary
- The stress tester only validates small cases (N ≤ 20) — correctness on large inputs (N = 200,000) cannot be mathematically proven, only empirically observed

## What I Learned

- How to model real-world problems as graph theory problems (Maximum Weight Independent Set)
- Why some problems are NP-Hard and why exact solutions are computationally impossible at scale
- How greedy algorithms work and why a single greedy strategy can fail on certain graph shapes
- How Simulated Annealing works as a local search technique to escape local maxima
- How to combine multiple heuristics to build a more robust solver
- How to design a stress tester that compares a heuristic against a brute-force solution
- How to handle fast I/O in Python for large inputs (200,000+ lines)
- How to bound algorithm execution using environment-controlled time limits
