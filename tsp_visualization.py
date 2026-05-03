
# TSP Visualization and Comparison
# MSML 606 Extra credit project
# tsp_visualization.py
# Visualizes the TSP solution using matplotlib and networkx
# Compares to brute force and greeedy alogorithms.
# Taner Bulbul
# Muazuddin Syed
# AI and External Use: Main code for brute-forec and greedy (neraest neighbor)
# follows class notes and own knowledge. For Held-Karp, we utiilized calss notes
# for DP and memoization. Used GitHub Copilot for some of the bitmask 
# implementation and path construction. We added comparison logic and code.
# Used Copilot for application network graph part but most of the user interaction logic
# is developed by us.
import time
from itertools import permutations

import math
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

# List of cities and their coordinates
cities = [
    ("Scaggsville", 39.1425, -76.8900),
    ("Columbia", 39.2011, -76.8581),
    ("Baltimore", 39.2904, -76.6122),
    ("Annapolis", 38.9784, -76.4922),
    ("Washington D.C.", 38.9072, -77.0369),
    ("Silver Spring", 38.9907, -77.0261),
    ("Rockville", 39.0840, -77.1528),
    ("Frederick", 39.4143, -77.4105),
    ("Hagerstown", 39.6418, -77.7200),
    ("Alexandria", 38.8048, -77.0469),
    ("Arlington", 38.8783, -77.0687),
    ("Fairfax", 38.8462, -77.3064),
    ("Bel Air", 39.5359, -76.3483),
    ("Westminster", 39.5759, -77.0000),
    ("Laurel", 39.0993, -76.8483),
    ("College Park", 38.9897, -76.9378)
]
# Calculate the distance between two cities using Earth;s curvature.
def distance(city1, city2):
    lat1, lon1 = city1[1], city1[2]
    lat2, lon2 = city2[1], city2[2]
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Build the a distance adjacency matrix for the cities.
def build_distance_matrix(city_list):
    n = len(city_list)
    dist = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(distance(city_list[i], city_list[j]))
        dist.append(row)
    return dist

# Brute force TSP (for small n)
# Experimentallyy more 11-12 cities may lock your computer!!!
def brute_force_tsp(start_idx, city_list):
    n = len(city_list)
    dist = build_distance_matrix(city_list)
    nodes = [i for i in range(n) if i != start_idx]
    min_cost = float('inf')
    best_path = None
    op_count = 0
    # each permutation is a possible tour
    for perm in permutations(nodes): # (n-1)! permutations
        cost = 0
        prev = start_idx
        for node in perm:
            cost += dist[prev][node]
            prev = node
            op_count += 1  # one operation per edge, for comparison
        cost += dist[prev][start_idx]  # return to start
        op_count += 1
        if cost < min_cost:
            min_cost = cost
            best_path = [start_idx] + list(perm)
    return min_cost, best_path, city_list, op_count

