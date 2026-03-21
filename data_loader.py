import csv

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
