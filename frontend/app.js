// Constantes da Lotofácil
const MOLDURA = [1,2,3,4,5,6,10,11,15,16,20,21,22,23,24,25];
const PRIMOS = [2,3,5,7,11,13,17,19,23];
const MULTIPLOS_3 = [3,6,9,12,15,18,21,24];
const FIBONACCI = [1,2,3,5,8,13,21];

// O Jogo anterior será carregado em tempo real do backend via Fetch API
let ULTIMO_JOGO = [];

// Estado da aplicação
let currentMode = 'padrao'; // padrao, fixar, excluir
let numbersState = {}; // { 1: 'padrao', 2: 'fixar', 3: 'none' }

// Elementos
const boardEl = document.getElementById('board');
const modeBtns = document.querySelectorAll('.mode-btn');
const tbody = document.getElementById('params-tbody');
const toggleParams = document.getElementById('toggle-params');
const paramsPanel = document.getElementById('params-panel');

// Inicializa estado e renderiza
async function init() {
    // 1. Fetch Real Time Data
    try {
        const resp = await fetch('/api/latest');
        const data = await resp.json();
        if (data && data.dezenas) {
            ULTIMO_JOGO = data.dezenas;
            console.log(`Opa! Último concurso (${data.concurso}) carregado. Fonte: ${data.source}`);
            
            // Popula na UI
            const container = document.getElementById('latest-draw-container');
            const title = document.getElementById('latest-draw-title');
            const numbersContainer = document.getElementById('latest-draw-numbers');
            
            if (container && title && numbersContainer) {
                container.style.display = 'flex';
                title.innerText = `Último Concurso (${data.concurso})`;
                
                numbersContainer.innerHTML = '';
                const sorted = [...ULTIMO_JOGO].sort((a, b) => a - b);
                sorted.forEach(num => {
                    const span = document.createElement('span');
                    span.className = 'latest-draw-num';
                    span.innerText = num.toString().padStart(2, '0');
                    numbersContainer.appendChild(span);
                });
            }
        }
    } catch(err) {
        console.warn('Aviso: Backend inativo ou erro de rede. Usando jogo de segurança.');
        ULTIMO_JOGO = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]; 
    }

    document.getElementById('btn-generate').addEventListener('click', generateGame);
    
    const btnClearAll = document.getElementById('btn-clear-all');
    if (btnClearAll) {
        btnClearAll.addEventListener('click', clearAll);
    }

    // 2. Render Board
    for (let i = 1; i <= 25; i++) {
        numbersState[i] = 'none';
        
        const btn = document.createElement('button');
        btn.className = 'number-btn';
        btn.innerText = i.toString().padStart(2, '0');
        btn.onclick = () => toggleNumber(i);
        
        // Indicadores (Opcional, inspirado na imagem: M=Moldura, P=Primo, F=Fib)
        if (MOLDURA.includes(i)) {
            let ind = document.createElement('span');
            ind.className = 'indicator ind-bl'; ind.innerText = 'M';
            btn.appendChild(ind);
        }
        if (PRIMOS.includes(i)) {
            let ind = document.createElement('span');
            ind.className = 'indicator ind-tr'; ind.innerText = 'P';
            btn.appendChild(ind);
        }
        if (FIBONACCI.includes(i)) {
            let ind = document.createElement('span');
            ind.className = 'indicator ind-br'; ind.innerText = 'F';
            btn.appendChild(ind);
        }

        btn.id = `num-${i}`;
        boardEl.appendChild(btn);
    }

    updateUI();
}

// Troca mode
modeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        modeBtns.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentMode = e.target.dataset.mode;
    });
});

// Toggle painel de parametros
toggleParams.addEventListener('change', (e) => {
    paramsPanel.style.display = e.target.checked ? 'none' : 'block';
});

// Botão Lixeira
window.clearMode = function(modeToRemove) {
    for(let i=1; i<=25; i++){
        if(numbersState[i] === modeToRemove) {
            numbersState[i] = 'none';
        }
    }
    updateUI();
}

// Botão Limpar Tudo
window.clearAll = function() {
    for(let i=1; i<=25; i++) {
        numbersState[i] = 'none';
    }
    updateUI();
}

// Clique em uma dezena
function toggleNumber(n) {
    if (numbersState[n] === currentMode) {
        numbersState[n] = 'none'; // Desmarca se já está no modo atual
    } else {
        numbersState[n] = currentMode; // Marca com o modo atual
    }
    updateUI();
}

function updateUI() {
    let countPadrao = 0;
    let countFixar = 0;
    let countExcluir = 0;
    
    let activeNumbers = [];

    // Atualiza botões
    for (let i = 1; i <= 25; i++) {
        const btn = document.getElementById(`num-${i}`);
        btn.className = 'number-btn'; // reseta classes
        
        if (numbersState[i] === 'padrao') {
            btn.classList.add('state-padrao');
            countPadrao++;
            activeNumbers.push(i);
        } else if (numbersState[i] === 'fixar') {
            btn.classList.add('state-fixar');
            countFixar++;
            activeNumbers.push(i);
        } else if (numbersState[i] === 'excluir') {
            btn.classList.add('state-excluir');
            countExcluir++;
        }
    }

    // Atualiza contadores
    document.getElementById('count-padrao').innerText = countPadrao;
    document.getElementById('count-fixar').innerText = countFixar;
    document.getElementById('count-excluir').innerText = countExcluir;

    // Atualiza Tabela de Parâmetros
    updateParamsTable(activeNumbers);
}

