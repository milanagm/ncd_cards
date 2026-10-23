"""Group Anagrams."""
import collections

from ._gen import text

METHOD = "groupAnagrams"
COMPARE = "groups"


def reference(strs):
    groups = collections.defaultdict(list)
    for s in strs:
        groups["".join(sorted(s))].append(s)
    return list(groups.values())


CASES = [
    (["act", "pots", "tops", "cat", "stop", "hat"],), (["x"],), ([""],),
    (["eat", "tea", "tan", "ate", "nat", "bat"],), (["bdddddddddd", "bbbbbbbbbbc"],),
    (["ab", "ba", "abc", "cab", "a"],), (["", "", "b"],),
]


def random_case(rng):
    return ([text(rng, "abc", 0, 4) for _ in range(rng.randint(1, 8))],)
