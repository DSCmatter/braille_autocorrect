# Braille Auto-Correct

This project provides a simple, real-time auto-correct and suggestion system for Braille input using only the Levenshtein distance algorithm. It’s designed for QWERTY-based Braille typing (keys `s`, `d`, `f`, `j`, `k`, `l` mapping to Braille dots 1–6).

---

## 1. Objective

Provide a simple yet effective real-time suggestion system for QWERTY-based Braille input that:

* Corrects substitutions, insertions, and deletions.
* Requires minimal setup and dependencies.
* Delivers low latency for small-to-medium dictionaries.

---

## 2. Usage

1. **Install**:
   No external packages required—pure Python.

2. **Define your dictionary** (list of words in QWERTY Braille form).

3. **Initialize**:

   ```python
   from braille_autocorrect import BrailleAutoCorrect

   words = ['sad', 'fad', 'lad', 'sal', 'ads']
   ac = BrailleAutoCorrect(words)
   ```

4. **Get suggestions**:

   ```python
   suggestions = ac.suggest('sdf', max_dist=2, top_k=3)
   print(suggestions)  # e.g. ['sad', 'ads', 'fad']
   ```
5. **Outputs**:

```python
Input: sdf -> Suggestions: ['ads', 'sad', 'fat']
Input: sd -> Suggestions: ['ads', 'sad', 'cat']
Input: sdfj -> Suggestions: ['ads', 'sad']
```
---

## 3. Design Overview

### 3.1 Input Normalization

* **Mapping**: `{'s':1, 'd':2, 'f':3, 'j':4, 'k':5, 'l':6}`
* Convert a key sequence (e.g. `"sdfj"`) → dot pattern string (`"1234"`).

### 3.2 Levenshtein Distance

- **DP Table**: Compute in O(n·m) time, where n, m are string lengths.
- **Space**: O(min(n,m)) by storing only the previous row.
- **Early Exit**: Abort when the current row’s minimal edit cost exceeds max_dist.


### 3.3 Suggestion Logic

1. **Brute-Force Scan** all dictionary patterns.
2. **Filter** by distance ≤ `max_dist`.
3. **Sort** by `(distance, word)`.
4. **Return** top `K` results.

---

## 4. Optimizations

* **Early-Exit** in distance calc reduces wasted DP iterations.
* **Precomputed Patterns** avoid re-mapping on each query.
* **Compact Strings** speed string ops and lower memory usage.
* **Threshold Tuning** (`max_dist` of 1–2) balances accuracy and speed.

---

## 5. Trade-Offs

| Choice             | Benefit                              | Drawback                                     |
| ------------------ | ------------------------------------ | -------------------------------------------- |
| Brute-Force Search | Simplicity; no extra data structures | `O(N·n·m)` per query may be slow for large N |
| Levenshtein Metric | Handles all edit types uniformly     | Quadratic with string lengths                |
| Pure Python        | Portable; zero dependencies          | Single-threaded—performance ceiling          |
| Early-Termination  | Prunes costly comparisons early      | Requires careful `max_dist` selection        |

---

## 6. When to Use

* **Ideal** for prototypes, demos, and dictionaries up to \~50K entries.
