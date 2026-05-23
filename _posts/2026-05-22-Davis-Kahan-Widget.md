---
title: "Davis-Kahan sin θ — an Eigengap Widget"
date: 2026-05-22
motivation: "Spectral algorithms (PCA, spectral clustering, network embeddings) ultimately care about eigenvectors of a noisy estimate of some clean matrix.  Why does a big eigengap make those eigenvectors stable?  The bound is one line; the geometric reason is one picture."
background: "Symmetric perturbation theory.  The Rayleigh quotient as a height function on the unit sphere.  Eigenvalue gap as Hessian curvature at a constrained optimum."
llm: "Claude"
tags: [widget, linear-algebra, spectral-theory]
math: true
---

# Davis-Kahan sin θ — an Eigengap Widget

Drag the orange handle to steer the perturbation; pull the sliders to make the eigengap small.  Watch the blue eigenvector arm rotate away from the grey one, and watch the Davis-Kahan bound $\lVert E \rVert / \delta$ track the rotation.

<iframe src="{{ '/assets/widgets/davis-kahan.html' | relative_url }}"
        style="width:100%; height:780px; border:0; border-radius:12px; background:#000;"
        loading="lazy"
        title="Davis-Kahan widget"></iframe>

## What the theorem says

Let $A$ be a symmetric matrix with eigenvalues $\lambda_1 \ge \lambda_2 \ge \cdots$ and corresponding eigenvectors $v_1, v_2, \ldots$  Perturb it by a symmetric $E$ of operator norm $\lVert E \rVert$, and let $v_1'$ be the top eigenvector of $A + E$.  Define the eigengap

$$\delta = \lambda_1 - \lambda_2.$$

Then the angle $\theta$ between $v_1$ and $v_1'$ satisfies

$$\sin \theta \;\le\; \frac{\lVert E \rVert}{\delta}.$$

That is the simplest form of the Davis-Kahan sin θ theorem.  The general version replaces "top eigenvector" with "eigenspace of a chosen group of eigenvalues" and $\theta$ with the largest principal angle between the unperturbed and perturbed eigenspaces; the gap $\delta$ is then the distance from the chosen group to the rest of the spectrum.

So the rule is: **eigenvectors are stable to the extent that their eigenvalues are isolated.**  Eigenvalues that crowd together share an unstable eigenspace.

## Why?  The Rayleigh quotient landscape

The reason becomes vivid if you stop thinking of eigenvectors algebraically and start thinking of them as **optima of a height function**.

For a symmetric $A$, the Rayleigh quotient

$$R_A(v) = \frac{v^\top A v}{v^\top v}$$

is a smooth function on the unit sphere.  Its critical points are exactly the eigenvectors of $A$, and the critical values are the eigenvalues.  The top eigenvector $v_1$ is the global maximum, with value $\lambda_1$.

Now do a Taylor expansion of $R_A$ at $v_1$.  Move along the unit sphere a small amount in the direction of another eigenvector $v_j$ (write $v(\epsilon) = \cos(\epsilon) v_1 + \sin(\epsilon) v_j$).  Then

$$R_A(v(\epsilon)) = \lambda_1 - \tfrac{1}{2} \cdot 2(\lambda_1 - \lambda_j) \cdot \epsilon^2 + O(\epsilon^4).$$

The coefficient of $\epsilon^2/2$ — the *curvature* of $R_A$ at $v_1$ along the $v_j$ direction — is exactly $2(\lambda_1 - \lambda_j)$.  For the worst-case direction this is $2\delta$.

**The eigenvalue gap is literally the stiffness of the eigenvector.**

This is the whole game.  Replacing $A$ by $A + E$ adds a perturbation to the height function:

$$R_{A+E}(v) = R_A(v) + v^\top E v.$$

The new term $v^\top E v$ has magnitude at most $\lVert E \rVert$ and a smoothly varying gradient.  So the perturbed landscape is the old landscape plus a gentle tilt of size $\lVert E \rVert$.

In a quadratic well of curvature $\kappa$, a tilt of magnitude $g$ shifts the minimum by $g / \kappa$.  Here $g \sim \lVert E \rVert$ and $\kappa \sim \delta$, so the optimum moves by $\sim \lVert E \rVert / \delta$, which (for small angles) is exactly $\sin \theta$.

That is Davis-Kahan, with no inequalities, no projections, no traces.  Just: shallow wells let the ball roll farther.

***

