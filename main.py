from arbol import Nodo

# ==========================================
# 1. BÚSQUEDA EN AMPLITUD (BFS)
# ==========================================
def buscar_solucion_BFS(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)
    
    while (not solucionado) and len(nodos_frontera) != 0:
        # Cola FIFO: se extrae el primer elemento
        nodo = nodos_frontera.pop(0) 
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            # Expandir nodos hijos
            dato_nodo = nodo.get_datos()
            
            # Operador Izquierdo
            hijo_izq = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izquierdo = Nodo(hijo_izq)
            
            # Operador Central
            hijo_cen = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_central = Nodo(hijo_cen)
            
            # Operador Derecho
            hijo_der = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_derecho = Nodo(hijo_der)
            
            # Asignamos los hijos al nodo actual
            nodo.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])
            
            for nodo_hijo in nodo.get_hijos():
                if not nodo_hijo.en_lista(nodos_visitados) and not nodo_hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(nodo_hijo)
    return None

# ==========================================
# 2. BÚSQUEDA EN PROFUNDIDAD RECURSIVA (DFS)
# ==========================================
def buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        # Expandir los nodos sucesores (hijos)
        dato_nodo = nodo_inicial.get_datos()
        
        # Hijo izquierdo
        hijo_izq = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izquierdo = Nodo(hijo_izq)
        
        # Hijo central
        hijo_cen = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_central = Nodo(hijo_cen)
        
        # Hijo derecho
        hijo_der = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_derecho = Nodo(hijo_der)
        
        nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])
        
        for nodo_hijo in nodo_inicial.get_hijos():
            if not nodo_hijo.get_datos() in visitados:
                # Llamada recursiva
                sol = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
                if sol != None:
                    return sol
        return None

# ==========================================
# 3. BÚSQUEDA DE COSTO UNIFORME
# ==========================================
def buscar_solucion_costo_uniforme(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = []
    
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0) # Costo inicial 0
    nodos_frontera.append(nodo_inicial)
    
    while len(nodos_frontera) != 0:
        # Ordenar la lista de nodos_frontera según el costo
        nodos_frontera.sort(key=lambda x: x.get_costo())
        
        # Extraer el nodo con menor costo
        nodo_actual = nodos_frontera.pop(0)
        nodos_visitados.append(nodo_actual)
        
        if nodo_actual.get_datos() == solucion:
            return nodo_actual
        else:
            dato_nodo = nodo_actual.get_datos()
            costo_actual = nodo_actual.get_costo()
            
            # Operador Izquierdo (costo + 1)
            h_izq = Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]])
            h_izq.set_costo(costo_actual + 1)
            
            # Operador Central (costo + 1)
            h_cen = Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]])
            h_cen.set_costo(costo_actual + 1)
            
            # Operador Derecho (costo + 1)
            h_der = Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
            h_der.set_costo(costo_actual + 1)
            
            nodo_actual.set_hijos([h_izq, h_cen, h_der])
            
            for nodo_hijo in nodo_actual.get_hijos():
                if not nodo_hijo.en_lista(nodos_visitados):
                    if not nodo_hijo.en_lista(nodos_frontera):
                        nodos_frontera.append(nodo_hijo)
    return None

# ==========================================
# BLOQUE DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    
    print("--- BÚSQUEDA EN AMPLITUD (BFS) ---")
    nodo_solucion_bfs = buscar_solucion_BFS(estado_inicial, solucion)
    if nodo_solucion_bfs:
        resultado = []
        nodo = nodo_solucion_bfs
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
        print(f"Resultado: {resultado}\n")

    print("--- BÚSQUEDA EN PROFUNDIDAD RECURSIVA (DFS) ---")
    nodo_ini_dfs = Nodo(estado_inicial)
    visitados = []
    nodo_solucion_dfs = buscar_solucion_DFS_rec(nodo_ini_dfs, solucion, visitados)
    if nodo_solucion_dfs:
        resultado = []
        nodo = nodo_solucion_dfs
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
        print(f"Resultado: {resultado}\n")
        
    print("--- BÚSQUEDA DE COSTO UNIFORME ---")
    nodo_solucion_cu = buscar_solucion_costo_uniforme(estado_inicial, solucion)
    if nodo_solucion_cu:
        resultado = []
        costo_final = nodo_solucion_cu.get_costo()
        nodo = nodo_solucion_cu
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
        print(f"Resultado: {resultado}")
        print(f"Costo acumulado: {costo_final}\n")