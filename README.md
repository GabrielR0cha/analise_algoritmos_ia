# Estudo Dirigido 1 - Inteligência Artificial

Este projeto implementa e compara diferentes algoritmos de busca para resolver o jogo **Lights Out**. O objetivo é encontrar a sequência de cliques necessária para ligar todas as luzes do tabuleiro.

## Algoritmos Implementados

O projeto inclui as seguintes estratégias de busca:

- **Busca em Largura (BFS):** Garante a solução ótima (menor número de passos), mas consome muita memória.
- **Busca em Profundidade (DFS):** Explora caminhos até um limite definido; nem sempre encontra a solução ótima.
- **Busca Gulosa (Greedy):** Utiliza uma heurística para priorizar estados que parecem mais próximos do objetivo.
- **Busca A*:** Combina o custo do caminho percorrido com a heurística para encontrar a solução ótima de forma mais eficiente que o BFS.
- **Hill Climbing:** Um algoritmo de busca local que tenta melhorar o estado atual a cada passo, podendo ficar preso em máximos locais.

## Estrutura do Projeto

- `codigo-fonte/main.py`: Contém a implementação do jogo, dos algoritmos de busca e o script para execução dos experimentos.

## Como Executar

Certifique-se de ter o Python 3 instalado em sua máquina.

Para rodar os experimentos e ver a comparação de desempenho entre os algoritmos:

```bash
python3 codigo-fonte/main.py
```

## Métricas de Comparação

Para cada experimento, o script reporta:
- **Status/Passos:** Se a solução foi encontrada e quantos cliques foram necessários.
- **Nós Expandidos:** Quantos estados foram explorados durante a busca.
- **Tempo (s):** Tempo total de execução do algoritmo.
- **Memória (KB):** Pico de uso de memória durante a execução.
