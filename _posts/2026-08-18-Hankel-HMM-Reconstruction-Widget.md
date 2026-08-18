---
title: "How Hankel Matrices Reconstruct Hidden Dynamics — a Widget"
date: 2026-08-18
motivation: "An HMM is a story about hidden states. A Hankel matrix starts from the opposite end: observable probabilities of past-plus-future strings. Its rank tells you how many linear predictive coordinates the process needs, and shifted Hankel blocks tell you how those coordinates update when a new symbol arrives. This widget makes the whole route visible at once — including the point where a reconstructed linear machine is not automatically a stochastic HMM."
background: "Edge-emitting hidden Markov models, word probabilities, singular value decomposition, predictive state representations, and weighted finite automata."
llm: "Codex"
tags: [widget, hidden-markov-models, spectral-learning, computational-mechanics]
math: true
---

# How Hankel Matrices Reconstruct Hidden Dynamics

Pick a generator and then pretend you cannot see it. All you get is a stream of symbols. The widget builds a table of past–future probabilities, reads its singular spectrum, and constructs rank-$r$ predictive machines. Switch from exact probabilities to a finite sample and watch the clean rank cutoff become a noisy elbow.

<iframe id="hankel-hmm-widget"
        src="{{ '/assets/widgets/hankel-hmm.html' | relative_url }}"
        style="width:100%; height:1030px; border:0; border-radius:12px; background:#000;"
        loading="lazy"
        title="Hankel reconstruction of hidden dynamics"></iframe>
<script>
function resizeHankelWidget() {
  var frame = document.getElementById('hankel-hmm-widget');
  if (!frame || !frame.contentWindow) return;
  try {
    frame.style.height = Math.max(900, frame.contentWindow.document.documentElement.scrollHeight + 4) + 'px';
  } catch (_) {}
}
window.addEventListener('message', function (event) {
  if (!event.data || event.data.type !== 'hankel-widget-height') return;
  var frame = document.getElementById('hankel-hmm-widget');
  if (frame && Number.isFinite(event.data.height)) {
    frame.style.height = Math.max(900, event.data.height + 4) + 'px';
  }
});
var hankelFrame = document.getElementById('hankel-hmm-widget');
if (hankelFrame) {
  hankelFrame.addEventListener('load', function () {
    resizeHankelWidget();
    window.setTimeout(resizeHankelWidget, 200);
    window.setTimeout(resizeHankelWidget, 800);
  });
}
window.addEventListener('resize', resizeHankelWidget);
</script>

The four numbered columns are the whole argument. The rest of this post walks back through them with the algebra visible.

## 1. An HMM turns every word into a matrix product

Use an edge-emitting HMM with hidden states $S_1,\ldots,S_m$. For each visible symbol $x$, let

$$
T^{(x)}_{ij}
=
\Pr(X_{t+1}=x,S_{t+1}=S_j\mid S_t=S_i).
$$

The matrices $T^{(x)}$ are not individually stochastic. Their sum over symbols is the ordinary hidden-state transition matrix, so

$$
\sum_x T^{(x)}\mathbf 1=\mathbf 1.
$$

If $w=x_1\cdots x_k$, write $T^{(w)}=T^{(x_1)}\cdots T^{(x_k)}$. Starting from a stationary row vector $\pi$, the probability of observing $w$ is

$$
\boxed{\Pr(w)=\pi T^{(w)}\mathbf 1.}
$$

That is everything the learner is allowed to measure. The hidden-state labels, the graph, and the matrices generating the stream are unavailable. The widget leaves the true graph visible because this is a toy and we want to know whether reconstruction worked; in an actual inference problem the first panel would be covered with a large black rectangle.

## 2. Put every past beside every possible future

Let $p$ be a history and $s$ a future test. The process Hankel matrix is

$$
H_{p,s}=\Pr(ps).
$$

Rows are histories; columns are questions about the future. The empty word $\epsilon$ is included on both axes, so $H_{p,\epsilon}=\Pr(p)$ and $H_{\epsilon,s}=\Pr(s)$.

Now insert the HMM word formula and split at the boundary between past and future:

$$
H_{p,s}
=
\underbrace{\pi T^{(p)}}_{\phi(p)}
\underbrace{T^{(s)}\mathbf 1}_{\psi(s)}.
$$

Stack every $\phi(p)$ as a row of a matrix $\Phi$ and every $\psi(s)$ as a column of a matrix $\Psi$. Then

$$
\boxed{H=\Phi\Psi,\qquad \operatorname{rank}(H)\le m.}
$$

The hidden model has compressed every distinction among arbitrarily long histories through an $m$-dimensional boundary state. The Hankel matrix detects that compression without seeing the boundary state.

There is a logical wrinkle which is easy to miss. A finite block of $H$ can prove a **lower bound** on the full rank: any independent rows or columns in the block remain independent in the infinite matrix. It does not, by itself, prove an upper bound. In this widget we know the toy generator is a finite HMM, so its number of hidden states supplies the missing upper bound. With an unknown real process, a larger block can always reveal a direction the smaller block missed.

## 3. The spectrum tells you which predictive directions survive

For a finite observed block, take the singular value decomposition

$$
H=U\Sigma V^\top.
$$

If the exact **population** process has rank $r_\star$, only the first $r_\star$ singular values are nonzero. A finite stream gives an estimate

$$
\widehat H=H+E,
$$

where $E$ is sampling error. A generic perturbation has components in every singular direction, so $\widehat H$ will usually have rank well above the population rank—and is often full rank—even when $H$ has rank two. This is a mathematical fact, not evidence that the finite sample secretly came from a higher-state process. Weyl's inequality gives the useful scale:

$$
\left|\sigma_i(\widehat H)-\sigma_i(H)\right|\leq \lVert E\rVert_2.
$$

