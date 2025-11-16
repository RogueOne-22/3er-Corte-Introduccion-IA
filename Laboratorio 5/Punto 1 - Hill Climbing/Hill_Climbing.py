import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import random
from matplotlib.animation import FuncAnimation

from matplotlib.widgets import Button
import warnings

# Configuración inicial
NUM_PEOPLE = 8
warnings.filterwarnings("ignore", category=UserWarning)
random.seed(42)
np.random.seed(42)

# --- 1. Generación de Datos ---

def create_satisfaction_matrix(n_people):
    matrix = np.random.randint(0, 11, size=(n_people, n_people))
    np.fill_diagonal(matrix, 0)
    conflict_indices = np.random.choice(range(n_people * n_people), 5, replace=False)
    for idx in conflict_indices:
        i = idx // n_people
        j = idx % n_people
        if i != j:
            matrix[i, j] = np.random.randint(-10, 0)
    return matrix

# --- 2. Algoritmo Hill Climbing ---

def calculate_total_satisfaction(arrangement, matrix):
    total_sat = 0
    n = len(arrangement)
    for i in range(n):
        p1, p2 = arrangement[i], arrangement[(i + 1) % n]
        total_sat += matrix[p1, p2] + matrix[p2, p1]
    return total_sat

def get_neighbors(arrangement):
    neighbors = []
    n = len(arrangement)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = list(arrangement)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def hill_climbing(matrix):
    n = len(matrix)
    current_arrangement = list(range(n))
    random.shuffle(current_arrangement)
    current_score = calculate_total_satisfaction(current_arrangement, matrix)
    history = [(list(current_arrangement), current_score)]

    while True:
        neighbors = get_neighbors(current_arrangement)
        scores = [calculate_total_satisfaction(nb, matrix) for nb in neighbors]

        better = [(nb, sc) for nb, sc in zip(neighbors, scores) if sc > current_score]

        if len(better) > 0:
            nb, sc = random.choice(better)
            current_arrangement, current_score = nb, sc
            history.append((list(nb), sc))
            continue

        threshold = 2  # Aceptar vecinos peores por poco
        near = [(nb, sc) for nb, sc in zip(neighbors, scores)
                if current_score - sc <= threshold and sc != current_score]

        if len(near) > 0 and random.random() < 0.25:  # 25% chance
            nb, sc = random.choice(near)
            current_arrangement, current_score = nb, sc
            history.append((list(nb), sc))
            continue

        break

    return current_arrangement, current_score, history

# --- 3. Visualización ---

def plot_heatmap(matrix, ax):
    sns.heatmap(matrix, annot=True, fmt="d", cmap="vlag", center=0,
                xticklabels=[f"P{i}" for i in range(len(matrix))],
                yticklabels=[f"P{i}" for i in range(len(matrix))],
                ax=ax)
    ax.set_title("Matriz de Satisfacción", fontsize=12)
    ax.set_xlabel("Persona 'j' (Vecino)")
    ax.set_ylabel("Persona 'i' (Quien siente)")

def plot_interaction_graph(matrix, ax):
    G = nx.Graph()
    n = len(matrix)
    weights, edges_to_add = [], []
    for i in range(n):
        G.add_node(f"P{i}")
        for j in range(i + 1, n):
            weight = matrix[i, j] + matrix[j, i]
            weights.append(weight)
            edges_to_add.append((f"P{i}", f"P{j}", weight))
    if weights:
        min_w, max_w = min(weights), max(weights)
    else:
        min_w, max_w = 0, 1
    scaled_weights = [1 + 9 * (w - min_w) / (max_w - min_w + 1e-6) for w in weights]
    colors = ['#2ca02c' if w > 0 else '#d62728' for w in weights]
    for k, (u, v, weight) in enumerate(edges_to_add):
         G.add_edge(u, v, weight=scaled_weights[k], color=colors[k])
    edge_colors = list(nx.get_edge_attributes(G, 'color').values())
    edge_widths = list(nx.get_edge_attributes(G, 'weight').values())
    pos = nx.spring_layout(G, k=1, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=1400, font_size=10, font_weight='bold',
            width=edge_widths, edge_color=edge_colors,
            ax=ax)
    ax.set_title(" Interacciones", fontsize=12)
    ax.text(0.5, -0.08, "Verde=Buena Relación / Rojo=Mala", ha='center',
            transform=ax.transAxes, style='italic', fontsize=9)