function updateParamsTable(activeNumbers) {
    let impares = 0, pares = 0, repetidas = 0;
    let moldura = 0, primos = 0, multiplos = 0, fibo = 0, soma = 0;

    activeNumbers.forEach(n => {
        if (n % 2 === 0) pares++; else impares++;
        if (ULTIMO_JOGO.includes(n)) repetidas++;
        if (MOLDURA.includes(n)) moldura++;
        if (PRIMOS.includes(n)) primos++;
        if (MULTIPLOS_3.includes(n)) multiplos++;
        if (FIBONACCI.includes(n)) fibo++;
        soma += n;
    });

    const isFull = activeNumbers.length === 15;

    const params = [
        { label: 'Ímpares', val: impares, ideal: impares >= 7 && impares <= 8 },
        { label: 'Pares', val: pares, ideal: pares >= 7 && pares <= 8 },
        { label: 'Repetidas', val: repetidas, ideal: repetidas >= 8 && repetidas <= 10 },
        { label: 'Moldura', val: moldura, ideal: moldura >= 9 && moldura <= 10 },
        { label: 'Primos', val: primos, ideal: primos >= 5 && primos <= 6 },
        { label: 'Múltiplos de 3', val: multiplos, ideal: multiplos >= 4 && multiplos <= 5 },
        { label: 'Fibonaccis', val: fibo, ideal: fibo >= 4 && fibo <= 5 },
        { label: 'Soma', val: soma, ideal: soma >= 195 && soma <= 209 }
    ];

    tbody.innerHTML = '';
    params.forEach(p => {
        const tr = document.createElement('tr');
        
        let statusHtml = `<span class="status-badge">Aguardando</span>`;
        if (activeNumbers.length > 0) {
            if (isFull && p.ideal) {
                statusHtml = `<span class="status-badge status-ideal">Ideal</span>`;
            } else if (isFull && !p.ideal) {
                statusHtml = `<span class="status-badge status-atencao">Atenção</span>`;
            } else {
                 statusHtml = `<span class="status-badge">Calculando...</span>`;
            }
        }

        tr.innerHTML = `
            <td>${p.label}</td>
            <td>${p.val}</td>
            <td>${statusHtml}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Lógica de Geração Heurística
function generateGame() {
    let fixas = [];
    let excluidas = [];
    
    // Prepara fixas e excluidas
    for (let i = 1; i <= 25; i++) {
        if (numbersState[i] === 'fixar') fixas.push(i);
        if (numbersState[i] === 'excluir') excluidas.push(i);
    }
    
    if (fixas.length > 15) {
        alert("Você selecionou mais de 15 dezenas fixas!");
        return;
    }
    
    let pool = [];
    for (let i = 1; i <= 25; i++) {
        if (!fixas.includes(i) && !excluidas.includes(i)) {
            pool.push(i);
        }
    }
    
    const maxAttempts = 50000;
    let attempt = 0;
    let bestGame = [];
    let bestScore = -1;
    
    const btnGen = document.getElementById('btn-generate');
    btnGen.innerHTML = '<span class="icon">⏳</span> Gerando...';
    
    setTimeout(() => {
        let needed = 15 - fixas.length;
        if (needed < 0 || needed > pool.length) {
            alert("Dezenas insuficientes para fechar 15 pontos.");
            btnGen.innerHTML = '<span class="icon">🔄</span> Gerar Jogo';
            return;
        }

        while(attempt < maxAttempts) {
            attempt++;
            let shuffled = [...pool].sort(() => 0.5 - Math.random());
            let candidate = [...fixas, ...shuffled.slice(0, needed)];
            
            let score = evaluateGame(candidate);
            if (score === 8) {
                bestGame = candidate;
                break;
            }
            if (score > bestScore) {
                bestScore = score;
                bestGame = candidate;
            }
        }
        
        // Aplica o melhor jogo encontrado
        for (let i = 1; i <= 25; i++) {
            if (numbersState[i] === 'padrao') {
               numbersState[i] = 'none';
            }
        }
        
        bestGame.forEach(n => {
             if (numbersState[n] !== 'fixar') {
                 numbersState[n] = 'padrao';
             }
        });
        
        updateUI();
        btnGen.innerHTML = '<span class="icon">🔄</span> Gerar Jogo';
    }, 50);
}

function evaluateGame(cand) {
    let impares = 0, pares = 0, repetidas = 0;
    let moldura = 0, primos = 0, multiplos = 0, fibo = 0, soma = 0;

    cand.forEach(n => {
        if (n % 2 === 0) pares++; else impares++;
        if (ULTIMO_JOGO.includes(n)) repetidas++;
        if (MOLDURA.includes(n)) moldura++;
        if (PRIMOS.includes(n)) primos++;
        if (MULTIPLOS_3.includes(n)) multiplos++;
        if (FIBONACCI.includes(n)) fibo++;
        soma += n;
    });

    let score = 0;
    if (impares >= 7 && impares <= 8) score++;
    if (pares >= 7 && pares <= 8) score++;
    if (repetidas >= 8 && repetidas <= 10) score++;
    if (moldura >= 9 && moldura <= 10) score++;
    if (primos >= 5 && primos <= 6) score++;
    if (multiplos >= 4 && multiplos <= 5) score++;
    if (fibo >= 4 && fibo <= 5) score++;
    if (soma >= 195 && soma <= 209) score++;
    return score;
}

// Start
init();
