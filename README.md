# 🍀 Lotofácil Analyzer Full Stack

Um sistema completo (Frontend Moderno + API Python) para análise heurística, estatística e geração inteligente de jogos da Lotofácil usando como base os últimos resultados do Brasil em tempo real.

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## ✨ Funcionalidades Principais
* **Dashboard Premium (`frontend/`)**: Interface fluida, moderna e limpa (aplique Padrão, Fixe dezenas ou Exclua).
* **Validação Ao Vivo**: A cada clique nas dezenas, o painel à direita é atualizado na hora para comparar seu jogo contra as estatísticas de ouro da Lotofácil (Ímpares, Pares, Repetidas, Moldura, Primos, Múltiplos de 3, Fibonacci e Soma 180-210).
* **Motor de Geração Heurística**: Diferente da 'Surpresinha', o botão "Gerar Jogo" testa recursivamente (até 50.000 iterações em milissegundos) milhares de combinações de jogos até achar 15 números que tirem "Nota 10" em todas as estatísticas matemáticas. Ele sempre tentará respeitar as dezenas que você marcou como "*Fixas*".
* **Sincronização Automática (`app.py`)**: O backend integrado em Flask se comunica com a API pública brasileira em tempo real para buscar os dados de "ontem" do sorteio (vital para o cálculo de jogos *Repetidos* do prêmio anterior).

## 🚀 Como instalar na sua máquina local

1. **Faça o clone do projeto na sua pasta:**
   ```bash
   git clone https://github.com/DanielOliveira-Gh/analyzer.git
   cd analyzer
   ```

2. **Instale as bibliotecas base (Python 3)**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Suba o Servidor (Backend):**
   ```bash
   python app.py
   ```

4. **Abra o sistema:**
   Com o servidor rodando, basta abrir [http://127.0.0.1:5000](http://127.0.0.1:5000) no seu navegador. A interface chamará o Python, que baixará os resultados e inicializará o sistema.

## ☁️ Como colocar online (Render.com)
1. Faça login via GitHub no **[Render.com](https://render.com/)**.
2. Clique em **New -> Web Service** e vincule este repositório `analyzer`.
3. Em *Build Command* preencha: `pip install -r requirements.txt`
4. Em *Start Command* preencha: `gunicorn app:app`
5. Aguarde o *deploy* (cerca de 2 minutinhos) e você ganhará um link público `.onrender.com` grátis para acessar pelo celular de todos seus amigos!

---
> Ferramenta auxiliar. **Atenção**: Este projeto serve exclusivamente para estudos matemáticos e de programação. Loterias são jogos de probabilidade sujeitos ao acaso. Dependendo da sorte do usuário. Não garante prêmios reais.
