"""
Princípio:
  DFS explora o espaço de estados seguindo sempre o ramo mais profundo
  antes de recuar (backtrack). Utiliza uma pilha LIFO — implementada
  aqui de forma iterativa para evitar estouro da pilha de chamadas do
  Python em instâncias maiores.

Complexidade:
  Tempo  : O(b^m)  — m = profundidade máxima (pode ser muito maior que d)
  Memória: O(b·m)  — apenas o caminho atual e seus irmãos precisam ficar
                     na memória, o que é uma vantagem clara sobre BFS.

Limitações importantes:
  1. DFS NÃO garante optimalidade — pode encontrar soluções longas.
  2. DFS pode não terminar em espaços infinitos. Aqui limitamos a
     profundidade máxima (depth_limit) para controlar isso.
  3. Em grafos com ciclos, o controle de estados visitados é necessário
     para evitar loops infinitos. Mantemos o conjunto do CAMINHO ATUAL
     (não todos os visitados) para preservar completude com menor custo
     de memória.

Decisão de projeto — `path_visited` em vez de `global_visited`:
  Usar um conjunto global de visitados (como em BFS) impediria o DFS de
  explorar o mesmo estado por caminhos diferentes. Para DFS isso pode
  ser problemático: o algoritmo poderia bloquear soluções válidas.
  Optamos por rastrear apenas os estados no CAMINHO ATUAL (prevenindo
  ciclos imediatos) e permitir revisitas em ramos distintos.
"""

import time
import tracemalloc
from dataclasses import dataclass, field

from board import Board, all_on, neighbors
from bfs import SearchResult          # reutiliza o dataclass de resultado



# Busca em Profundidade (iterativa com limite de profundidade)


def dfs(initial: Board, depth_limit: int = 25, max_nodes: int = 500_000) -> SearchResult:
    """
    Resolve o Lights Out usando DFS iterativo com limite de profundidade.

    Parâmetros:

    initial     : estado inicial
    depth_limit : profundidade máxima de busca
                  (N² é um limite natural razoável para o Lights Out)
    max_nodes   : número máximo de nós expandidos

    Retorna:

    SearchResult (optimal=False, pois DFS não garante solução mínima).
    """
    n = len(initial)
    result = SearchResult(algorithm="DFS", board_size=n, found=False, optimal=False)

    if all_on(initial):
        result.found = True
        return result

    tracemalloc.start()
    start = time.perf_counter()

    # Pilha: cada entrada é (estado, ações_até_aqui, estados_no_caminho)
    # - "ações_até_aqui"     : lista de (row, col) para reconstruir o caminho
    # - "estados_no_caminho" : frozenset dos estados no caminho atual (anti-ciclo)
    stack: list[tuple[Board, list, frozenset]] = [
        (initial, [], frozenset([initial]))
    ]
    nodes_expanded = 0

    while stack:
        if nodes_expanded >= max_nodes:
            break

        current, actions, path_states = stack.pop()
        nodes_expanded += 1

        # Poda por profundidade
        if len(actions) >= depth_limit:
            continue

        for next_board, action in neighbors(current):
            if next_board in path_states:       # ciclo no caminho atual
                continue

            new_actions = actions + [action]    # cria nova lista (imutável por design)
            new_path = path_states | {next_board}

            if all_on(next_board):
                result.found = True
                result.actions = new_actions
                result.nodes_expanded = nodes_expanded
                result.time_seconds = time.perf_counter() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                result.memory_peak_kb = peak / 1024
                return result

            stack.append((next_board, new_actions, new_path))

    result.nodes_expanded = nodes_expanded
    result.time_seconds = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result.memory_peak_kb = peak / 1024
    return result