def calculate_individual_satisfaction(person_id, arrangement, matrix):
    n = len(arrangement)
    idx = list(arrangement).index(person_id)
    p_left = arrangement[(idx - 1 + n) % n]
    p_right = arrangement[(idx + 1) % n]
    sat = (matrix[person_id, p_left] + matrix[p_left, person_id] +
           matrix[person_id, p_right] + matrix[p_right, person_id])
    return sat

def plot_score_evolution(history, ax):
    scores = [score for arr, score in history]
    ax.plot(scores, marker='o', linestyle='-', color='b')
    ax.set_title(" Satisfacción Total", fontsize=12)
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Satisfacción Total")
    if scores: # Evitar error si la historia está vacía
        ax.set_xticks(range(len(scores)))
    ax.grid(True, linestyle='--')

def plot_circular_map(arrangement, matrix, title_text, ax):
    n = len(arrangement)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x, y = np.cos(angles), np.sin(angles)
    satisfactions = [calculate_individual_satisfaction(p, arrangement, matrix) for p in arrangement]
    min_sat, max_sat = (min(satisfactions) if satisfactions else 0), (max(satisfactions) if satisfactions else 1)
    colors_norm = [(s - min_sat) / (max_sat - min_sat + 1e-6) for s in satisfactions]
    cmap = plt.get_cmap('RdYlGn')
    colors = [cmap(c) for c in colors_norm]
    ax.set_aspect('equal')
    ax.axis('off')
    for i in range(n):
        ax.plot([x[i], x[(i+1)%n]], [y[i], y[(i+1)%n]], color='gray', linestyle='--', zorder=1)
    ax.scatter(x, y, c=colors, s=1500, ec='black', zorder=2)
    for i in range(n):
        ax.text(x[i], y[i], f"P{arrangement[i]}", ha='center', va='center',
                fontsize=12, weight='bold', color='black')
    ax.set_title(title_text, fontsize=12)
    ax.text(0.5, -0.08, "Verde=Satisfecho / Rojo=Insatisfecho", ha='center',
            transform=ax.transAxes, style='italic', fontsize=9)

# Animación 
def animate_climbing_in_ax(ax_anim, history, matrix):
    n = len(history[0][0])
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x_coords, y_coords = np.cos(angles), np.sin(angles)
    history_arrs = [h[0] for h in history]
    history_scores = [h[1] for h in history]

    # eje principal (círculo)
    ax_anim.set_xlim(-1.5, 1.5); ax_anim.set_ylim(-1.5, 1.5)
    ax_anim.set_aspect('equal'); ax_anim.axis('off')
    # nodos iniciales (colores se actualizarán)
    nodescat = ax_anim.scatter(x_coords, y_coords, s=1200, c='gray', ec='black', zorder=3)
    labels = [ax_anim.text(x_coords[i], y_coords[i], "", ha='center', va='center', fontsize=12, weight='bold') for i in range(n)]
    for i in range(n):
        ax_anim.plot([x_coords[i], x_coords[(i+1)%n]], [y_coords[i], y_coords[(i+1)%n]], color='gray', linestyle='--', zorder=1)

    bbox = ax_anim.get_position()
    fig = ax_anim.figure
    
    if hasattr(ax_anim, '_inset_ax'):
        try:
            ax_anim._inset_ax.remove()
        except:
            pass 
            
    inset_ax = fig.add_axes([bbox.x0 + bbox.width*0.05, bbox.y0 + bbox.height*0.02, bbox.width*0.45, bbox.height*0.28])
    ax_anim._inset_ax = inset_ax 

    
    inset_ax.set_title("Score", fontsize=9)
    inset_ax.set_xlabel("Iter", fontsize=8)
    inset_ax.set_ylabel("Score", fontsize=8)
    inset_ax.grid(True, linestyle='--')
    inset_line, = inset_ax.plot([], [], marker='o', linestyle='-', color='b')


    all_indiv_sats = [calculate_individual_satisfaction(p, arr, matrix) for arr in history_arrs for p in arr]
    global_min_sat = min(all_indiv_sats) if all_indiv_sats else 0
    global_max_sat = max(all_indiv_sats) if all_indiv_sats else 1
    cmap = plt.get_cmap('RdYlGn')

    def update(frame):
        arrangement = history_arrs[frame]
        satisfactions = [calculate_individual_satisfaction(p, arrangement, matrix) for p in arrangement]
        colors_norm = [(s - global_min_sat) / (global_max_sat - global_min_sat + 1e-6) for s in satisfactions]
        colors = [cmap(c) for c in colors_norm]
        nodescat.set_color(colors)
        for i in range(n):
            labels[i].set_text(f"P{arrangement[i]}")
        inset_line.set_data(range(frame + 1), history_scores[:frame + 1])
        inset_ax.relim(); inset_ax.autoscale_view()
        ax_anim.set_title(f" Animación (iter {frame})", fontsize=12)
        return nodescat, *labels, inset_line

    ani = FuncAnimation(fig, update, frames=len(history_arrs), interval=900, repeat=False, blit=False)
    return ani

