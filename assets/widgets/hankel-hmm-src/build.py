#!/usr/bin/env python3
"""Build the self-contained Hankel-to-HMM teaching widget.

The browser receives only saved, deterministic toy-model results.  All linear
algebra happens here so the published widget has no runtime dependencies.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
# In the blog, this source directory sits beside the generated widget:
# assets/widgets/hankel-hmm-src/ -> assets/widgets/hankel-hmm.html.
OUT = HERE.parent / "hankel-hmm.html"
DEPTH = 3
MAX_RANK = 6
EVAL_LENGTH = 2 * DEPTH
SAMPLE_SIZES = {"sample-small": 2_500, "sample-large": 50_000}


def model_catalog() -> dict[str, dict]:
    golden_t0 = np.array([[0.0, 0.40], [0.0, 0.0]])
    golden_t1 = np.array([[0.60, 0.0], [1.0, 0.0]])

    z1r_t0 = np.array([
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.5, 0.0, 0.0],
    ])
    z1r_t1 = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.5, 0.0, 0.0],
    ])

    mess3 = np.array([
        [[.14, .06, .06], [.03, .28, .06], [.03, .06, .28]],
        [[.28, .03, .06], [.06, .14, .06], [.06, .03, .28]],
        [[.28, .06, .03], [.06, .28, .03], [.06, .06, .14]],
    ])

    return {
        "golden": {
            "label": "Golden Mean",
            "short": "No consecutive 0s",
            "symbols": ["0", "1"],
            "T": np.stack([golden_t0, golden_t1]),
            "positions": [[0.25, 0.5], [0.75, 0.5]],
        },
        "z1r": {
            "label": "Zero-One-Random",
            "short": "0, then 1, then a fair bit",
            "symbols": ["0", "1"],
            "T": np.stack([z1r_t0, z1r_t1]),
            "positions": [[0.16, 0.68], [0.50, 0.25], [0.84, 0.68]],
        },
        "mess3": {
            "label": "Mess3",
            "short": "Three symbols, mixed-state geometry",
            "symbols": ["0", "1", "2"],
            "T": mess3,
            "positions": [[0.18, 0.68], [0.50, 0.22], [0.82, 0.68]],
        },
    }


def stationary_distribution(T: np.ndarray) -> np.ndarray:
    transition = T.sum(axis=0)
    values, vectors = np.linalg.eig(transition.T)
    vector = np.real(vectors[:, np.argmin(np.abs(values - 1.0))])
    if vector.sum() < 0:
        vector *= -1
    vector = np.maximum(vector, 0)
    return vector / vector.sum()


def all_words(alphabet_size: int, max_length: int) -> list[tuple[int, ...]]:
    return [
        word
        for length in range(max_length + 1)
        for word in itertools.product(range(alphabet_size), repeat=length)
    ]


def word_probability(word: tuple[int, ...], T: np.ndarray, pi: np.ndarray) -> float:
    state = pi.copy()
    for symbol in word:
        state = state @ T[symbol]
    return float(state.sum())


def simulate(T: np.ndarray, pi: np.ndarray, n: int, seed: int) -> list[int]:
    rng = np.random.default_rng(seed)
    state = int(rng.choice(len(pi), p=pi))
    stream: list[int] = []
    for _ in range(n):
        outcomes: list[tuple[int, int]] = []
        probabilities: list[float] = []
        for symbol in range(T.shape[0]):
            for target in range(T.shape[1]):
                outcomes.append((symbol, target))
                probabilities.append(float(T[symbol, state, target]))
        choice = int(rng.choice(len(outcomes), p=np.asarray(probabilities)))
        symbol, state = outcomes[choice]
        stream.append(symbol)
    return stream


def empirical_probabilities(stream: list[int], max_length: int) -> dict[tuple[int, ...], float]:
    result: dict[tuple[int, ...], float] = {(): 1.0}
    n = len(stream)
    for length in range(1, max_length + 1):
        total = n - length + 1
        counts: dict[tuple[int, ...], int] = {}
        for start in range(total):
            word = tuple(stream[start:start + length])
            counts[word] = counts.get(word, 0) + 1
        for word, count in counts.items():
            result[word] = count / total
    return result


def round_number(value: float, digits: int = 8) -> float:
    if abs(value) < 0.5 * 10 ** (-digits):
        return 0.0
    return round(float(value), digits)


def matrix_payload(matrix: np.ndarray, digits: int = 7) -> list[list[float]]:
    return [[round_number(value, digits) for value in row] for row in matrix]


def build_condition(
    model_key: str,
    model: dict,
    regime: str,
    seed: int,
) -> dict:
    T = model["T"]
    alphabet_size = T.shape[0]
    pi = stationary_distribution(T)
    basis = all_words(alphabet_size, DEPTH)
    basis_index = {word: index for index, word in enumerate(basis)}
    max_length = 2 * DEPTH + 1

    exact = {
        word: word_probability(word, T, pi)
        for word in all_words(alphabet_size, max_length)
    }
    if regime == "exact":
        observed = exact
        stream = simulate(T, pi, 96, seed)
        sample_size = None
    else:
        sample_size = SAMPLE_SIZES[regime]
        long_stream = simulate(T, pi, sample_size, seed)
        observed = empirical_probabilities(long_stream, max_length)
        stream = long_stream[:96]

    def p_obs(word: tuple[int, ...]) -> float:
        return float(observed.get(word, 0.0))

    H = np.array([[p_obs(prefix + suffix) for suffix in basis] for prefix in basis])
    shifted = np.array([
        [[p_obs(prefix + (symbol,) + suffix) for suffix in basis] for prefix in basis]
        for symbol in range(alphabet_size)
    ])
    U, singular_values, Vt = np.linalg.svd(H, full_matrices=False)

    eval_words = list(itertools.product(range(alphabet_size), repeat=EVAL_LENGTH))
    p_true = np.array([exact[word] for word in eval_words], dtype=float)
    p_true /= p_true.sum()
    ranks = []
    denominator = max(float(np.linalg.norm(H, ord="fro")), 1e-15)

    for rank in range(1, MAX_RANK + 1):
        Ur = U[:, :rank]
        sr = singular_values[:rank]
        Vr = Vt[:rank, :].T
        Hr = (Ur * sr) @ Vr.T
        threshold = max(float(singular_values[0]) * 1e-10, 1e-14)
        active = sr > threshold
        sqrt_sr = np.where(active, np.sqrt(sr), 0.0)
        inv_sqrt = np.diag(np.where(active, 1.0 / np.sqrt(np.maximum(sr, threshold)), 0.0))
        operators = [
            inv_sqrt @ Ur.T @ shifted[symbol] @ Vr @ inv_sqrt
            for symbol in range(alphabet_size)
        ]
        alpha = Ur[basis_index[()], :] * sqrt_sr
        beta = sqrt_sr * Vr[basis_index[()], :]
        q_values = []
        for word in eval_words:
            state = alpha.copy()
            for symbol in word:
                state = state @ operators[symbol]
            q_values.append(float(state @ beta))
        q_raw = np.asarray(q_values)
        negative_mass = float(np.maximum(-q_raw, 0).sum())
        q = np.maximum(q_raw, 1e-12)
        q /= q.sum()
        difference = p_true - q

        support = p_true > 0
        kl = float(np.sum(p_true[support] * np.log(p_true[support] / q[support])))
        ranks.append({
            "r": rank,
            "metrics": {
                "l1": round_number(float(np.abs(difference).sum())),
                "l2": round_number(float(np.linalg.norm(difference))),
                "kl": round_number(kl),
                "hankel": round_number(float(np.linalg.norm(H - Hr, ord="fro") / denominator)),
            },
            "negative_mass": round_number(negative_mass),
            "normalization_error": round_number(abs(float(q_raw.sum()) - 1.0)),
            "operators": [matrix_payload(operator, 5) for operator in operators],
            "alpha": [round_number(value, 5) for value in alpha],
            "beta": [round_number(value, 5) for value in beta],
        })

    exact_H = np.array([
        [exact[prefix + suffix] for suffix in basis]
        for prefix in basis
    ])
    true_rank = int(np.linalg.matrix_rank(exact_H, tol=1e-10))

    # The finite block should expose the known process rank at this depth.
    assert true_rank == T.shape[1], (model_key, true_rank, T.shape[1])
    assert abs(float(H[0, 0]) - 1.0) < 1e-12
    assert abs(float(p_true.sum()) - 1.0) < 1e-10
    if regime == "exact":
        exact_metrics = ranks[true_rank - 1]["metrics"]
        assert exact_metrics["l1"] < 1e-7, (model_key, exact_metrics)
        assert exact_metrics["hankel"] < 1e-7, (model_key, exact_metrics)

    heat_limit = min(15, len(basis))
    return {
        "regime": regime,
        "sample_size": sample_size,
        "seed": seed,
        "basis_labels": [word_label(word, model["symbols"]) for word in basis[:heat_limit]],
        "heatmap": matrix_payload(H[:heat_limit, :heat_limit], 6),
        "heat_max": round_number(float(np.max(H[:heat_limit, :heat_limit])), 6),
        "singular_values": [round_number(value, 10) for value in singular_values[:MAX_RANK + 3]],
        "stream": [model["symbols"][symbol] for symbol in stream],
        "ranks": ranks,
    }


def word_label(word: tuple[int, ...], symbols: list[str]) -> str:
    if not word:
        return "ε"
    return "".join(symbols[index] for index in word)


def graph_edges(T: np.ndarray, symbols: list[str]) -> list[dict]:
    edges = []
    for symbol_index, symbol in enumerate(symbols):
        for source in range(T.shape[1]):
            for target in range(T.shape[2]):
                probability = float(T[symbol_index, source, target])
                if probability > 1e-12:
                    edges.append({
                        "source": source,
                        "target": target,
                        "symbol": symbol,
                        "probability": round_number(probability, 4),
                    })
    return edges


def build_payload() -> dict:
    catalog = model_catalog()
    result = {
        "meta": {
            "depth": DEPTH,
            "max_rank": MAX_RANK,
            "eval_length": EVAL_LENGTH,
            "metric_notes": {
                "l1": "L1 distance between true and reconstructed length-6 word distributions (TV is half this).",
                "l2": "Euclidean distance between true and reconstructed length-6 word distributions.",
                "kl": "KL(true || reconstruction), after clipping and renormalizing the displayed finite-word distribution.",
                "hankel": "Relative Frobenius residual of the observed finite Hankel block.",
            },
        },
        "models": {},
    }
    regimes = ["exact", "sample-small", "sample-large"]
    for model_index, (key, model) in enumerate(catalog.items()):
        pi = stationary_distribution(model["T"])
        conditions = {}
        for regime_index, regime in enumerate(regimes):
            seed = 1701 + 100 * model_index + 11 * regime_index
            conditions[regime] = build_condition(key, model, regime, seed)
        result["models"][key] = {
            "label": model["label"],
            "short": model["short"],
            "symbols": model["symbols"],
            "state_count": int(model["T"].shape[1]),
            "true_rank": int(model["T"].shape[1]),
            "positions": model["positions"],
            "stationary": [round_number(value, 6) for value in pi],
            "edges": graph_edges(model["T"], model["symbols"]),
            "conditions": conditions,
        }
    return result


def main() -> None:
    payload = build_payload()
    payload_json = json.dumps(payload, separators=(",", ":"), allow_nan=False)
    template = (HERE / "template.html").read_text()
    rendered = template.replace("__WIDGET_DATA__", payload_json)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered)
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
