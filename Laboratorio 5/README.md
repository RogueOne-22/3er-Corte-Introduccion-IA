# 🎯 Colección de Algoritmos de Optimización y Búsqueda

Este repositorio contiene tres proyectos que implementan diferentes algoritmos clásicos de optimización y búsqueda, cada uno con visualizaciones interactivas y explicaciones detalladas.

---

## 📚 Índice de Proyectos

1. [💰 Sistema de Cambio de Monedas - Algoritmo Voraz](#1--sistema-de-cambio-de-monedas---algoritmo-voraz)
2. [🎮 Piedra, Papel o Tijera - Cadenas de Markov](#2--piedra-papel-o-tijera---cadenas-de-markov)
3. [🪑 Optimización de Asientos - Hill Climbing](#3--optimización-de-asientos---hill-climbing)

---

## 1. 💰 Sistema de Cambio de Monedas - Algoritmo Voraz

### 📖 Descripción
**Algoritmo voraz** aplicado al problema para dar cambio con monedas, minimizando la cantidad de monedas utilizadas.

### 🧠 Algoritmo: Voraz (Greedy)

**Principio:** Seleccionar siempre la opción localmente óptima (la moneda de mayor valor posible) esperando llegar a una solución globalmente óptima.

**Funcionamiento:**
```python
def calcular_cambio_voraz(monto):
    monedas = [50, 20, 10, 5, 1]  # Ordenadas de mayor a menor
    resultado = []
    
    for moneda in monedas:
        while monto >= moneda:
            monto -= moneda
            resultado.append(moneda)
    
    return resultado
```

**Complejidad:** O(n), donde n = número de denominaciones

### ✨ Características
- 📊 Panel informativo con seguimiento en tiempo real
- 🎲 Generación aleatoria de montos
- 🔄 Botón para generar nuevos casos

### 🎯 Ejemplo de Ejecución
```
Monto: 87
Proceso:
  50 → Restante: 37
  20 → Restante: 17
  10 → Restante: 7
  5  → Restante: 2
  1  → Restante: 1
  1  → Restante: 0
  
Total: 6 monedas
```
<img width="748" height="580" alt="Adversarial" src="https://github.com/user-attachments/assets/77b066a1-cd7c-4fbb-bba7-32e8fdc4a7f7" />

### ⚡ Ventajas del Algoritmo Voraz
- ✅ Muy rápido y eficiente
- ✅ Simple de implementar
- ✅ Óptimo para sistemas monetarios canónicos
- ✅ No requiere memoria de estados previos

### ⚠️ Limitaciones
- ❌ No siempre garantiza solución óptima en todos los sistemas de monedas
---

## 2. 🎮 Piedra, Papel o Tijera - Markov

### 📖 Descripción
Juego interactivo donde una IA utiliza **Cadenas de Markov** para predecir y contrarrestar los movimientos del jugador, aprendiendo de sus patrones de juego.

### 🧠 Algoritmo Markov

**Principio:** Un modelo estocástico que predice el siguiente estado basándose únicamente en los estados actuales, sin necesidad de conocer toda la historia.

**Funcionamiento:**
```python
class MarkovRPS:
    def __init__(self):
        self.chain = {}  # Matriz de transición
    
    def update(self, last_two, new_move):
        # Registra: Después de (jugada1, jugada2) → jugada3
        if last_two not in self.chain:
            self.chain[last_two] = {}
        self.chain[last_two][new_move] += 1
    
    def predict(self, last_two):
        # Retorna la jugada más frecuente después del patrón
        return max(self.chain[last_two], key=self.chain[last_two].get)
```

### 🎲 Propiedad Markoviana
> "El futuro depende solo del presente, no del pasado completo"

```
Estado actual: (Piedra, Papel)
Historial de transiciones:
  (Piedra, Papel) → Tijera: 5 veces
  (Piedra, Papel) → Piedra: 2 veces
  (Piedra, Papel) → Papel: 1 vez

Predicción: Tijera (la más frecuente)
Contraataque IA: Piedra (vence a Tijera)
```

### ✨ Características
- 📊 Estadísticas en tiempo real (Victorias/Derrotas/Empates)
- 🧠 IA que aprende continuamente
- 🔄 Reinicio completo (borra memoria de IA)

  <img width="475" height="572" alt="juego" src="https://github.com/user-attachments/assets/c0321067-be1a-4245-8028-6de5a7979594" />


### 📈 Rendimiento Esperado
| Tipo de Jugador | Victoria IA | Empate | Victoria Jugador |
|-----------------|-------------|--------|------------------|
| Con Patrones    | 60-70%      | 10-15% | 15-30%          |
| Aleatorio       | 33%         | 33%    | 33%             |

### 🎯 Cómo Vencer a la IA
1. **Juega completamente al azar** (usa dado/moneda)
2. **Cambia constantemente** tus patrones
3. **Crea patrones falsos** y luego rómpelos
4. **Meta-juego**: Predice qué predecirá la IA

---

## 3. 🪑 Optimización de Asientos - Hill Climbing

### 📖 Descripción
Sistema que optimiza la disposición de personas alrededor de una mesa circular para **maximizar la satisfacción total**, considerando las preferencias interpersonales de cada persona.

### 🧠 Algoritmo: Hill Climbing

**Principio:** Algoritmo de búsqueda local que explora el espacio de soluciones moviéndose siempre hacia vecinos con mejor evaluación (mayor satisfacción).

**Funcionamiento:**
```python
def hill_climbing(matrix):
    current = generar_solucion_inicial()
    current_score = evaluar(current)
    
    while True:
        vecinos = generar_vecinos(current)
        mejor_vecino = max(vecinos, key=evaluar)
        mejor_score = evaluar(mejor_vecino)
        
        if mejor_score <= current_score:
            break  # Máximo local alcanzado
        
        current = mejor_vecino
        current_score = mejor_score
    
    return current, current_score
```

**Complejidad:** O(n² × k), donde n = número de personas, k = iteraciones

### 🔑 Conceptos Clave

#### Función Objetivo
```python
def calculate_total_satisfaction(arrangement, matrix):
    total = 0
    for i in range(n):
        persona1 = arrangement[i]
        persona2 = arrangement[(i + 1) % n]  # Circular
        # Satisfacción mutua
        total += matrix[persona1, persona2] + matrix[persona2, persona1]
    return total
```

#### Generación de Vecinos
```python
def get_neighbors(arrangement):
    neighbors = []
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = arrangement.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Swap
            neighbors.append(neighbor)
    return neighbors
```

#### Mejora: Aceptación de Movimientos 
Para escapar de máximos locales:
```python
if mejor_score > current_score:
    current = mejor_vecino  # Siempre acepta mejoras
elif current_score - mejor_score <= threshold and random() < 0.25:
    current = mejor_vecino  # 25% chance de aceptar empeoramiento leve
```

### ✨ Características
- 🎨 Dashboard interactivo con 6 visualizaciones
- 📊 **Heatmap**: Matriz de satisfacción entre personas
- 🕸️ **Grafo de Interacciones**: Relaciones visualizadas (verde=positiva, rojo=negativa)
- 📈 **Evolución del Score**: Progreso del algoritmo
- 🎡 **Mapa Circular**: Disposición inicial y final (color por satisfacción individual)
- 🎬 **Animación**: Progreso paso a paso con gráfica de score incrustada
- 🔄 Botón para generar nuevas simulaciones
- 💾 Exportación automática a GIF

### 🎯 Matriz de Satisfacción
```python
# Valores positivos: buena relación
# Valores negativos: mala relación (conflictos)
# Diagonal: 0 (uno mismo)

Ejemplo:
      P0  P1  P2  P3
P0 [  0   8  -5   3 ]
P1 [  7   0   2  -3 ]
P2 [ -4   1   0   9 ]
P3 [  5  -2   8   0 ]
```
<img width="1685" height="935" alt="Hill Climbing" src="https://github.com/user-attachments/assets/d1cc023b-9fd2-4292-819f-e9a640466e9d" />

### 📊 Visualizaciones Incluidas

1. **Animación Hill Climbing** (con gráfico de score incrustado)
2. **Grafo de Interacciones** (NetworkX)
3. **Evolución del Score** (line plot)
4. **Disposición Inicial** (circular map)
5. **Disposición Final** (circular map)
6. **Heatmap de Satisfacción** (matriz de preferencias)

### 🎬 Proceso Visual
```
Disposición Inicial: [P0, P1, P2, P3, P4, P5, P6, P7]
Score inicial: -12

Iteración 1: Intercambio P0 ↔ P5
Score: 8

Iteración 2: Intercambio P2 ↔ P7
Score: 23

...

Disposición Final: [P5, P3, P1, P7, P4, P2, P6, P0]
Score final: 45
Mejora: +57 puntos en 8 iteraciones
```

### ⚡ Ventajas de Hill Climbing
- ✅ Simple de implementar
- ✅ Encuentra soluciones buenas rápidamente
- ✅ No requiere mucha memoria
- ✅ Funciona bien en espacios continuos

### ⚠️ Limitaciones
- ❌ Se queda en máximos locales
- ❌ No garantiza óptimo global
- ❌ Sensible a la solución inicial
- ❌ No explora todo el espacio de búsqueda

---

## 🔬 Comparación de Algoritmos

| Algoritmo | Tipo | Optimalidad | Complejidad | Memoria | Uso Principal |
|-----------|------|-------------|-------------|---------|---------------|
| **Voraz** | Constructivo | Local óptima* | O(n) | O(1) | Problemas con elección local clara |
| **Markov** | Predictivo | Probabilística | O(1) | O(k²) | Predicción de secuencias |
| **Hill Climbing** | Búsqueda Local | Máximo local | O(n²k) | O(n) | Optimización con vecindad definida |

---

## 📊 Conceptos Clave Compartidos

### 1. Búsqueda Heurística
Todos los algoritmos utilizan **heurísticas** (reglas prácticas) en lugar de búsqueda exhaustiva:
- **Voraz**: "Siempre elige la moneda más grande"
- **Markov**: "Predice basándote en lo más frecuente"
- **Hill Climbing**: "Muévete hacia el vecino mejor evaluado"

### 2. Trade-off: Velocidad vs Optimalidad
```
Voraz:          ████████████████ Rápido    ████░░░░░░░░ Óptimo
Markov:         ████████████████ Rápido    ████████░░░░ Óptimo
Hill Climbing:  ████████░░░░░░░░ Rápido    ████████████ Óptimo
```

### 3. Aplicaciones Reales

#### Algoritmo Voraz
- 💵 Sistemas de pago automático
- 📦 Algoritmo de Huffman (compresión)
- 🚗 Algoritmo de Dijkstra (caminos mínimos)
- 🌳 Árboles de expansión mínima (Kruskal, Prim)

#### Cadenas de Markov
- 📱 Predicción de texto (teclados)
- 🧬 Análisis de secuencias de ADN
- 📈 Modelos financieros (predicción de acciones)
- 🎵 Generación de música
- 🌤️ Predicción del clima

#### Hill Climbing
- 🤖 Entrenamiento de redes neuronales
- 🎮 IA en videojuegos
- 📍 Problemas de ruteo (TSP)
- ⚙️ Optimización de parámetros
- 🏭 Scheduling de producción

---

## 📚 Recursos Educativos

### Algoritmo Voraz
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - Capítulo 16
- [Greedy Algorithms - GeeksforGeeks](https://www.geeksforgeeks.org/greedy-algorithms/)

### Cadenas de Markov
- [Introduction to Probability Models - Sheldon Ross](https://www.elsevier.com/books/introduction-to-probability-models/ross/978-0-12-814346-9)
- [Markov Chains - Brilliant.org](https://brilliant.org/wiki/markov-chains/)

### Hill Climbing
- [Artificial Intelligence: A Modern Approach (Russell & Norvig)](http://aima.cs.berkeley.edu/) - Capítulo 4
- [Hill Climbing Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Hill_climbing)

---

## 🎯 Conclusión

1. **Optimización Greedy** (Voraz) - Decisiones locales óptimas
2. **Predicción Probabilística** (Markov) - Modelado estocástico
3. **Búsqueda Local** (Hill Climbing) - Mejora iterativa

---

## 📄 Licencia

#### Este código es de uso educativo y puede ser modificado libremente.
---
## ✨Autor
### Paula S

