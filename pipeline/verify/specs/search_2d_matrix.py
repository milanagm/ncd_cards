"""Search a 2D Matrix: rows sorted, each row starts above the previous row's end."""
METHOD = "searchMatrix"
COMPARE = "exact"


def reference(matrix, target):
    return any(target in row for row in matrix)


M = [[1, 2, 4, 8], [10, 11, 12, 13], [14, 20, 30, 40]]
CASES = [
    (M, 10), (M, 15), (M, 1), (M, 40), (M, 0), (M, 41), (M, 9), (M, 12),
    ([[1]], 1), ([[1]], 2), ([[1], [3]], 3), ([[1], [3]], 2), ([[1, 3]], 3),
]


def random_case(rng):
    m, n = rng.randint(1, 4), rng.randint(1, 4)
    values = sorted(rng.sample(range(-30, 30), m * n))
    matrix = [values[r * n:(r + 1) * n] for r in range(m)]
    target = rng.choice(values) if rng.random() < 0.5 else rng.randint(-31, 31)
    return (matrix, target)