# --- 4. Ejecución Principal---

if __name__ == "__main__":

    # --- 1. Crear la GUI (Figura y Ejes) UNA SOLA VEZ ---
    fig_static, ax_static = plt.subplots(2, 3, figsize=(20, 12))
    # Dejar espacio para el título y el botón
    plt.subplots_adjust(wspace=0.3, hspace=0.35, top=0.92, bottom=0.1)
    fig_static.suptitle("Hill Climbing", fontsize=18, y=0.99)

    # --- 2. Definir la función del botón ---
    def on_reset_clicked(event):
        
        # --- A. Correr la simulación ---
        satisfaction_matrix = create_satisfaction_matrix(NUM_PEOPLE)
        final_arrangement, final_score, history = hill_climbing(satisfaction_matrix)

        print("--- Proceso de Optimización (Hill Climbing) ---")
        print(f"Disposición Inicial: {history[0][0]} (Score: {history[0][1]})")
        print(f"Disposición Final:   {final_arrangement} (Score: {final_score})")
        print(f"Mejora encontrada en {len(history) - 1} iteraciones.")
        
        # --- B. Limpiar los ejes ---
        for ax in ax_static.flat:
            ax.clear()

        # --- C. Generar las visualizaciones estáticas ---
        print("\nGenerando visualizaciones...")
        plot_heatmap(satisfaction_matrix, ax=ax_static[1, 2])
        plot_interaction_graph(satisfaction_matrix, ax=ax_static[0, 1])
        plot_score_evolution(history, ax=ax_static[0, 2])
        plot_circular_map(history[0][0], satisfaction_matrix, " Diposición Inicial", ax=ax_static[1, 0])
        plot_circular_map(final_arrangement, satisfaction_matrix, "Disposición Final", ax=ax_static[1, 1])

        # --- D. Repintar la animación (en tu layout) ---
        ax_for_animation = ax_static[0, 0]
        ax_for_animation.set_title("Progreso Hill Climbing)", fontsize=12)
        ax_for_animation.axis('off') # Re-aplicar 'axis off'
        
        ani = animate_climbing_in_ax(ax_for_animation, history, satisfaction_matrix)
        
        fig_static._animation_ref = ani

        # --- E. Guardar el GIF (sobrescribir el anterior) ---
        print("\nGuardando animación como 'dashboard_animadoV1.gif'...")
        ani.save("dashboard_animadoV1.gif", writer='pillow', fps=1.1)
        print("¡GIF guardado exitosamente!")

        # --- F. Redibujar el canvas ---
        fig_static.canvas.draw_idle()
        print("Dashboard actualizado.")

    # --- 3. Crear el Botón ---
    ax_button = plt.axes([0.4, 0.02, 0.2, 0.05]) # [izquierda, abajo, ancho, alto]
    btn_reset = Button(ax_button, 'Reiniciar Simulación')
    btn_reset.on_clicked(on_reset_clicked)
    # Guardar referencia al botón también
    fig_static._button_ref = btn_reset

    # --- 4. Carga Inicial ---
    print("Generando simulación inicial...")
    on_reset_clicked(None) # Llamar una vez para la carga inicial

    # --- 5. Mostrar la GUI ---
    plt.show()