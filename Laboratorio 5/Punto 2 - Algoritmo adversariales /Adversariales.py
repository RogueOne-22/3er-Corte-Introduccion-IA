import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import math
from matplotlib.widgets import Button

# --- 1. El Algoritmo Voraz ---
def calcular_cambio_voraz(monto_a_devolver):
    monedas = [50, 20, 10, 5, 1]
    cambio_entregado = []
    monto_restante = monto_a_devolver
    
    for moneda in monedas:
        while monto_restante >= moneda:
            monto_restante -= moneda
            cambio_entregado.append(moneda)
            
    return cambio_entregado, monto_a_devolver

# --- 2. Animación ---
def run_animation_on_axis(ax, historial_monedas, monto_total):
    
    # --- A. Limpiar y re-configurar el eje ---
    ax.clear() # Limpia 
    
    num_monedas = len(historial_monedas)
    FILAS = math.ceil(num_monedas / 10) + 1
    ax.set_aspect('equal')
    ax.set_xlim(-1, 10)
    ax.set_ylim(-FILAS, 2)
    ax.axis('off')
    
    # Guardar la figura para referencias
    fig = ax.figure

    # --- B. Dibujar los textos estáticos ---
    txt_titulo = ax.text(4.5, 1.5, f"Monto a devolver: {monto_total}", 
                         ha='center', fontsize=22, weight='bold')
    
    txt_estado = ax.text(4.5, 0.5, f"Entregando cambio...", 
                         ha='center', fontsize=18, color='teal', weight='bold')
    
    txt_restante = ax.text(4.5, -0.2, f"Falta por devolver: {monto_total}", 
                           ha='center', fontsize=18, color='purple', weight='bold')

    moneda_props = {
        50: {'color': "#2FFF00", 'radius': 0.45}, # Dorado
        20: {'color': "#C8AA24", 'radius': 0.4},  # Plata
        10: {'color': '#C0C0C0', 'radius': 0.35}, # Plata
        5:  {'color': '#B87333', 'radius': 0.3},  # Bronce
        1:  {'color': "#7333B852", 'radius': 0.25}  # Bronce
    }
    
    suma_acumulada = [sum(historial_monedas[:i+1]) for i in range(num_monedas)]

    # --- C. Definir la función de actualización de la animación ---
    def update(frame):
        moneda_valor = historial_monedas[frame]
        props = moneda_props[moneda_valor]
        
        MONEDAS_POR_FILA = 10
        fila = frame // MONEDAS_POR_FILA
        col = frame % MONEDAS_POR_FILA
        
        x = col
        y = -1.5 - (fila * 1.2)
        
        moneda_circulo = Circle((x, y), 
                                radius=props['radius'], 
                                color=props['color'], 
                                ec='black', 
                                zorder=2)
        ax.add_patch(moneda_circulo)
        
        ax.text(x, y, f"{moneda_valor}", 
                ha='center', va='center', 
                fontsize=10, weight='bold', zorder=3)
        
        monto_entregado = suma_acumulada[frame]
        monto_restante = monto_total - monto_entregado
        
        txt_estado.set_text(f"Entregando: {moneda_valor}")
        txt_restante.set_text(f"Falta por devolver: {monto_restante}")
        
        if frame == num_monedas - 1:
            txt_estado.set_text("¡Cambio Entregado!")
            txt_estado.set_color('green')
            txt_restante.set_text("Falta por devolver: 0")
            txt_restante.set_color('green')
            
        return [moneda_circulo]

    # --- D. Crear y devolver el objeto de animación ---
    ani = FuncAnimation(fig, update, 
                        frames=len(historial_monedas),
                        interval=400, 
                        repeat=False,
                        blit=False) 
    
    return ani

# --- 3. Ejecución Principal ---
if __name__ == "__main__":
    
    # 1. Crear la figura 
    fig, ax = plt.subplots(figsize=(10, 7))
    # Ajustar la figura para dejar espacio al botón
    plt.subplots_adjust(bottom=0.1)

    # 2. Definir la función de reinicio
    def on_reset_clicked(event):
        print("Botón presionado. Generando nuevo cambio...")
        
        # a. Generar nuevos datos
        monto_aleatorio = random.randint(40, 240)
        historial, total = calcular_cambio_voraz(monto_aleatorio)
        
        print(f"Monto Total a Devolver: {total}")
        print(f"Monedas usadas ({len(historial)} en total):")
        print(historial)
        
        # b. Re-ejecutar la animación en el eje existente
        animacion = run_animation_on_axis(ax, historial, total)
        
        fig._animation_ref = animacion
        
        # d. Refrescar la ventana
        fig.canvas.draw_idle()

    # 3. Crear el eje del botón
    ax_button = plt.axes([0.4, 0.02, 0.2, 0.05]) # [izquierda, abajo, ancho, alto]
    
    # 4. Crear el objeto botón y conectarlo
    btn_reset = Button(ax_button, 'Generar Nuevo Cambio')
    btn_reset.on_clicked(on_reset_clicked)
    # Guardar referencia al botón 
    fig._button_ref = btn_reset

    # 5. Carga inicial
    print("Generando animación inicial...")
    on_reset_clicked(None)
    
    # 6. Mostrar la GUI
    print("Presiona el botón para reiniciar.")
    plt.show()