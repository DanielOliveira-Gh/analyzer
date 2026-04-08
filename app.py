from flask import Flask, send_from_directory, jsonify
import requests
import os

app = Flask(__name__, static_folder='frontend')

# API gratuita para sorteios da Lotofácil
# API gratuita para sorteios da Lotofácil
API_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/"

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/latest')
def get_latest():
    """
    Busca o último concurso a partir do nosso arquivo CSV local (resultados.csv).
    """
    # 1. Tentar ler do arquivo local CSV PRIMEIRO
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
        print(f"Erro ao ler CSV local: {e}")

    # Fallback extremo
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
