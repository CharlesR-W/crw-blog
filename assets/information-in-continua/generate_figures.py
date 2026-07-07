from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def capacity_modes():
    rho = np.array([12.0, 5.0, 2.2, 0.9, 0.35, 0.13, 0.05, 0.018])
    P = 3.0

    inv = 1.0 / rho
    order = np.argsort(inv)
    inv_sorted = inv[order]
    tau = None
    for m in range(1, len(rho) + 1):
        candidate = (P + inv_sorted[:m].sum()) / m
        if m == len(rho) or candidate <= inv_sorted[m]:
            tau = candidate
            break
    p = np.maximum(tau - inv, 0.0)
    capacity_terms = 0.5 * np.log1p(p * rho)

    fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.5))
    i = np.arange(1, len(rho) + 1)

    ax[0].bar(i, rho, color="#2f6f9f", alpha=0.9)
    ax[0].axhline(1 / tau, color="#b33a3a", lw=2, label="water line")
    ax[0].set_title("mode quality")
    ax[0].set_xlabel("mode")
    ax[0].set_ylabel(r"$\rho_i$")
    ax[0].set_yscale("log")
    ax[0].legend(frameon=False)

    ax[1].bar(i, p, color="#5c8f3f", alpha=0.9, label="allocated power")
    ax[1].plot(i, capacity_terms, "o-", color="#6a4c93", label="capacity contribution")
    ax[1].set_title("water filling")
    ax[1].set_xlabel("mode")
    ax[1].set_ylabel("power / nats")
    ax[1].legend(frameon=False)

    fig.suptitle("Schematic RKHS channel capacity", y=1.04)
    save(fig, "iic_I_capacity_modes.png")


def bounded_belief_projection():
    x = np.linspace(-np.pi, np.pi, 700)
    prior = np.ones_like(x) / (2 * np.pi)
    likelihood = np.exp(-0.5 * ((x - 1.15) / 0.42) ** 2)
    likelihood += 0.55 * np.exp(-0.5 * ((x + 1.55) / 0.26) ** 2)
    posterior = prior * likelihood
    posterior /= np.trapezoid(posterior, x)

    coeff = np.fft.rfft(posterior)
    recon = {}
    for r in [1, 3, 8]:
        c = coeff.copy()
        c[r + 1 :] = 0
        y = np.fft.irfft(c, n=len(x))
        y = np.maximum(y, 0)
        y /= np.trapezoid(y, x)
        recon[r] = y

    fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.5))
    ax[0].plot(x, likelihood / likelihood.max(), color="#2f6f9f", label="evidence")
    ax[0].plot(x, posterior / posterior.max(), color="#111111", label="exact posterior")
    ax[0].set_title("tilt by evidence")
    ax[0].set_xlabel("state")
    ax[0].set_yticks([])
    ax[0].legend(frameon=False)

    ax[1].plot(x, posterior, color="#111111", lw=2, label="exact")
    for r, color in [(1, "#9a6324"), (3, "#5c8f3f"), (8, "#6a4c93")]:
        ax[1].plot(x, recon[r], color=color, label=f"{r} Fourier modes")
    ax[1].set_title("project to affordable questions")
    ax[1].set_xlabel("state")
    ax[1].set_yticks([])
    ax[1].legend(frameon=False)

    fig.suptitle("Schematic precision-bounded belief update", y=1.04)
    save(fig, "iic_II_bounded_bayes.png")


def routing_patterns():
    n = 7
    diag = np.eye(n)
    summary = np.zeros((n, n))
    summary[:, 0] = 0.55
    summary[0, :] = 0.55
    summary += 0.15 * np.eye(n)
    late = np.ones((n, n)) * 0.16
    late += 0.55 * np.eye(n)

    mats = [diag, summary, late]
    titles = ["local carry", "read into summary", "emit from summary"]

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.2), constrained_layout=True)
    for ax, mat, title in zip(axes, mats, titles):
        im = ax.imshow(mat, vmin=0, vmax=1, cmap="viridis")
        ax.set_title(title)
        ax.set_xlabel("output mode")
        ax.set_ylabel("input mode")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.colorbar(im, ax=axes, shrink=0.75, label=r"$R_{jk}$")
    fig.suptitle("Schematic routing matrices for sequential computations", y=1.05)
    save(fig, "iic_III_routing_patterns.png")


if __name__ == "__main__":
    capacity_modes()
    bounded_belief_projection()
    routing_patterns()
