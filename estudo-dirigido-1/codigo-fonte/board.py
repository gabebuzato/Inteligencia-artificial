"""
Centraliza toda a lógica do tabuleiro para que os algoritmos de busca
possam reutilizá-la sem duplicação de código.

Decisão de projeto:
  O tabuleiro é representado como uma tupla de tuplas de inteiros (0/1).
  Tuplas são imutáveis e hasháveis, o que permite usá-las diretamente
  como chaves em conjuntos e dicionários (essencial para os conjuntos de
  estados visitados em BFS, DFS e A*).
"""

from typing import Generator



# Tipo auxiliar

Board = tuple[tuple[int, ...], ...]   # grade N×N de 0s e 1s



# Funções básicas do tabuleiro


def create_board(n: int, cells: list[int] | None = None) -> Board:
    """
    Cria um tabuleiro N×N.

    Parâmetros

    n     : dimensão do tabuleiro
    cells : lista linearizada de valores 0/1 (linha por linha).
            Se None, todas as células começam DESLIGADAS (0).

    Retorna

    Board (tupla de tuplas)
    """
    if cells is None:
        cells = [0] * (n * n)
    return tuple(tuple(cells[i * n:(i + 1) * n]) for i in range(n))


def all_on(board: Board) -> bool:
    """Retorna True se todas as células estão ligadas (= 1)."""
    return all(cell == 1 for row in board for cell in row)


def count_off(board: Board) -> int:
    """Conta quantas células estão desligadas — usada como heurística."""
    return sum(cell == 0 for row in board for cell in row)


def toggle(board: Board, row: int, col: int) -> Board:
    """
    Aplica um clique na célula (row, col).

    Regra do Lights Out:
      A célula clicada e seus vizinhos diretos (cima, baixo, esquerda,
      direita) trocam de estado (0↔1).

    Retorna um NOVO tabuleiro sem modificar o original.
    """
    n = len(board)
    # Converte para lista mutável de listas
    grid = [list(row) for row in board]

    for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < n and 0 <= c < n:
            grid[r][c] ^= 1          # XOR: inverte sem branch

    return tuple(tuple(r) for r in grid)


def neighbors(board: Board) -> Generator[tuple[Board, tuple[int, int]], None, None]:
    """
    Gerador que produz todos os estados alcançáveis a partir de `board`
    com um único clique, junto com a ação (row, col) que o gerou.

    Yields
    ------
    (novo_tabuleiro, (row, col))
    """
    n = len(board)
    for r in range(n):
        for c in range(n):
            yield toggle(board, r, c), (r, c)



# Geração de instâncias para experimentos


import random


def random_board(n: int, seed: int | None = None) -> Board:
    """
    Gera um tabuleiro N×N com estado aleatório, garantindo que exista
    solução (aplica cliques aleatórios a partir do estado-meta).

    Partir do estado-meta e aplicar cliques garante que o puzzle seja
    sempre solucionável — evitamos configurações sem solução que existem
    no Lights Out clássico.
    """
    rng = random.Random(seed)
    # Estado-meta: todas ligadas
    board = create_board(n, [1] * (n * n))
    # Embaralha aplicando cliques aleatórios
    moves = n * n                        # número de cliques embaralhadores
    for _ in range(moves):
        r = rng.randrange(n)
        c = rng.randrange(n)
        board = toggle(board, r, c)
    return board


def board_to_str(board: Board) -> str:
    """Representação visual simples para debug/logs."""
    symbols = {0: "⬛", 1: "🟡"}
    return "\n".join("".join(symbols[c] for c in row) for row in board)