The zero population tail therefore becomes a small empirical noise floor. The revised spectrum plots $\sigma_i/\sigma_1$ on a labelled log axis, overlays the exact population spectrum because this is a toy, and reports both the first tail ratio and the fraction of squared spectral energy in the entire tail. The sample matrix's raw numerical rank is deliberately shown too—but it is a diagnostic of finite precision and sampling, not an estimator of process dimension. Choosing $r$ means locating a stable signal–noise separation, ideally with held-out prediction or repeated samples, rather than counting every nonzero singular value.

The rank-$r$ truncated SVD is

$$
H_r=U_r\Sigma_rV_r^\top.
$$

For this **finite matrix**, Eckart–Young tells us that $H_r$ is the best rank-$r$ approximation in both Frobenius and spectral norm. The dashboard's purple curve is

$$
E_H(r)=\frac{\lVert H-H_r\rVert_F}{\lVert H\rVert_F}.
$$

So: is there a special “Hankel error”? Sorta, but the noun is overloaded.

- A finite Hankel **block** has ordinary matrix norms. The Frobenius residual above adds the squared discarded singular values; the spectral-norm residual is exactly $\sigma_{r+1}$.
- In linear control, the **Hankel norm** normally means the operator norm of the past-to-future Hankel operator. That will be the natural quantity in the continuous-space control version of this widget.
- Neither one is the same as $L_1$, $L_2$, or KL error between predicted word distributions. Those ask whether the reconstructed process predicts the right observable strings, not merely whether it fits this particular matrix block.

The error column therefore keeps four small multiples on separate vertical scales. The first three compare length-six word distributions against the known toy truth. The fourth measures fit to the observed Hankel block. In the finite-sample setting, keep increasing $r$: the purple training residual must fall, while the out-of-sample word errors can flatten or rise. Hello, overfitting. Nice to see you somewhere this small.

A low-rank linear machine can assign negative weight to a word. To make KL defined, the widget clips negative entries in the evaluated length-six vector and renormalizes it; $L_1$ and $L_2$ use that same corrected vector. The selected-rank readout tells you when clipping was needed. This is an evaluation convention, not a proof that the machine is globally stochastic.

## 4. Shift the Hankel matrix to recover dynamics

Rank gives a state-space dimension, but a state without an update rule is not much of a state. For each symbol $x$, construct a shifted block

$$
H_x[p,s]=\Pr(pxs).
$$

Using the same singular subspaces as $H$, define

$$
A_x
=
\Sigma_r^{-1/2}U_r^\top H_xV_r\Sigma_r^{-1/2},
$$

with boundary vectors

$$
\alpha^\top=e_\epsilon^\top U_r\Sigma_r^{1/2},
\qquad
\beta=\Sigma_r^{1/2}V_r^\top e_\epsilon.
$$

Then the reconstructed probability of a word is

$$
\widehat{\Pr}(x_1\cdots x_k)
=
\alpha^\top A_{x_1}\cdots A_{x_k}\beta.
$$

The four little network diagrams in the third dashboard column show these symbol-labelled operators. Line colour identifies the observed symbol; thickness is operator magnitude; dashed edges are negative entries. Click a rank in the spectrum, reconstruction cards, or error plots and the same $r$ is highlighted everywhere.

At the correct rank and with exact probabilities, this linear machine reproduces the toy process. It need not reproduce the original hidden-state coordinates. If $G$ is invertible, the change of basis

$$
\alpha^\top\mapsto\alpha^\top G,
\qquad
A_x\mapsto G^{-1}A_xG,
\qquad
\beta\mapsto G^{-1}\beta
$$

leaves every word probability unchanged. Observable dynamics are identifiable before a preferred latent basis is.

## The mildly annoying final caveat

A finite-rank Hankel matrix guarantees a finite-dimensional **linear realization** — equivalently, a weighted finite automaton or predictive-state representation. It does not automatically guarantee a same-sized realization whose entries are all nonnegative and whose outgoing probabilities sum to one.

That is why the dashboard says “predictive machines,” not “we recovered the one true hidden graph.” An actual HMM is a **positive realization** of the observable process. Finding one imposes additional nonnegativity and stochasticity constraints, and it may need more states than the ordinary real-valued Hankel rank. Even when a minimal HMM exists, hidden-state permutations and redundant realizations prevent the original internal story from being uniquely determined by observations alone.

This is not a failure of the Hankel construction. It is the useful answer:

$$
\boxed{\text{Hankel rank recovers minimal linear predictive memory, not privileged hidden ontology.}}
$$

The true HMM in the first panel proves an upper bound. The observed Hankel block supplies a lower bound. When they meet, we know the predictive dimension exactly. Please clap.

## Things to try

- Start with **Zero-One-Random** and exact probabilities. The spectrum has three live directions. Rank two underfits; rank three closes the observable error; higher ranks add nothing.
- Switch to **2,500 symbols**. The tail no longer vanishes. Watch the Hankel residual continue downward after the true rank while KL does not receive the same guaranteed improvement.
- Jump from **50,000 symbols** back to **2,500**. This is the bias–variance tradeoff with nowhere to hide: same generator, same finite block, different amount of evidence.
- Compare **Golden Mean** and **Mess3**. Golden Mean needs two linear directions. Mess3 needs three, even though its conditional belief states range over a much richer set than three discrete predictive classes. Rank is the dimension of a linear span, not generally the number of predictive states.

---

*Widget and walkthrough built with Codex. Source: [`hankel-hmm.html`]({{ '/assets/widgets/hankel-hmm.html' | relative_url }}); deterministic builder: [`build.py`]({{ '/assets/widgets/hankel-hmm-src/build.py' | relative_url }}).*
