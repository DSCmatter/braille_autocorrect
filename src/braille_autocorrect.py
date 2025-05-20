from typing import Dict, List, Tuple

# Mapping QWERTY keys to Braille dot positions (1-6)
QWERTY_TO_DOTS: Dict[str, int] = {
    's': 1, 'd': 2, 'f': 3,
    'j': 4, 'k': 5, 'l': 6
}

def qwerty_to_pattern(keys: str) -> str:
    """
    Convert a string of QWERTY Braille keys (e.g., "sdfj") into a sorted dot pattern string (e.g., "123").
    """
    dots = [QWERTY_TO_DOTS[k] for k in keys if k in QWERTY_TO_DOTS]
    return ''.join(str(d) for d in sorted(dots))

def levenshtein(a: str, b: str, max_dist: int = None) -> int:
    """
    Compute Levenshtein distance between strings a and b.
    If max_dist is provided, abort and return > max_dist once distance exceeds it.
    """
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = len(a), len(b)
    prev = list(range(n+1))
    for j in range(1, m+1):
        curr = [j] + [0] * n
        for i in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            curr[i] = min(prev[i] + 1, curr[i-1] + 1, prev[i-1] + cost)
        if max_dist is not None and min(curr) > max_dist:
            return max_dist + 1
        prev = curr
    return prev[n]

class BrailleAutoCorrect:
    def __init__(self, dictionary: List[str]):
        # Preprocess dictionary: map each word to its Braille pattern
        self.pattern_map = {w: qwerty_to_pattern(w) for w in dictionary}

    def suggest(self, input_keys: str, max_dist: int = 2, top_k: int = 3) -> List[str]:
        """
        Given input Braille keys, suggest up to top_k closest words within max_dist.
        """
        input_pat = qwerty_to_pattern(input_keys)
        candidates: List[Tuple[str, int]] = []
        for word, pat in self.pattern_map.items():
            dist = levenshtein(input_pat, pat, max_dist)
            if dist <= max_dist:
                candidates.append((word, dist))
        candidates.sort(key=lambda x: (x[1], x[0]))
        return [w for w, _ in candidates[:top_k]]

if __name__ == "__main__":
    # Example usage
    braille_words = ['sad', 'fat', 'cat', 'kitty', 'ads']  # dictionary in QWERTY format
    ac = BrailleAutoCorrect(braille_words)
    tests = ['sdf', 'sd', 'sdfj']
    for t in tests:
        print(f"Input: {t} -> Suggestions: {ac.suggest(t)}")
