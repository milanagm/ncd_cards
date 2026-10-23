"""Small random-input helpers shared by the specs."""


def ints(rng, min_len, max_len, lo, hi):
    return [rng.randint(lo, hi) for _ in range(rng.randint(min_len, max_len))]


def text(rng, alphabet, min_len, max_len):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(min_len, max_len)))