The left panel of the widget is that height function explicitly: $R(v(\theta))$ as a function of the angle $\theta$ that picks out a direction on the unit circle.  Grey is $R_A$, blue is $R_{A+E}$.  The maxima are eigenvectors.  The red dashed parabola is the second-order Taylor approximation at the perturbed peak, whose width *is* the gap.  Push the eigenvalues together (shrink $\delta$) and watch the peak flatten — and the perturbed max slide far from the unperturbed one.

The right panel is the same story in $\mathbb{R}^2$: original eigenvector in grey, perturbed in blue, red wedge their angle.  The dashed yellow arc is the Davis-Kahan bound — the perturbed eigenvector is guaranteed to stay within it.

## Things to play with

- **Tight gap, small perturbation.**  Set $\lambda_1 = 1$, $\lambda_2 = 0.95$, $\lVert E \rVert = 0.05$.  A perturbation that is tiny in absolute terms causes a rotation of more than 45°.  The bound is $1.0$ — it has run out of headroom.

- **Sweep the perturbation direction.**  Hit "animate φ".  The actual sin θ traces out a sinusoid; the worst-case direction is $\varphi = \pm 45°$ (purely off-diagonal in the eigenbasis of $A$), where the bound is tight.  At $\varphi = 0$ the perturbation is parallel to $A$ — it changes the eigenvalues but leaves the eigenvectors fixed, so sin θ collapses to zero.

- **Eigenvalue crossing.**  Drag $\lambda_2$ up past $\lambda_1$ with the perturbation nonzero.  The blue eigenvector swings through 90° as the gap closes and reopens with reversed sign.  This is the spectral analogue of avoided crossings in quantum mechanics.

- **Trace the cloud.**  Toggle "trace" and start dragging the orange handle around.  The blue dots paint out the locus of perturbed eigenvectors over all perturbation directions; the cloud is an arc whose half-width is $\arcsin(\lVert E \rVert / \delta)$ — the Davis-Kahan envelope.

## Why this shows up in practice

Wherever you compute eigenvectors of a noisy estimator and *use* those eigenvectors downstream, Davis-Kahan tells you whether you should trust the answer.

- **PCA.**  The principal components of an empirical covariance $\hat{\Sigma} = \Sigma + E$ are stable to the extent that the true eigenvalues are spread out.  A spiked-covariance population with one strong direction has stable PC1 — but PC2 vs PC3 may be a coin flip if their true eigenvalues are close.

- **Spectral clustering.**  The cluster indicators live in the eigenspace of the smallest non-trivial eigenvalues of the Laplacian.  A well-separated cluster structure means a big spectral gap (between the bottom-$k$ and the rest), which means stable cluster recovery.  Cheeger-type results are the qualitative cousin.

- **Network embeddings, Laplacian eigenmaps, diffusion maps.**  Same story.  The embedding is the eigenvector basis; the bound tells you how much the embedding can rotate when you re-estimate with new data.

- **Random matrix theory.**  In Wigner / Marchenko-Pastur asymptotics, individual eigenvectors in the bulk are *not* localized because gaps are $O(1/N)$ — vanishing eigengap means infinite Davis-Kahan ratio means random eigenvector directions, even with fixed perturbation strength.  Eigenvectors at the spectral edge are different: gaps there scale better, so edge eigenvectors are recoverable.

## Caveats and extensions

The bound above is for the *top* eigenvector and uses the gap to the next eigenvalue.  For a $k$-dimensional invariant subspace, the natural generalization uses the gap between $\lambda_k$ and $\lambda_{k+1}$, and "angle" becomes the largest principal angle between the unperturbed and perturbed $k$-dimensional subspaces.  Same shape of bound, same intuition.

The theorem is sharp for symmetric matrices and worst-case perturbations.  For *non*-symmetric or non-normal matrices the story is much worse: pseudospectra can be huge even when the spectrum is well-separated, and tiny perturbations can swing eigenvectors arbitrarily.  Davis-Kahan is a story about self-adjoint operators specifically — about the rigidity that comes from having a real spectrum and an orthonormal eigenbasis.

There are also tighter variants.  The Davis-Kahan-Wedin theorem extends the bound to singular vectors.  The Yu-Wang-Samworth refinement gives a Frobenius-norm version with cleaner constants for statistical applications.  And in cases where you only care about a few specific eigenvalues, you can replace $\delta$ with a *partial* gap and tighten the bound substantially.

But the core picture stays: gap = curvature, perturbation = tilt, displacement = tilt over curvature.

---

*Widget written with Claude.  Source: [`davis-kahan.html`]({{ '/assets/widgets/davis-kahan.html' | relative_url }}).*
