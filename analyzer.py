from collections import Counter

def calcular_frequencias(jogos):
    frequencias = Counter()
    for jogo in jogos:
        for dezena in jogo['dezenas']:
            frequencias[dezena] += 1
    return frequencias

def contar_pares_impares(jogo):
    pares = sum(1 for n in jogo['dezenas'] if n % 2 == 0)
    impares = 15 - pares
    return pares, impares

def calcular_soma(jogo):
    return sum(jogo['dezenas'])

def contar_primos(jogo):
    primos_lotofacil = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    return sum(1 for n in jogo['dezenas'] if n in primos_lotofacil)

def contar_fibonacci(jogo):
    fibonacci_lotofacil = {1, 2, 3, 5, 8, 13, 21}
    return sum(1 for n in jogo['dezenas'] if n in fibonacci_lotofacil)

def analisar_jogos(jogos):
    if not jogos:
        print("Nenhum jogo para analisar.")
        return
        
    print(f"\n--- Analisando um total de {len(jogos)} jogos ---")
    
    # Frequência das dezenas
    freqs = calcular_frequencias(jogos)
    padrao = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    
    print("\n[ TOP 5 ] Dezenas Mais Sorteadas:")
    for dezena, contagem in padrao[:5]:
        print(f"  Dezena {dezena:02d} -> {contagem} vez(es)")
        
    print("\n[ BOTTOM 5 ] Dezenas Menos Sorteadas:")
    # Reverter o array bottom 5 para aparecer em ordem ascendente de sorteios, se preferir
    for dezena, contagem in reversed(padrao[-5:]):
        print(f"  Dezena {dezena:02d} -> {contagem} vez(es)")

    # Padrões do último jogo registrado
    ultimo_jogo = max(jogos, key=lambda j: j['concurso'])
    print(f"\n--- Análise do Último Jogo (Concurso {ultimo_jogo['concurso']}) ---")
    
    pares, impares = contar_pares_impares(ultimo_jogo)
    print(f"  Pares / Ímpares: {pares} pares, {impares} ímpares")
    print(f"  Soma das Dezenas: {calcular_soma(ultimo_jogo)}")
    print(f"  Números Primos: {contar_primos(ultimo_jogo)}")
    print(f"  Números de Fibonacci: {contar_fibonacci(ultimo_jogo)}")
    
    # Dica baseada na soma
    soma = calcular_soma(ultimo_jogo)
    print("  Curiosidade: A maioria das somas vencedoras fica entre 195 e 209.")
