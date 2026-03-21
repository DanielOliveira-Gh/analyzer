from flask import Flask, send_from_directory, jsonify
import requests
import os

app = Flask(__name__, static_folder='frontend')

# API gratuita para sorteios da Lotofácil
API_URL = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest"

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/latest')
def get_latest():
    """
    Busca o último concurso em uma API real e repassa ao frontend.
    Caso a API falhe, faz o fallback para o nosso CSV local.
    """
    try:
        # Acesso em tempo real
        resp = requests.get(API_URL, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # As dezenas costumam vir como strings ["01", "04"...]
            dezenas_int = [int(d) for d in data.get('dezenas', [])]
            return jsonify({
                "source": "api_externa",
                "concurso": data.get("concurso"),
                "dezenas": dezenas_int
            })
    except Exception as e:
        print(f"Aviso - Erro na API real: {e}")
        
    # BACKUP: Tentar ler do arquivo local CSV
    try:
        from data_loader import carregar_resultados
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, 'resultados.csv')
        jogos = carregar_resultados(csv_path)
        if jogos:
             ultimo = max(jogos, key=lambda j: j['concurso'])
             return jsonify({
                 "source": "csv_local",
                 "concurso": ultimo['concurso'],
                 "dezenas": ultimo['dezenas']
             })
    except Exception as e:
        print(f"Erro de fallback local: {e}")

    # Fallback extremo para nunca quebrar a UI
    return jsonify({
        "source": "hardcode",
        "concurso": 0,
        "dezenas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    })

if __name__ == '__main__':
    print("====================================")
    print("🚀 Servidor Python Lotofácil ON!")
    print("====================================")
    print("Acesse no navegador: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
