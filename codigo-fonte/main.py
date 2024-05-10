import time
import heapq
from collections import deque
import random
import tracemalloc

class LightsOut:
    def __init__(self, size, initial_state=None):
        self.size = size
        if initial_state:
            self.state = initial_state
        else:
            self.state = tuple(tuple(0 for _ in range(size)) for _ in range(size))

    def is_goal(self, state):
        return all(all(cell == 1 for cell in row) for row in state)

    def get_neighbors(self, state):
        neighbors = []
        for r in range(self.size):
            for c in range(self.size):
                new_state = self.toggle(state, r, c)
                neighbors.append((new_state, (r, c)))
        return neighbors

    def toggle(self, state, r, c):
        temp = [list(row) for row in state]
        for dr, dc in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                temp[nr][nc] = 1 - temp[nr][nc]
        return tuple(tuple(row) for row in temp)

    def h(self, state):
        """Heurística: Número de luzes apagadas / 5"""
        off_count = sum(row.count(0) for row in state)
        return off_count / 5

# --- Wrapper para medição ---
def measure_algorithm(alg_func, problem):
    tracemalloc.start()
    start_time = time.time()
    
    # Executa o algoritmo
    result = alg_func(problem)
    
    if len(result) == 3:
        res_path, nodes_expanded, _ = result
    else:
        res_path, nodes_expanded = result
        
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    duration = time.time() - start_time
    memory_kb = peak / 1024
    
    return res_path, nodes_expanded, duration, memory_kb

# --- Algoritmos de Busca ---
def bfs(problem):
    start_node = problem.state
    if problem.is_goal(start_node):
        return [], 0

    queue = deque([(start_node, [])])
    visited = {start_node}
    nodes_expanded = 0

    while queue:
        current_state, path = queue.popleft()
        nodes_expanded += 1

        for next_state, action in problem.get_neighbors(current_state):
            if next_state not in visited:
                if problem.is_goal(next_state):
                    return path + [action], nodes_expanded
                visited.add(next_state)
                queue.append((next_state, path + [action]))
    return None, nodes_expanded

def dfs(problem, limit=20):
    stack = [(problem.state, [], 0)]
    visited = {problem.state: 0}
    nodes_expanded = 0

    while stack:
        current_state, path, depth = stack.pop()
        nodes_expanded += 1

        if problem.is_goal(current_state):
            return path, nodes_expanded

        if depth < limit:
            for next_state, action in problem.get_neighbors(current_state):
                if next_state not in visited or visited[next_state] > depth + 1:
                    visited[next_state] = depth + 1
                    stack.append((next_state, path + [action], depth + 1))
    return None, nodes_expanded

def a_star(problem):
    start_node = problem.state
    pq = [(problem.h(start_node), start_node, [], 0)]
    visited = {start_node: 0}
    nodes_expanded = 0

    while pq:
        f, current_state, path, g = heapq.heappop(pq)
        nodes_expanded += 1

        if problem.is_goal(current_state):
            return path, nodes_expanded

        for next_state, action in problem.get_neighbors(current_state):
            new_g = g + 1
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                f = new_g + problem.h(next_state)
                heapq.heappush(pq, (f, next_state, path + [action], new_g))
    return None, nodes_expanded

def greedy(problem):
    start_node = problem.state
    pq = [(problem.h(start_node), start_node, [])]
    visited = {start_node}
    nodes_expanded = 0

    while pq:
        h, current_state, path = heapq.heappop(pq)
        nodes_expanded += 1

        if problem.is_goal(current_state):
            return path, nodes_expanded

        for next_state, action in problem.get_neighbors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                heapq.heappush(pq, (problem.h(next_state), next_state, path + [action]))
    return None, nodes_expanded

def hill_climbing(problem, max_restarts=10):
    total_nodes_expanded = 0
    for _ in range(max_restarts):
        current_state = problem.state
        path = []
        while True:
            total_nodes_expanded += 1
            if problem.is_goal(current_state):
                return path, total_nodes_expanded
            neighbors = problem.get_neighbors(current_state)
            next_state, action = min(neighbors, key=lambda x: problem.h(x[0]))
            if problem.h(next_state) >= problem.h(current_state):
                break
            current_state = next_state
            path.append(action)
    return None, total_nodes_expanded


# --- Execução de Experimentos ---
def run_experiment(size, complexity=3):
    print(f"\n{'='*95}")
    print(f" EXPERIMENTO: Tabuleiro {size}x{size} | Complexidade Inicial: {complexity} cliques")
    print(f"{'='*95}")
    
    game = LightsOut(size)
    initial_state = tuple(tuple(1 for _ in range(size)) for _ in range(size))
    for _ in range(complexity):
        r, c = random.randint(0, size-1), random.randint(0, size-1)
        initial_state = game.toggle(initial_state, r, c)
    
    game.state = initial_state
    
    algorithms = [
        ("BFS", bfs),
        ("DFS", lambda p: dfs(p, limit=complexity+10)),
        ("Greedy", greedy),
        ("A*", a_star),
        ("Hill Climbing", hill_climbing)
    ]
    
    header = f"{'Algoritmo':<15} | {'Status/Passos':<20} | {'Nós Exp.':<10} | {'Tempo (s)':<12} | {'Memória (KB)':<12}"
    print(header)
    print("-" * len(header))
    
    for name, alg in algorithms:
        res_path, nodes, duration, memory = measure_algorithm(alg, game)
        
        status = f"Sucesso ({len(res_path)})" if res_path is not None else "Falha"
        print(f"{name:<15} | {status:<20} | {nodes:<10} | {duration:<12.4f} | {memory:<12.2f}")
    print(f"{'='*95}")

if __name__ == "__main__":
    # Testando diferentes tamanhos
    for s in [2, 3, 4, 5]:
        run_experiment(s, complexity=s*s // 2)
    
    
