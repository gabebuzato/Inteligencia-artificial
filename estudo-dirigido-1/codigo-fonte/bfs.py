"""
Princípio:
  BFS explora o espaço de estados nível por nível, utilizando uma fila
  FIFO. Isso garante que, ao encontrar o estado-objetivo, o caminho
  percorrido seja o de menor número de passos (ótimo em número de ações).

Complexidade:
  Tempo  : O(b^d)  — b = fator de ramificação, d = profundidade da solução
  Memória: O(b^d)  — todos os nós da fronteira precisam ser mantidos

  Para o Lights Out N×N: b = N² (um clique por célula) e d pode crescer
  rapidamente, tornando BFS inviável para tabuleiros maiores que ~3×3.

Decisões de projeto:
  1. Usei `collections.deque` como fila (enqueue O(1), dequeue O(1)).
  2. Registo de estados visitados em um `set` — O(1) para busca e inserção.
  3. O caminho de ações é reconstruído pelo dicionário `parent`, que mapeia
     cada estado ao par (estado_anterior, ação) que o gerou.
"""

import collections
import time
import tracemalloc
from dataclasses import dataclass, field

from board import Board, all_on, neighbors



# Estrutura de resultado (compartilhada por todos os algoritmos)


@dataclass
class SearchResult:
    algorithm: str
    board_size: int
    found: bool
    actions: list[tuple[int, int]] = field(default_factory=list)
    nodes_expanded: int = 0
    time_seconds: float = 0.0
    memory_peak_kb: float = 0.0
    optimal: bool | None = None   # None = não determinado pelo algoritmo



# Busca em Largura


def bfs(initial: Board, max_nodes: int = 500_000) -> SearchResult:
    """
    Resolve o Lights Out usando BFS.

    Parâmetros

    initial   : estado inicial do tabuleiro
    max_nodes : limite de nós expandidos (evita estouro de memória em
                instâncias grandes)

    Retorna

    SearchResult com o caminho ótimo (se encontrado) e métricas.
    """
    n = len(initial)
    result = SearchResult(algorithm="BFS", board_size=n, found=False, optimal=True)

    # Caso trivial: já está resolvido
    if all_on(initial):
        result.found = True
        return result

    tracemalloc.start()
    start = time.perf_counter()

    # parent[estado] = (estado_pai, ação)
    # Permite reconstruir o caminho ao final
    parent: dict[Board, tuple[Board, tuple[int, int]] | None] = {initial: None}

    queue: collections.deque[Board] = collections.deque([initial])
    nodes_expanded = 0

    while queue:
        if nodes_expanded >= max_nodes:
            # Interrompido por limite — marca como não encontrado
            break

        current = queue.popleft()
        nodes_expanded += 1

        for next_board, action in neighbors(current):
            if next_board in parent:        # já visitado
                continue

            parent[next_board] = (current, action)

            if all_on(next_board):
                # Solução encontrada — reconstrói o caminho
                result.found = True
                result.actions = _reconstruct(parent, next_board)
                result.nodes_expanded = nodes_expanded
                result.time_seconds = time.perf_counter() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                result.memory_peak_kb = peak / 1024
                return result

            queue.append(next_board)

    result.nodes_expanded = nodes_expanded
    result.time_seconds = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result.memory_peak_kb = peak / 1024
    return result



# Auxiliar: reconstrói o caminho de ações

def _reconstruct(
    parent: dict[Board, tuple[Board, tuple[int, int]] | None],
    goal: Board,
) -> list[tuple[int, int]]:
    """Segue os ponteiros `parent` do goal até o estado inicial."""
    path = []
    state = goal
    while parent[state] is not None:
        prev, action = parent[state]
        path.append(action)
        state = prev
    path.reverse()
    return path
