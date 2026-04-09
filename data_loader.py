import csv
import urllib.request
import json
import os

def update_resultados_csv(filepath, num_resultados=3):
    """
    Busca os últimos concursos na API da Caixa e atualiza o CSV.
    """
    try:
        url_latest = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/"
        req = urllib.request.Request(url_latest, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            ultimo_concurso_api = data['numero']
        
        concursos_existentes = set()
        if os.path.exists(filepath):
            with open(filepath, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Concurso'):
                        concursos_existentes.add(int(row['Concurso']))
        else:
            with open(filepath, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Concurso'] + [f'Bola{i}' for i in range(1, 16)])

        concursos_para_buscar = []
        for i in range(num_resultados):
            concurso = ultimo_concurso_api - i
            if concurso > 0 and concurso not in concursos_existentes:
                concursos_para_buscar.append(concurso)
        
        concursos_para_buscar.sort()
        
        if not concursos_para_buscar:
            return

        with open(filepath, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for concurso in concursos_para_buscar:
                url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/{concurso}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read())
                    dezenas = [int(d) for d in data['listaDezenas']]
                    dezenas.sort()
                    writer.writerow([concurso] + dezenas)
                
    except Exception as e:
        print(f"Erro ao tentar atualizar o CSV: {e}")

def carregar_resultados(filepath):
    """
    Lê o arquivo CSV e retorna uma lista de dicionários com os jogos.
    O formato esperado do CSV é: Concurso,Bola1,Bola2,...,Bola15
    """
    jogos = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    concurso = int(row['Concurso'])
                    bolas = [int(row[f'Bola{i}']) for i in range(1, 16)]
                    jogos.append({
                        'concurso': concurso,
                        'dezenas': bolas
                    })
                except (ValueError, KeyError) as e:
                    print(f"Erro ao processar linha: {e}")
        return jogos
    except FileNotFoundError:
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return []
    except Exception as e:
        print(f"Erro inesperado ao carregar arquivo: {e}")
        return []
