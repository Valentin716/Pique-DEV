from flask import Flask, render_template, jsonify, request
from arbol import Nodo 

app = Flask(__name__)

GRAFO = {
    'Jiloyork': [('CDMX', 100), ('Toluca', 60)],
    'CDMX': [('Monterrey', 851), ('Puebla', 130)],
    'Toluca': [('Monterrey', 900), ('Guadalajara', 450)],
    'Puebla': [('Monterrey', 950)],
    'Guadalajara': [('Monterrey', 670)],
    'Monterrey': []
}

# Diccionario para guardar el estado de las 3 búsquedas
procesos = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar_todas')
def iniciar_todas():
    # Inicializamos los 3 algoritmos a la vez
    for alg in ['bfs', 'dfs', 'ucs']:
        nodo_ini = Nodo('Jiloyork')
        nodo_ini.set_costo(0)
        procesos[alg] = {
            'frontera': [nodo_ini],
            'visitados': [],
            'terminado': False,
            'actual': 'Jiloyork',
            'costo': 0
        }
    return jsonify({"status": "ready"})

@app.route('/paso_comparativo')
def paso_comparativo():
    alg = request.args.get('alg', 'bfs')
    p = procesos.get(alg)

    if not p or not p['frontera'] or p['terminado']:
        return jsonify({"status": "finalizado"})

    # Lógica de extracción según algoritmo
    if alg == 'bfs': nodo_actual = p['frontera'].pop(0)
    elif alg == 'dfs': nodo_actual = p['frontera'].pop()
    else: # ucs
        p['frontera'].sort(key=lambda x: x.get_costo())
        nodo_actual = p['frontera'].pop(0)

    ciudad = nodo_actual.get_datos()
    p['visitados'].append(ciudad)
    p['actual'] = ciudad
    p['costo'] = nodo_actual.get_costo()

    if ciudad == 'Monterrey':
        p['terminado'] = True
        return jsonify({"status": "encontrado", "ciudad": ciudad, "costo": p['costo']})

    for vecino, costo in GRAFO.get(ciudad, []):
        hijo = Nodo(vecino)
        hijo.set_padre(nodo_actual)
        hijo.set_costo(p['costo'] + costo)
        if hijo.get_datos() not in p['visitados']:
            p['frontera'].append(hijo)

    return jsonify({"status": "buscando", "ciudad": ciudad, "costo": p['costo']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)