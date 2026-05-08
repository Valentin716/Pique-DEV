from flask import Flask, render_template, jsonify, request
from arbol import Nodo # Asegúrate de que arbol.py soporte datos tipo string

app = Flask(__name__)

# --- MAPA DE CIUDADES (GRAFO) ---
# Formato: 'Ciudad': [('Destino', Costo), ...]
GRAFO = {
    'Jiloyork': [('CDMX', 100), ('Toluca', 60)],
    'CDMX': [('Monterrey', 851), ('Puebla', 130)],
    'Toluca': [('Monterrey', 900), ('Guadalajara', 450)],
    'Puebla': [('Monterrey', 950)],
    'Guadalajara': [('Monterrey', 670)],
    'Monterrey': []
}

proceso = {
    'frontera': [],
    'visitados': [],
    'objetivo': 'Monterrey',
    'algoritmo': 'bfs'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar')
def iniciar():
    alg = request.args.get('algoritmo', 'bfs')
    proceso['algoritmo'] = alg
    proceso['visitados'] = []
    
    nodo_inicial = Nodo('Jiloyork')
    nodo_inicial.set_costo(0)
    proceso['frontera'] = [nodo_inicial]
    return jsonify({"status": "ready"})

@app.route('/paso')
def paso():
    if not proceso['frontera']:
        return jsonify({"status": "finalizado"})

    # Selección de lógica según algoritmo
    if proceso['algoritmo'] == 'bfs':
        nodo_actual = proceso['frontera'].pop(0) # FIFO
    elif proceso['algoritmo'] == 'dfs':
        nodo_actual = proceso['frontera'].pop()    # LIFO
    elif proceso['algoritmo'] == 'ucs':
        proceso['frontera'].sort(key=lambda x: x.get_costo())
        nodo_actual = proceso['frontera'].pop(0) # Menor costo

    ciudad_actual = nodo_actual.get_datos()
    proceso['visitados'].append(ciudad_actual)

    if ciudad_actual == proceso['objetivo']:
        return jsonify({
            "status": "encontrado", 
            "actual": ciudad_actual, 
            "costo_total": nodo_actual.get_costo()
        })

    # Expandir vecinos desde el Grafo
    for vecino, costo_tramo in GRAFO.get(ciudad_actual, []):
        hijo = Nodo(vecino)
        hijo.set_padre(nodo_actual)
        hijo.set_costo(nodo_actual.get_costo() + costo_tramo)
        
        if hijo.get_datos() not in proceso['visitados']:
            if not hijo.en_lista(proceso['frontera']):
                proceso['frontera'].append(hijo)

    return jsonify({
        "status": "buscando",
        "actual": ciudad_actual,
        "costo_acumulado": nodo_actual.get_costo(),
        "pendientes": [n.get_datos() for n in proceso['frontera']]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)