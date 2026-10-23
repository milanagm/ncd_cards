"""Top K Frequent Elements: cases are built so the answer is unique."""
import collections

METHOD = "topKFrequent"
COMPARE = "unordered"


def reference(nums, k):
    return [v for v, _ in collections.Counter(nums).most_common(k)]


CASES = [
    ([1, 2, 2, 3, 3, 3], 2), ([7, 7], 1), ([1], 1), ([4, 1, -1, 2, -1, 2, 3], 2),
    ([5, 5, 5, 6, 6, 7], 1), ([1, 1, 1, 2, 2, 3], 3),
]


def random_case(rng):
    values = rng.sample(range(-9, 10), rng.randint(1, 5))
    counts = rng.sample(range(1, 7), len(values))  # distinct counts -> unique top k
    nums = [v for v, c in zip(values, counts) for _ in range(c)]
    rng.shuffle(nums)
    return (nums, rng.randint(1, len(values)))
