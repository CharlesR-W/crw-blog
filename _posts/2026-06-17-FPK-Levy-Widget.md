---
title: "Noisy-Channel Codebooks & Lévy Noise — a Widget"
date: 2026-06-17
motivation: "Put a budget on the amplitude of a transmitted symbol and the information-optimal input stops being a smooth distribution and becomes a handful of discrete points — a codebook — for no obvious reason.  Does gradient descent find it?  And does heavy-tailed noise make the codebook sharper or blurrier?  The answers are 'no, not really' and 'it depends which question you're asking', both of which are more interesting than the guesses."
background: "Additive noise channels and mutual information.  Smith's 1971 theorem on amplitude-constrained capacity.  The Blahut-Arimoto algorithm.  α-stable laws and the fractional Laplacian as the generator of a Lévy process."
llm: "Claude"
tags: [widget, information-theory, levy-processes, stochastic-processes]
math: true
---

# Noisy-Channel Codebooks & Lévy Noise — a Widget

Send a real number $X$ across a channel that adds noise, $Y = X + \sigma N$, and ask: which input distribution $p(X)$ carries the most information, subject to a budget on how big $X$ is allowed to be?  The folklore answer for a power budget is "a Gaussian".  The answer for an *amplitude* budget is stranger — a finite set of spikes.  This widget lets you watch that codebook appear, watch gradient descent fail to quite find it, and watch heavy-tailed noise do the opposite of what you'd expect.

<iframe src="{{ '/assets/widgets/fpk-levy.html' | relative_url }}"
        style="width:100%; height:720px; border:0; border-radius:12px; background:#000;"
        loading="lazy"
        title="FPK-Lévy widget"></iframe>

Three tabs: the **noise kernels** (what α-stable noise looks like), the **optimal codebook** (the discrete constellation, and how it grows), and the **FPK relaxation** (a particle settling in a well, where heavy tails finally earn their reputation).

## The surprise: an amplitude budget forces a discrete code

The channel is $Y = X + \sigma N$.  Mutual information splits cleanly for additive noise,

$$I(X;Y) = h(Y) - h(N),$$

because the conditional $h(Y \mid X) = h(N)$ doesn't depend on the input.  So maximising information is just maximising the output entropy $h(Y)$, subject to whatever constraint we impose on $X$.

With an *average-power* budget $\mathbb{E}[X^2] \le P$ and Gaussian noise, the optimiser is the familiar Gaussian — smooth, spread out, continuous.  But Claude Shannon's student Joel Max and, definitively, **J. G. Smith (1971)** showed that under an *amplitude* budget — a peak constraint $\vert X\vert \le A$, or a mean-absolute constraint $\mathbb{E}[\vert X\vert] \le 1$ — the capacity-achieving input is **discrete, with finitely many mass points**.  Nothing in the problem mentions discreteness; it falls out of the constraint geometry.

Open the **optimal codebook** tab and drag the budget $A$.  At small $A$ the optimum is binary — two antipodal points, $\pm A$.  Push $A$ up and you get a **staircase**: a third point appears in the middle, then a fourth, then more, roughly one new level per unit of $A/\sigma$.  Hit the *rich constellation* preset to jump to a ten-point code with eight interior levels.  The red stems are the exact optimum, computed by Blahut-Arimoto (more on that in a second).

The hand-wavy reason: the output entropy wants the symbols spread as far apart as the noise can resolve, and the budget caps how far that is.  In between, putting mass at a continuum of points wastes it — once two candidate symbols are closer than the noise width they're indistinguishable, so you may as well merge them.  The optimum is the coarsest grid the noise will let you read back.  (Smith's actual proof is an analyticity argument: the optimal output density would have to be analytic with too many zeros if the support were an interval, a contradiction.)

## Does gradient descent find it?

This is the question I actually cared about.  Parametrise $p(X)$ as soft-max weights over a fine grid and run gradient *ascent* on $I(X;Y)$.  (The gradient has a tidy closed form — because the output density is one Fourier multiply, $\hat p_Y = \hat p_X \cdot \varphi_N$, the chain rule collapses to a single extra FFT, no autodiff required.)

The honest answer: **gradient descent finds the capacity but not the code.**  It climbs to within a percent or two of the true maximum, but it parks on the *wrong distribution* — it piles mass on the two extreme symbols and smears the rest into a continuous pedestal, instead of laying down clean interior atoms.

The reason is geometric, and it's a nice cautionary tale.  Near the optimum the information surface is *flat*: a whole family of distributions, including smooth ones, achieves near-capacity.  Gradient descent feels no pressure to sparsify onto the exact discrete support, because moving onto it barely changes the objective.  Discreteness is a property of the *exact* maximiser, not of every near-maximiser — and first-order methods only ever find the latter.

