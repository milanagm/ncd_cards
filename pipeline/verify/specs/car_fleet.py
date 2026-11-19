"""Car Fleet: cars catching up with a slower car ahead join its fleet; count fleets arriving at target."""
from fractions import Fraction

METHOD = "carFleet"
COMPARE = "exact"


def reference(target, position, speed):
    fleets, slowest = 0, None
    for p, s in sorted(zip(position, speed), reverse=True):
        t = Fraction(target - p, s)  # exact, so equal arrival times count as one fleet
        if slowest is None or t > slowest:
            fleets, slowest = fleets + 1, t
    return fleets


CASES = [
    (10, [1, 4], [3, 2]), (10, [4, 1, 0, 7], [2, 2, 1, 1]), (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]),
    (10, [3], [3]), (100, [0, 2, 4], [4, 2, 1]), (10, [0, 4, 2], [2, 1, 3]), (10, [6, 8], [3, 2]),
    (1000, [0, 999], [100, 1]),
]


def random_case(rng):
    target = rng.randint(2, 30)
    n = rng.randint(1, min(6, target))
    position = rng.sample(range(target), n)
    speed = [rng.randint(1, 5) for _ in range(n)]
    return (target, position, speed)
