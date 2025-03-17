import tkinter as tk
from tkinter import messagebox

def find_all_matchings(graph, n):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if graph[i][j] == 1]
    all_matchings = []
    def build_matchings(current_matching, remaining_edges, matched_vertices):
        all_matchings.append(current_matching[:])
        for i, (u, v) in enumerate(remaining_edges):
            if u not in matched_vertices and v not in matched_vertices:
                build_matchings(current_matching + [(u, v)], remaining_edges[i + 1:], matched_vertices | {u, v})
    build_matchings([], edges, set())
    return all_matchings

def find_maximum_matching(graph, n):
    all_matchings = find_all_matchings(graph, n)
    return max(all_matchings, key=len) if all_matchings else []

def find_maximal_matching(graph, n):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if graph[i][j] == 1]
    matched = set()
    maximal_matching = []
    for u, v in edges:
        if u not in matched and v not in matched:
            maximal_matching.append((u, v))
            matched.add(u)
            matched.add(v)
    return maximal_matching

def find_perfect_matching(graph, n):
    maximum_matching = find_maximum_matching(graph, n)
    return maximum_matching if len(maximum_matching) == n // 2 else None

def dfs(graph, v, visited):
    visited[v] = True
    for i, connected in enumerate(graph[v]):
        if connected == 1 and not visited[i]:
            dfs(graph, i, visited)

def is_connected(graph, n):
    visited = [False] * n
    start_vertex = next((i for i in range(n) if sum(graph[i]) > 0), -1)
    if start_vertex == -1:
        return True
    dfs(graph, start_vertex, visited)
    return all(visited[i] or sum(graph[i]) == 0 for i in range(n))

def find_eulerian_path(graph, n):
    if not is_connected(graph, n):
        return None
    odd_degree_vertices = [i for i in range(n) if sum(graph[i]) % 2 != 0]
    if len(odd_degree_vertices) != 0 and len(odd_degree_vertices) != 2:
        return None
    start_vertex = odd_degree_vertices[0] if odd_degree_vertices else 0
    stack, path = [start_vertex], []
    local_graph = [row[:] for row in graph]
    while stack:
        v = stack[-1]
        has_unvisited_edge = False
        for u in range(n):
            if local_graph[v][u] == 1:
                stack.append(u)
                local_graph[v][u] = local_graph[u][v] = 0
                has_unvisited_edge = True
                break
        if not has_unvisited_edge:
            path.append(stack.pop())
    return path if len(path) == sum(sum(row) for row in graph) // 2 + 1 else None

def process_input():
    input_text = text_area.get("1.0", tk.END).strip()
    adj_matrix = []
    try:
        for line in input_text.split("\n"):
            row = list(map(int, line.strip().split(",")))
            adj_matrix.append(row)
        n = len(adj_matrix)
        maximal_match = find_maximal_matching(adj_matrix, n)
        maximum_match = find_maximum_matching(adj_matrix, n)
        perfect_match = find_perfect_matching(adj_matrix, n)
        eulerian_path = find_eulerian_path(adj_matrix, n)
        maximal_label.config(text=f"Maximal Matching: {maximal_match}")
        maximum_label.config(text=f"Maximum Matching: {maximum_match}")
        perfect_label.config(text=f"Perfect Matching: {perfect_match}" if perfect_match else "Perfect Matching: None")
        eulerian_label.config(text=f"Eulerian Path: {eulerian_path}" if eulerian_path else "Eulerian Path: None")
        if eulerian_path is not None:
            visualize_eulerian_path(adj_matrix, eulerian_path)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

def show_instructions():
    instructions = (
        "1. Enter the adjacency matrix for your graph.\n"
        "2. Each row should have the same number of elements, separated by commas.\n"
        "3. The graph is considered undirected and unweighted.\n"
        "4. Ensure the input is formatted correctly, using only 0s and 1s.\n"
        "\nExample matrix:\n"
        "0,1,1,0\n1,0,1,1\n1,1,0,1\n0,1,1,0"
    )
    messagebox.showinfo("Instructions", instructions)

def visualize_eulerian_path(graph, path):
    canvas.delete("all")
    n = len(graph)
    radius = 30
    coords = [(100 * (i + 1), 100 + (i // 2) * 100) for i in range(n)]  
    for i, (x, y) in enumerate(coords):
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue")
        canvas.create_text(x, y, text=f'V{i}', font=("Arial", 10))
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                x1, y1 = coords[i]
                x2, y2 = coords[j]
                canvas.create_line(x1, y1, x2, y2)
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

root = tk.Tk()
root.title("Graph Matching and Eulerian Path Finder")
instruction_button = tk.Button(root, text="Instructions", command=show_instructions)
instruction_button.pack(pady=10)

default_matrix = "0,1,1,0\n1,0,1,1\n1,1,0,1\n0,1,1,0"
text_area = tk.Text(root, height=10, width=50)
text_area.pack(pady=5)
text_area.insert(tk.END, default_matrix)

submit_button = tk.Button(root, text="Process Graph", command=process_input)
submit_button.pack(pady=20)

maximal_label = tk.Label(root, text="", font=("Arial", 12))
maximal_label.pack(pady=5)
maximum_label = tk.Label(root, text="", font=("Arial", 12))
maximum_label.pack(pady=5)
perfect_label = tk.Label(root, text="", font=("Arial", 12))
perfect_label.pack(pady=5)
eulerian_label = tk.Label(root, text="", font=("Arial", 12))
eulerian_label.pack(pady=5)

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(pady=10)

root.mainloop()
