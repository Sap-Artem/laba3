import math
import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    mas = [[0] * n for i in range(n)]
    k = 0
    for i in range(0, n):
        for j in range(0, n):
            mas[i][j] = values[k]
            k = k + 1
    return mas
    pass


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    mas = [0] * len(grid)
    for i in range(0, len(grid)):
        mas[i] = grid[pos[0]][i]
    return mas
    pass


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    mas = [0] * len(grid[0])
    for i in range(0, len(grid[0])):
        mas[i] = grid[i][pos[1]]
    return mas
    pass


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    mas = [0] * 9
    k = 0
    for i in range(math.floor(pos[0] / 3) * 3, (math.floor(pos[0] / 3) + 1) * 3):
        for j in range(math.floor(pos[1] / 3) * 3, (math.floor(pos[1] / 3) + 1) * 3):
            mas[k] = grid[i][j]
            k = k + 1
    return mas
    pass


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (grid[i][j] == '.'):
                mas = (i, j)
                return mas
    mas = (-1, -1)
    return mas
    pass


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    mas_row = get_row(grid, pos)
    set_row = set()
    for i in range(0, len(mas_row)):
        set_row.add(mas_row[i])
    mas_col = get_col(grid, pos)
    set_col = set()
    for i in range(0, len(mas_col)):
        set_col.add(mas_col[i])
    mas_block = get_block(grid, pos)
    set_block = set()
    for i in range(0, len(mas_block)):
        set_block.add(mas_block[i])
    set_summary = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    set_summary.difference_update(set_row)
    set_summary.difference_update(set_col)
    set_summary.difference_update(set_block)
    return set_summary
    pass


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """
    Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения, которые могут находиться на этой позиции
    3. Для каждого возможного значения:
        3.1. Поместить это значение на эту позицию
        3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    >>> grid = read_sudoku('test_puzzles.txt')
    >>> solve(grid)
    [['2', '9', '3', '4', '5', '7', '6', '8', '1'], ['4', '7', '5', '1', '8', '6', '3', '9', '2'], ['1', '6', '8', '3', '9', '2', '7', '4', '5'], ['9', '4', '2', '5', '7', '1', '8', '6', '3'], ['3', '8', '1', '6', '2', '9', '5', '7', '4'], ['6', '5', '7', '8', '3', '4', '1', '2', '9'], ['7', '2', '6', '9', '1', '3', '4', '5', '8'], ['5', '1', '4', '2', '6', '8', '9', '3', '7'], ['8', '3', '9', '7', '4', '5', '2', '1', '6']]
    """
    pos = find_empty_positions(grid)
    if pos == (-1,-1):
        if check_solution(grid):
            return grid
    else:
        value = find_possible_values(grid,pos)
        for i in value:
            grid[pos[0]][pos[1]] = i
            solve(grid)
            if check_solution(grid):
                return grid
            grid[pos[0]][pos[1]] = '.'
    pass


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
        >>> grid = read_sudoku('puzzle_bad.txt')
        >>> check_solution(grid)
        False
        >>> grid = read_sudoku('puzzle_good.txt')
        >>> check_solution(grid)
        True
        """
    for i in range (0,9):
        if sum(1 for row in solution for e in row if e == '.') != 0:
            return False
        pos = (i,0)
        value = get_row(solution,pos)
        for j in range(0, len(value)-1):
            for k in range(j+1,len(value)):
                if value[j] == value[k]:
                    return False
        pos = (0, i)
        value = get_col(solution, pos)
        for j in range(0, len(value) - 1):
            for k in range(j + 1, len(value)):
                if value[j] == value[k]:
                    return False
    for i in range (0,3):
        for j in range (0,3):
            pos = (1+j*3, 1+i*3)
            value = get_block(solution,pos)
            for j in range(0, len(value) - 1):
                for k in range(j + 1, len(value)):
                    if value[j] == value[k]:
                        return False
    return True
    # TODO: Add doctests with bad puzzles
    pass


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    shablon = [['2', '9', '3', '4', '5', '7', '6', '8', '1'], ['4', '7', '5', '1', '8', '6', '3', '9', '2'], ['1', '6', '8', '3', '9', '2', '7', '4', '5'], ['9', '4', '2', '5', '7', '1', '8', '6', '3'], ['3', '8', '1', '6', '2', '9', '5', '7', '4'], ['6', '5', '7', '8', '3', '4', '1', '2', '9'], ['7', '2', '6', '9', '1', '3', '4', '5', '8'], ['5', '1', '4', '2', '6', '8', '9', '3', '7'], ['8', '3', '9', '7', '4', '5', '2', '1', '6']]
    while N < 81:
        pos0 = random.randint(0, 8)
        pos1 = random.randint(0, 8)
        if shablon[pos0][pos1]!='.':
            shablon[pos0][pos1] = '.'
            N = N + 1
    return shablon
    pass


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
def main():
    grid = read_sudoku('puzzle1.txt')
    display(solve(grid))

