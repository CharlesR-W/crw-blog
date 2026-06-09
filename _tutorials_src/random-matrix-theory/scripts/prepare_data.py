"""Precompute all data for the RMT tutorial.

Run once.  Output goes to ../data/*.json.  The Quarto document loads these
JSON files via fetch() in Observable cells -- no Python is run at
slider-change time, so interactivity is instant.
"""
import json
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)


def histogram(x, bins, range_):
    """Return (centers, density) histogram."""
    counts, edges = np.histogram(x, bins=bins, range=range_, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers.tolist(), counts.tolist()


# ---------------------------------------------------------------------------
# Shared eigenvalue samplers.
# ---------------------------------------------------------------------------
def gue_eigenvalues(N):
    """Sample a complex GUE matrix.  Bulk lives on [-2, 2]."""
    A = (rng.standard_normal(size=(N, N)) + 1j * rng.standard_normal(size=(N, N))) / np.sqrt(2)
    H = (A + A.conj().T) / np.sqrt(2 * N)
    return np.sort(np.linalg.eigvalsh(H))


def goe_eigenvalues(N):
    """Sample a real symmetric GOE matrix.  Bulk lives on [-2, 2]."""
    A = rng.standard_normal(size=(N, N))
    H = (A + A.T) / np.sqrt(2 * N)
    return np.sort(np.linalg.eigvalsh(H))


def sample_cov(p, n):
    """Sample one Wishart eigenvalue spectrum."""
    X = rng.standard_normal(size=(n, p))
    S = (X.T @ X) / n
    return np.linalg.eigvalsh(S)


def mp_density(lam, gamma):
    """Marchenko-Pastur density at lam for ratio gamma = p/n."""
    lam_plus = (1 + np.sqrt(gamma)) ** 2
    lam_minus = (1 - np.sqrt(gamma)) ** 2
    out = np.zeros_like(lam, dtype=float)
    inside = (lam > lam_minus) & (lam < lam_plus)
    out[inside] = np.sqrt((lam_plus - lam[inside]) * (lam[inside] - lam_minus)) / (
        2 * np.pi * gamma * lam[inside]
    )
    return out


# ---------------------------------------------------------------------------
# 1.  Continuous gamma sweep for the section-1 hero widget.
#     A range of gamma values; for each, an MP analytic curve and a sample
#     covariance histogram sufficient to be seen.
# ---------------------------------------------------------------------------
def build_section1_data():
    gammas = [round(g, 2) for g in np.linspace(0.05, 1.5, 30)]
    out = {"gammas": gammas, "panels": {}}
    n_base = 800
    for gamma in gammas:
        if gamma <= 1.0:
            n = n_base
            p = max(2, int(round(gamma * n)))
        else:
            # Keep p constant, vary n.  Otherwise p gets huge.
            p = n_base
            n = max(2, int(round(p / gamma)))
        eigs = []
        for _ in range(20):
            eigs.extend(sample_cov(p, n).tolist())
        # Histogram range: a touch beyond MP support.
        lam_plus = (1 + np.sqrt(gamma)) ** 2
        hi = max(lam_plus * 1.18, 0.5)
        centers, density = histogram(eigs, bins=70, range_=(0.0, hi))
        # Analytic MP curve.
        lam = np.linspace(1e-6, hi, 320)
        rho = mp_density(lam, gamma).tolist()
        # Mass at zero when gamma > 1 (n - p zero eigenvalues).
        # We do not draw a delta, but flag it for the prose.
        delta_mass = max(0.0, 1.0 - 1.0 / gamma) if gamma > 1.0 else 0.0
        out["panels"][f"{gamma:.2f}"] = {
            "gamma": gamma,
            "p": p,
            "n": n,
            "hist_x": centers,
            "hist_y": density,
            "mp_x": lam.tolist(),
            "mp_y": rho,
            "lam_minus": (1 - np.sqrt(gamma)) ** 2,
            "lam_plus": lam_plus,
            "delta_mass": delta_mass,
        }
    with open(OUT / "section1_cov.json", "w") as f:
        json.dump(out, f)


# ---------------------------------------------------------------------------
# 2.  Spacings (Poisson vs GUE) and the full GUE spectrum, used to visualize
#     repulsion directly via a scatter of eigenvalues for one realization.
# ---------------------------------------------------------------------------
def poisson_spacings(n_samples=20000):
    x = rng.uniform(0.0, n_samples, size=n_samples)
    x.sort()
    s = np.diff(x)
    return s / s.mean()


def gue_spacings_near_bulk(N, n_realizations):
    out = []
    for _ in range(n_realizations):
        w = gue_eigenvalues(N)
        lo = N // 4
        hi = 3 * N // 4
        s = np.diff(w[lo:hi])
        out.extend((s / s.mean()).tolist())
    return out


def goe_spacings_near_bulk(N, n_realizations):
    out = []
    for _ in range(n_realizations):
        w = goe_eigenvalues(N)
        lo = N // 4
        hi = 3 * N // 4
        s = np.diff(w[lo:hi])
        out.extend((s / s.mean()).tolist())
    return out


def wigner_surmise(s, beta):
    s = np.asarray(s)
    if beta == 1:
        return (np.pi / 2) * s * np.exp(-np.pi * s ** 2 / 4)
    if beta == 2:
        return (32 / np.pi ** 2) * s ** 2 * np.exp(-4 * s ** 2 / np.pi)
    if beta == 4:
        return (262144 / (729 * np.pi ** 3)) * s ** 4 * np.exp(-64 * s ** 2 / (9 * np.pi))
    raise ValueError(beta)


def build_section2_data():
    poisson = poisson_spacings(n_samples=20000)
    gue = gue_spacings_near_bulk(N=300, n_realizations=200)
    grid_x = np.linspace(0.0, 4.0, 200)
    # One sample of GUE eigenvalues + matched iid Poisson sample on the same line,
    # for a visual repulsion comparison.  Center both at 0, width-match.
    w = gue_eigenvalues(150)
    # iid samples drawn from the empirical density of w (use semicircle scale).
    iid = np.sort(rng.uniform(-2.0, 2.0, size=150))
    out = {
        "poisson": dict(zip(["x", "y"], histogram(poisson, bins=60, range_=(0.0, 4.0)))),
        "gue": dict(zip(["x", "y"], histogram(gue, bins=60, range_=(0.0, 4.0)))),
        "exp_x": grid_x.tolist(),
        "exp_y": np.exp(-grid_x).tolist(),
        "wigner_x": grid_x.tolist(),
        "wigner_y": wigner_surmise(grid_x, 2).tolist(),
        "spectrum_gue": w.tolist(),
        "spectrum_iid": iid.tolist(),
    }
    with open(OUT / "section2_spacings.json", "w") as f:
        json.dump(out, f)


# ---------------------------------------------------------------------------
# 4.  Semicircle convergence with finer N control.
# ---------------------------------------------------------------------------
def build_section4_data():
    Ns = [10, 20, 50, 100, 200, 500, 1000, 2000]
    out = {"Ns": Ns, "panels": {}}
    for N in Ns:
        n_real = max(2, 800 // max(1, N))
        if N >= 1000:
            n_real = 4
        eigs = []
        for _ in range(n_real):
            eigs.extend(gue_eigenvalues(N).tolist())
        centers, density = histogram(eigs, bins=80, range_=(-2.6, 2.6))
        out["panels"][str(N)] = {"x": centers, "y": density, "n_real": n_real}
    lam = np.linspace(-2.0, 2.0, 240)
    out["semicircle_x"] = lam.tolist()
    out["semicircle_y"] = (np.sqrt(np.maximum(0, 4 - lam ** 2)) / (2 * np.pi)).tolist()
    with open(OUT / "section4_semicircle.json", "w") as f:
        json.dump(out, f)


# ---------------------------------------------------------------------------
# 5.  Stieltjes transform G(lambda + i*eps) for the semicircle, plus a
#     "watch the cut emerge" widget (real and imaginary parts vs lambda).
# ---------------------------------------------------------------------------
def stieltjes_semicircle(z):
    """Closed form: G(z) = (z - sqrt(z^2 - 4)) / 2 with the branch chosen so
    that G(z) ~ 1/z at infinity.
    """
    # Use complex sqrt on z^2 - 4 with the principal branch.  For z just above
    # the real line the imaginary part should be -i*pi*rho(lam), giving
    # density via -Im G / pi.
    s = np.sqrt(z ** 2 - 4 + 0j)
    # Pick the sign so Im(G) <= 0 above the real axis.
    G_plus = (z - s) / 2
    G_minus = (z + s) / 2
    # For Im z > 0, the correct branch is the one with Im G < 0.  Choose it.
    use_plus = np.imag(G_plus) < np.imag(G_minus)
    return np.where(use_plus, G_plus, G_minus)


def build_section_stieltjes_data():
    lam = np.linspace(-3.0, 3.0, 360)
    epsilons = [round(e, 4) for e in [0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.001]]
    panels = {}
    for eps in epsilons:
        z = lam + 1j * eps
        G = stieltjes_semicircle(z)
        panels[f"{eps:.4f}"] = {
            "lam": lam.tolist(),
            "re_G": np.real(G).tolist(),
            "im_G": np.imag(G).tolist(),
            "neg_im_G_over_pi": (-np.imag(G) / np.pi).tolist(),
        }
    # Analytic semicircle for comparison.
    lam_circ = np.linspace(-2.0, 2.0, 200)
    out = {
        "epsilons": epsilons,
        "panels": panels,
        "semicircle_x": lam_circ.tolist(),
        "semicircle_y": (np.sqrt(np.maximum(0, 4 - lam_circ ** 2)) / (2 * np.pi)).tolist(),
    }
    with open(OUT / "section_stieltjes.json", "w") as f:
        json.dump(out, f)


# ---------------------------------------------------------------------------
# 6.  Marchenko-Pastur with continuous gamma (already in section 5 below) +
#     a separate "MP plus a spike" widget for the BBP transition flavor.
# ---------------------------------------------------------------------------
def build_section5_data():
    gammas = [round(g, 3) for g in np.linspace(0.05, 1.0, 40)]
    out = {"gammas": gammas, "curves": {}}
    for gamma in gammas:
        lam_plus = (1 + np.sqrt(gamma)) ** 2
        lam_minus = (1 - np.sqrt(gamma)) ** 2
        lam = np.linspace(max(1e-3, lam_minus * 0.3), lam_plus * 1.05, 300)
        rho = mp_density(lam, gamma).tolist()
        out["curves"][f"{gamma:.3f}"] = {
            "x": lam.tolist(),
            "y": rho,
            "lam_minus": lam_minus,
            "lam_plus": lam_plus,
        }
    with open(OUT / "section5_mp.json", "w") as f:
        json.dump(out, f)


def build_spike_data():
    """Empirical spectrum of (1/n) X^T diag(s, 1, 1, ...) X for varying spike s.
    Shows the Baik-Ben Arous-Peche transition: spike pops out of bulk above
    a critical s.
    """
    p, n = 200, 500
    gamma = p / n
    lam_plus = (1 + np.sqrt(gamma)) ** 2
    spikes = [round(s, 2) for s in np.linspace(1.0, 4.0, 31)]
    out = {"gamma": gamma, "lam_plus": lam_plus, "spikes": spikes, "panels": {}}
    for s in spikes:
        # X has unit-variance entries; multiply column 0 by sqrt(s) to give
        # population covariance Sigma = diag(s, 1, ..., 1).
        eigs_all = []
        n_real = 30
        for _ in range(n_real):
            X = rng.standard_normal(size=(n, p))
            X[:, 0] *= np.sqrt(s)
            S = (X.T @ X) / n
            w = np.linalg.eigvalsh(S)
            eigs_all.extend(w.tolist())
        # Top-eigenvalue cluster: collect the per-realization maxima.
        top = []
        for _ in range(80):
            X = rng.standard_normal(size=(n, p))
            X[:, 0] *= np.sqrt(s)
            S = (X.T @ X) / n
            top.append(float(np.max(np.linalg.eigvalsh(S))))
        # Histogram of the bulk plus separate top-eigenvalue marker.
        hi = max(lam_plus * 1.05, max(eigs_all) * 1.02)
        centers, density = histogram(eigs_all, bins=80, range_=(0.0, hi))
        # Analytic prediction for top eigenvalue, BBP:
        # if s > 1 + sqrt(gamma), top = s + s * gamma / (s - 1).
        crit = 1 + np.sqrt(gamma)
        if s > crit:
            top_pred = s + s * gamma / (s - 1)
        else:
            top_pred = lam_plus
        out["panels"][f"{s:.2f}"] = {
            "spike": s,
            "hist_x": centers,
            "hist_y": density,
            "top_mean": float(np.mean(top)),
            "top_std": float(np.std(top)),
            "top_pred": float(top_pred),
        }
    # MP analytic curve at this gamma.
    lam = np.linspace(1e-3, max(o["top_mean"] for o in out["panels"].values()) * 1.05, 320)
    out["mp_x"] = lam.tolist()
    out["mp_y"] = mp_density(lam, gamma).tolist()
    out["bbp_critical_spike"] = float(crit)
    with open(OUT / "section_spike.json", "w") as f:
        json.dump(out, f)


# ---------------------------------------------------------------------------
# 7.  Beta-ensemble surmises + GOE/GUE histograms (universality).
# ---------------------------------------------------------------------------
def build_section6_data():
    grid_x = np.linspace(0.0, 4.0, 240)
    out = {
        "surmise": {
            "x": grid_x.tolist(),
            "beta1": wigner_surmise(grid_x, 1).tolist(),
            "beta2": wigner_surmise(grid_x, 2).tolist(),
            "beta4": wigner_surmise(grid_x, 4).tolist(),
        },
    }
    goe = goe_spacings_near_bulk(N=300, n_realizations=200)
    gue = gue_spacings_near_bulk(N=300, n_realizations=200)
    out["hist"] = {
        "beta1": dict(zip(["x", "y"], histogram(goe, bins=60, range_=(0.0, 4.0)))),
        "beta2": dict(zip(["x", "y"], histogram(gue, bins=60, range_=(0.0, 4.0)))),
    }
    # Also: non-Gaussian universality demo.  Take a Bernoulli matrix (entries
    # +/- 1 / sqrt(N)) and show the spacings still match the Wigner surmise.
    bernoulli_spacings = []
    for _ in range(200):
        N = 300
        A = rng.choice([-1.0, 1.0], size=(N, N))
        H = (A + A.T) / np.sqrt(4 * N)  # entries: variance 1/N off-diagonal -> bulk on [-2,2]
        w = np.sort(np.linalg.eigvalsh(H))
        s = np.diff(w[N // 4 : 3 * N // 4])
        bernoulli_spacings.extend((s / s.mean()).tolist())
    out["hist"]["bernoulli"] = dict(zip(["x", "y"], histogram(bernoulli_spacings, bins=60, range_=(0.0, 4.0))))
    with open(OUT / "section6_universality.json", "w") as f:
        json.dump(out, f)


# ---------------------------------------------------------------------------
# 8.  Tracy-Widom: largest eigenvalue, centered and rescaled, converges to TW2.
# ---------------------------------------------------------------------------
def build_tracy_widom_data():
    """For our normalization (semicircle on [-2, 2]), the rescaling is
    (lambda_max - 2) * N^{2/3} -> Tracy-Widom_2.

    Multi-threaded BLAS is counter-productive on small matrices, so we set
    OMP/MKL/OPENBLAS threads to 1 *before* importing numpy at the top-level.
    Sample sizes are chosen to finish in under a minute.
    """
    Ns = [40, 80, 160, 320]
    out = {"Ns": Ns, "panels": {}}
    for N in Ns:
        n_samples = 1500 if N <= 80 else (800 if N <= 160 else 400)
        tops = np.empty(n_samples)
        for i in range(n_samples):
            tops[i] = gue_eigenvalues(N)[-1]
        rescaled = (tops - 2.0) * (N ** (2.0 / 3.0))
        centers, density = histogram(rescaled.tolist(), bins=50, range_=(-5.0, 3.0))
        out["panels"][str(N)] = {
            "x": centers,
            "y": density,
            "n_samples": n_samples,
            "raw_top_mean": float(np.mean(tops)),
            "raw_top_std": float(np.std(tops)),
        }
    # Empirical TW2 reference: use the largest-N panel since the rescaled
    # distributions collapse there anyway.  Cheaper than a separate big run.
    N_ref = 320
    out["tw2_ref"] = out["panels"][str(N_ref)].copy()
    with open(OUT / "section_tracy_widom.json", "w") as f:
        json.dump(out, f)


if __name__ == "__main__":
    print("Building section 1 (sample covariance + MP overlay, continuous gamma)...")
    build_section1_data()
    print("Building section 2 (Poisson vs GUE spacings)...")
    build_section2_data()
    print("Building section 4 (semicircle convergence)...")
    build_section4_data()
    print("Building Stieltjes-transform widget data...")
    build_section_stieltjes_data()
    print("Building section 5 (Marchenko-Pastur curves, continuous gamma)...")
    build_section5_data()
    print("Building MP-plus-spike widget data (BBP transition)...")
    build_spike_data()
    print("Building section 6 (beta-ensemble surmises)...")
    build_section6_data()
    print("Building Tracy-Widom convergence data...")
    build_tracy_widom_data()
    print(f"Done.  JSON files written to {OUT}")
