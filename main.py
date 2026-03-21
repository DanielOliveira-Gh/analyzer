import os
from data_loader import carregar_resultados
from analyzer import analisar_jogos

def main():
    print("====================================")
    print("    ANALISADOR DE LOTOFÁCIL v1.0    ")
    print("====================================")
    
    # Resolve o caminho baseado na pasta atual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'resultados.csv')
    
    print(f"Procurando dados em: {csv_path}")
    
    jogos = carregar_resultados(csv_path)
    
    if jogos:
        analisar_jogos(jogos)
    else:
        print("\n[!] Não foi possível realizar a análise devido à falta de dados.")

if __name__ == "__main__":
    main()