# Dynamic Programming TSP (Held-Karp)
def held_karp(start_idx, city_list):
    n = len(city_list)
    dist = build_distance_matrix(city_list)
    C = {}
    op_count = 0
    for k in range(n): # Initialize Base cases
        if k == start_idx:
            continue
        # for each city initially only the cost from start 
        # to that city is known, and the parent is start_idx
        C[(1 << k, k)] = (dist[start_idx][k], start_idx) # (cost, parent)
        op_count += 1 # for statistics
    for subset_size in range(2, n): # Iterate over subsets of increasing size
        for subset in combinations([i for i in range(n) if i != start_idx], subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == k:
                        continue
                    # the cost to reach k from the subset defined 
                    # by prev_bits is the cost to reach city m plus the
                    # cost from m to k
                    res.append((C[(prev_bits, m)][0] + dist[m][k], m))
                    op_count += 1
                    # State is defined by the subset of cities 
                    # visited (bits) and the last city visited (k)
                C[(bits, k)] = min(res)
    bits = 0
    for i in range(n):
        if i != start_idx:
            bits |= 1 << i
    res = []
    for k in range(n):
        if k == start_idx:
            continue
        # cost for returning to the starting city
        res.append((C[(bits, k)][0] + dist[k][start_idx], k))
        op_count += 1
    opt, parent = min(res)
    # Reconstruct path in correct order (start -> ... -> start)
    path = [start_idx]
    last = parent
    bits_cpy = bits
    order = []
    for i in range(n - 1):
        order.append(last)
        new_bits = bits_cpy & ~(1 << last)
        _, last = C[(bits_cpy, last)]
        bits_cpy = new_bits
    order = order[::-1]  # reverse to get visiting order
    path.extend(order)
    return opt, path, city_list, op_count
# Greedy (Nearest Neighbor) TSP
def greedy_tsp(start_idx, city_list):
    n = len(city_list)
    dist = build_distance_matrix(city_list)
    unvisited = set(range(n)) # use a set, no repeated cities allowed
    path = [start_idx]
    total_cost = 0
    op_count = 0
    current = start_idx
    unvisited.remove(current)
    # for each unvisited city, find the nearest one and go there
    while unvisited:
        # choose the nearest unvisited city
        next_city = min(unvisited, key=lambda city: dist[current][city])
        total_cost += dist[current][next_city]
        path.append(next_city)
        current = next_city
        # once we visit a city, remove from the set
        unvisited.remove(current)
        op_count += 1
    total_cost += dist[current][start_idx]  # return to start
    path.append(start_idx)
    op_count += 1
    return total_cost, path, city_list, op_count

# Graph the TSP using networkx and mathplotlib
def plot_tsp(path, method_name=None):
    G = nx.DiGraph() # directed graph
    pos = {}
    for idx, (name, lat, lon) in enumerate(cities):
        pos[idx] = (lon, lat)
        G.add_node(idx, label=name)
        
    edge_labels = {}
    n_edges = len(path)
    
    for i in range(n_edges - 1):
        u, v = path[i], path[i+1]
        dist_uv = distance(cities[u], cities[v])
        G.add_edge(u, v)
        edge_labels[(u, v)] = f"{dist_uv:.1f} km\n({i+1})"

    labels = {i: cities[i][0] for i in range(len(cities))}
    plt.figure(figsize=(9.6, 7.2))
    
    # FIX: Changed nx.draw to nx.draw_networkx
    nx.draw_networkx(G, pos, with_labels=True, labels=labels, node_size=700, node_color='lightblue', font_size=9, arrowsize=20)
    
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='r', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue', font_size=9, label_pos=0.7)
    
    # Title and Labels will now display properly
    if method_name:
        plt.title(f"{method_name} - Optimal TSP Tour")
        # Optional: Changes the actual popup window name (if running locally)
        try:
            plt.gcf().canvas.manager.set_window_title(method_name)
        except AttributeError:
            pass 
    else:
        plt.title("Optimal TSP Tour")
        
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    # Adding a grid helps visualize the coordinate space
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Ensure axes are explicitly forced on (just in case)
    plt.axis('on')
    
    plt.show()

# ask for starting city and number of cities to visit
# then ask for algorithms to run. Individual or all
# Print the results and graph the tour for each selected 
# algorithm
def main():

    print("Cities (enter the number in the first column):")
    for i, (name, _, _) in enumerate(cities):
        print(f"{i+1}: {name}")

    # Prompt user for starting city (1-based index)
    while True:
        try:
            start_idx = int(input(f"Enter the index of the starting city (1-{len(cities)}): ")) - 1
            if 0 <= start_idx < len(cities):
                break
            else:
                print(f"Please enter a number between 1 and {len(cities)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Ask user how many cities to include (besides starting city)
    max_cities = len(cities)
    while True:
        try:
            num_cities = int(input(f"How many cities (including the starting city) to include in the search? (2-{max_cities}): "))
            if 2 <= num_cities <= max_cities:
                break
            else:
                print(f"Please enter a number between 2 and {max_cities}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Build the city list: always include the starting city, then the next (num_cities-1) cities from the list (excluding the starting city)
    city_list = [cities[start_idx]] + [cities[i] for i in range(len(cities)) if i != start_idx][:num_cities-1]
    # The new start_idx is always 0 in city_list
    new_start_idx = 0

    print("\nWhich TSP algorithm do you want to run?")
    print("1: Held-Karp (Dynamic Programming)")
    print("2: Brute Force (only for small n)")
    print("3: Greedy (Nearest Neighbor)")
    print("4: All of the above")
    while True:
        algo_choice = input("Enter your choice (1/2/3/4): ").strip()
        if algo_choice in ("1", "2", "3", "4"):
            break
        else:
            print("Please enter 1, 2, 3, or 4.")

    n = len(city_list)
    results = []
    # Held-Karp
    if algo_choice in ("1", "4"):
        t0 = time.perf_counter()
        opt_cost, opt_path, used_cities, hk_actual_ops = held_karp(new_start_idx, city_list)
        t1 = time.perf_counter()
        print(f"\nHeld-Karp Algorithm:")
        print(f"Optimal tour cost: {opt_cost:.2f} km")
        print("Optimal tour:")
        for idx in opt_path:
            print(used_cities[idx][0])
        print(used_cities[opt_path[0]][0])
        heldkarp_ops = n * n * (2 ** n)
        print(f"Held-Karp time: {t1-t0:.4f} seconds")
        print(f"Held-Karp estimated operations: {heldkarp_ops:,}")
        print(f"Held-Karp actual operations: {hk_actual_ops:,}")
        plot_tsp(opt_path + [opt_path[0]], method_name="Held-Karp")
        results.append(("Held-Karp", opt_cost, t1-t0))

    # Brute Force
    if algo_choice in ("2", "4"):
        if num_cities > 12:
            print("\nBrute force TSP is very slow for more than 12 cities. Skipping brute force.")
        else:
            t2 = time.perf_counter()
            bf_cost, bf_path, bf_cities, bf_actual_ops = brute_force_tsp(new_start_idx, city_list)
            t3 = time.perf_counter()
            from math import factorial
            brute_ops = factorial(n-1)
            print(f"\nBrute Force Algorithm:")
            print(f"Optimal tour cost: {bf_cost:.2f} km")
            print("Optimal tour:")
            for idx in bf_path:
                print(bf_cities[idx][0])
            print(bf_cities[bf_path[0]][0])
            print(f"Brute force time: {t3-t2:.4f} seconds")
            print(f"Brute force operations: {brute_ops:,}")
            print(f"Brute force actual operations: {bf_actual_ops:,}")
            plot_tsp(bf_path + [bf_path[0]], method_name="Brute Force")
            results.append(("Brute Force", bf_cost, t3-t2))

    # Greedy
    if algo_choice in ("3", "4"):
        t4 = time.perf_counter()
        gr_cost, gr_path, gr_cities, gr_actual_ops = greedy_tsp(new_start_idx, city_list)
        t5 = time.perf_counter()
        print(f"\nGreedy Algorithm (Nearest Neighbor):")
        print(f"Tour cost: {gr_cost:.2f} km")
        print("Tour:")
        for idx in gr_path:
            print(gr_cities[idx][0])
        print(f"Greedy time:0 {t5-t4:.4f} seconds")
        print(f"Greedy actual operations: {gr_actual_ops:,}")
        plot_tsp(gr_path, method_name="Greedy")
        results.append(("Greedy", gr_cost, t5-t4))

    # Print summary table once at the end
    if results:
        print("\nSummary Table:")
        print(f"{'Method':<15}{'Tour Cost (km)':>18}{'Time (s)':>15}")
        print("-"*48)
        for method, cost, timing in results:
            print(f"{method:<15}{cost:>18.2f}{timing:>15.4f}")

if __name__ == "__main__":
    main()
