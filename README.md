# TSP with Dynamic Programming

**MSML 606 — Extra Credit Project**  
Authors: Taner Bulbul, Muazuddin Syed

## Overview

An interactive Python application that solves the **Travelling Salesman Problem (TSP)** for a set of real-world cities in the Maryland/DC metro area. The program compares three algorithms — Held-Karp (Dynamic Programming), Brute Force, and Greedy (Nearest Neighbor) — and visualizes the resulting tour on a geographic network graph.

## Cities

The dataset includes 16 cities with real GPS coordinates:

Scaggsville, Columbia, Baltimore, Annapolis, Washington D.C., Silver Spring, Rockville, Frederick, Hagerstown, Alexandria, Arlington, Fairfax, Bel Air, Westminster, Laurel, College Park

Distances are calculated using the **Haversine formula** (great-circle distance in km).

## Algorithms

| Algorithm | Time Complexity | Notes |
|---|---|---|
| **Held-Karp** (DP) | O(n² · 2ⁿ) | Optimal solution via bitmask DP + memoization |
| **Brute Force** | O((n-1)!) | Exact optimal; limited to ≤ 12 cities |
| **Greedy (Nearest Neighbor)** | O(n²) | Heuristic; fast but not always optimal |

## Requirements

- Python
- `matplotlib`
- `networkx`

Install dependencies:

pip install matplotlib networkx

## How to run: 

python tsp_visualization.py

The program will interactively prompt you to:

1. **Select a starting city** (1–16)
2. **Choose how many cities** to include in the tour (2–16)
   - >  Brute Force is automatically skipped for more than 12 cities to prevent excessive computation time.
3. **Select an algorithm** to run:
   - `1` — Held-Karp (Dynamic Programming)
   - `2` — Brute Force
   - `3` — Greedy (Nearest Neighbor)
   - `4` — All of the above

## Output

- **Console**: Tour order, total distance (km), execution time, and estimated vs. actual operation counts are printed on the console
- **Plot**: A directed network graph for each methods showing the tour route overlaid on a coordinate grid with edge labels showing distance and step order
- **Summary table**: Side-by-side comparison of all selected algorithms

## Example Summary Table

```
Method          Tour Cost (km)        Time (s)
------------------------------------------------
Held-Karp               245.30         0.1523
Brute Force             245.30         3.8741
Greedy                  267.14         0.0003
```

## External Resource Usage

- Brute force and greedy algorithms follow class notes and the authors' own knowledge.
- Held-Karp bitmask implementation and path reconstruction assisted by GitHub Copilot.
- Network graph visualization assisted by GitHub Copilot; user interaction logic developed by the authors.