The clean codebook in the widget comes instead from **Blahut-Arimoto**, the standard capacity algorithm.  Its update is multiplicative,

$$p(x) \;\leftarrow\; \frac{p(x)\,\exp D(x)}{\sum_{x'} p(x')\,\exp D(x')}, \qquad D(x) = \int p(y\mid x)\,\log\frac{p(y\mid x)}{p(y)}\,dy,$$

which is a mirror-descent step in the KL geometry — and *that* geometry punishes mass on suboptimal points, so the support self-sparsifies onto the atoms.  Same optimum, different optimiser, very different idea of where to put the mass on the way there.

## Gaussian vs Lévy: the reversal

Now make the noise heavy-tailed.  α-stable noise has the characteristic function

$$\varphi_N(k) = \exp\!\big(-\vert \sigma k\vert^{\alpha}\big),$$

with $\alpha = 2$ the Gaussian and $\alpha = 1$ the Cauchy; smaller $\alpha$ means heavier tails.  The **noise kernels** tab shows them: lighter α is simultaneously more peaked in the centre *and* fatter in the tails.

Intuition says heavier tails — more outliers — should *sharpen* the codebook.  In the channel, it does the opposite.  At low SNR, Cauchy noise is so broad that it can't resolve discrete levels at all and the optimum smears back toward a continuum.  This is the **Fahs-Abou-Faycal** condition: the optimal input is discrete only when the noise log-density decays *faster* than the cost grows.  Gaussian log-density falls like $-x^2$ (fast), so an $\vert x\vert$ budget gives crisp levels; the Cauchy log-density falls like $-\log x^2$ (slow), so its overlap blurs neighbours together.  Drag α toward 1 in the codebook tab and watch the capacity readout drop — heavy tails cost bits.

At *high* SNR something subtler happens, and it's where your intuition was half-right.  Crank the budget up and Cauchy noise produces *more* atoms than Gaussian — but in a **frustrated, uneven** pattern: almost all the mass sits on the two extreme symbols, the interior atoms are tiny and irregular, and Blahut-Arimoto converges slowly there because the fixed point involves KL integrals against a heavy-tailed kernel that never quite sharpens.  Heavy tails support a richer alphabet but can't resolve its interior cleanly.

## Where Lévy noise *does* manufacture discreteness

Switch from "optimal code" to "physical relaxation" and the heavy-tail story flips back in your favour.

A particle in a confining potential $V$, kicked by α-stable noise, has a probability density obeying the **fractional Fokker-Planck equation**

$$\partial_t p = \partial_x\!\big(p\,V'(x)\big) - D\,(-\Delta)^{\alpha/2} p,$$

where the fractional Laplacian $(-\Delta)^{\alpha/2}$ — the generator of the Lévy process — is just the Fourier multiplier $\vert k\vert^{\alpha}$.  (That's the same $\varphi_N$ from the channel showing up as a diffusion operator; one Fourier engine runs the whole widget.)

In a steep, super-harmonic well $V(x) = (x/x_0)^4$, Gaussian noise ($\alpha = 2$) relaxes to the usual unimodal Boltzmann state $\propto e^{-V/D}$.  But **Lévy flights split it into a bimodal state**: a long jump overshoots the gentle centre of the well, lands out on the steep wall, and the density piles up there instead of at the bottom.  Open the **FPK relaxation** tab and watch the two panels diverge in real time — left stays a single hump, right grows two.  This is the cleanest sense in which heavy tails *create* discrete structure rather than destroying it.

## Things to play with

- **The binary-to-staircase transition.**  In the codebook tab, sweep $A$ from $0.5$ up.  Note the plateaus — the optimum stays binary over a range, then abruptly admits a third point.  Capacity is smooth even though the support count jumps.

- **Heavy tails cost bits.**  Fix a generous budget and drag α from $2$ down to $1$.  The capacity readout falls monotonically; the constellation gets denser but messier.

- **Steepness drives bimodality.**  In the FPK tab, increase the well steepness $x_0$ slider and restart.  A flatter centre gives the Lévy jumps more room to overshoot, so the bimodal split is sharper.  Near $\alpha = 2$ the split disappears — bimodality is a genuinely heavy-tailed effect.

## The one-sentence version

Discreteness shows up twice here for unrelated reasons.  In the **channel**, it comes from the amplitude budget (Smith), it's sharpest for *light*-tailed noise, and gradient descent reaches capacity without ever finding the actual code.  In the **confined diffusion**, it comes from heavy tails plus steep walls, and Lévy noise is exactly what makes it.  Same word, opposite mechanisms — which is most of the fun.

---

*Widget written with Claude.  Source: [`fpk-levy.html`]({{ '/assets/widgets/fpk-levy.html' | relative_url }}).*
