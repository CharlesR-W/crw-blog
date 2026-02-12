---
title: "Selection As Noisy Channel"
date: 2026-02-12
math: true
---

# Selection As Noisy Channel

*This work was done as part of [MATS 9.0](https://www.matsprogram.org/) under the mentorship of Richard Ngo.  This post is pedagogical; I'm collecting and reframing known results (Haldane, Fisher, Kimura, and others) in a way that I think makes the connections between them clearer.  I intend to refer to this post in later work.*

---

**BLUF**: Natural selection is a noisy channel from environment to population.  Fixing a new allele starting at frequency $p_0$ costs exactly $-\ln p_0$ nats — its surprisal.  Information gain per generation is bounded by $\frac{1}{2}\ln(1 + \text{SNR})$ nats, where the signal-to-noise ratio (SNR) is set by the effective population size $N_e$.

---

Natural selection is an optimizing process.  There's a web of results connecting it to information theory that deserves to be better known.

Three threads (for brevity, eliding some important caveats):

- [**Haldane** (1957)](https://link.springer.com/article/10.1007/BF02984069): the total 'cost' of an adaptation is its surprisal
- [**Fisher** (1930)](https://en.wikipedia.org/wiki/The_Genetical_Theory_of_Natural_Selection): the rate of adaptation is the fitness variance
- **The channel picture**: finite populations make selection a noisy channel, with capacity set by the population $N_e$

These fit together into a picture where selection has a finite, calculable throughput — and this throughput constrains what evolution can and can't do.  I'll develop the noiseless case first (Haldane, Fisher), then add the finite-population noise that makes the channel picture precise.

I'll assume you're comfortable with probability distributions and have a rough sense of KL divergence ("extra bits from using the wrong code").

## Selection is reweighting

*The one equation that defines selection: reweight by fitness, renormalize.  This is Bayes' theorem.*

Let the population have a distribution $p$ over types $i$.  Each type has fitness $w_i \geq 0$ (definitionally satisfying the equation below).  Selection produces a new generation with distribution $q$:

$$q_i = \frac{p_i \, w_i}{\bar{w}}, \qquad \bar{w} = \sum_j p_j w_j$$

"Reweight by fitness, then renormalize".  Note that in using distributions, we are tracking only type _ratios_, not the absolute population.

This is Bayes' theorem: $p$ is the prior, $w_i/\bar{w}$ is the likelihood ratio, and $q$ is the posterior.  Selection updates a population the way evidence updates a belief.  (This is also the redistribution rule for a market of Kelly bettors — wealth flows to strategies in proportion to their payoff, then renormalizes.  See Garrabrant's [Geometric Rationality](https://www.lesswrong.com/s/4hmf7rdfuXDJkxhfg) for more.)

For now, the types can be anything — organisms, hairstyles, hypotheses; but nothing that has sex (recombination breaks this simple replicator structure).  The environment has structure, reflected in $w_i$, and selection writes that structure into the population.  Actually modeling $w_i$ is tricky, so for now we will assume they are fixed and given, and we will focus on the dynamics of selection.

We will answer the following:
- What is the cost of selection?
- How long does selection take?
- Are there information-theoretic limits to how selection can act?  (yes, of course)

## The cost of a substitution

*The total cost (measured in growth shortfall) to fix a new allele is $-\ln p_0$ nats — the surprisal of its initial frequency — independent of selection strength.*

Consider a favoured allele with **selective advantage** $s$: carriers have fitness $1+s$, non-carriers have fitness 1 (so $s$ is the fractional fitness benefit, typically small).  The allele starts at population frequency $p_0$ and will eventually fix (reach frequency 1).  Write $p_t$ for its frequency in generation $t$.

While fixation is incomplete, the population pays a **genetic load** — the fractional shortfall in mean fitness relative to a population where everyone carries the favoured allele.  It's a dimensionless number between 0 and 1, measuring the fraction of potential fitness "wasted" each generation because some individuals still carry the inferior variant.  If we were tracking population, it would be the 'lost' population due to suboptimality.  With the favoured allele at frequency $p_t$, the mean fitness is $\bar{w}_t = 1 + sp_t$ while the maximum possible is $1 + s$, giving:

$$L_t = 1 -\frac{\bar{w}_t}{w_{\textrm{max}}} = \frac{s(1 - p_t)}{1 + s} \approx s(1 - p_t) \quad \text{(for small } s\text{)}$$

Large when the favoured allele is rare, zero at fixation.

Haldane's insight was to ask: what is the **total cost** — the load accumulated across all generations from initial appearance to fixation?  Again, if we were working in terms of population, it would be like the total population loss due to suboptimality.  To convert this sum over generations into an integral over frequency, we use the standard selection dynamics: under selection alone, the per-generation frequency change is $\Delta p \approx sp(1-p)$, so one generation corresponds to $dp/[sp(1-p)]$.  Substituting $L \approx s(1-p)$:

$$C = \int_{p_0}^{1}\frac{s(1-p)}{sp(1-p)}\,dp = \int_{p_0}^{1}\frac{dp}{p} = -\ln p_0$$

The $s$ cancels.  Strong selection means high load per generation but fewer generations; weak selection is the reverse.  The total depends only on initial frequency — and it's a pure number, measured in nats (natural logarithm units), interpretable as a dimensionless "information cost."

This is the **surprisal** — the same quantity that shows up in information theory as the information content of an event with probability $p_0$.  Learning that a rare event occurred (or, equivalently, driving a rare allele to fixation) costs an amount set by how improbable that starting point was.  (This is exact in the simplest genetic models; sexual reproduction and dominance effects introduce correction factors, but the key point — cost = surprisal, independent of $s$ — is robust.)

## Information per generation

*Parent and offspring distributions differ by $D_{\textrm{KL}}(q\|p)$ per generation.*

How much information does one round of selection extract?  The KL divergence from post- to pre-selection (q, and p, resp.):

$$D_{\text{KL}}(q \| p) = \sum_i q_i \ln\frac{q_i}{p_i} = \mathbb{E}_q[\ln w] - \ln\bar{w}$$

Always non-negative, zero when all fitnesses are equal — nats of information written per generation.  (We use $D_{\text{KL}}(q \| p)$ — information gained by updating from prior $p$ to posterior $q$ — the direction measuring information gained in the update.)

Perhaps a little more enlightening, for a very weak selection ($w_i \approx 1 + s_i$, $s_i$ small), this simplifies:

$$D_{\text{KL}} \approx \tfrac{1}{2}\,\text{Var}_p(\ln w)$$

No fitness variance, no information.  More variance, more per round.  This is [Fisher's fundamental theorem (1930)](https://en.wikipedia.org/wiki/Fisher%27s_fundamental_theorem_of_natural_selection) — "the rate of increase of fitness equals the variance in fitness" — reread as an information-theoretic statement.  A subtlety: Fisher's precise claim is about the *partial* change in mean fitness due to natural selection alone, holding environment constant and excluding frequency-dependent effects.  Total mean fitness can decrease (e.g., if the environment deteriorates).  The theorem says selection's *contribution* is always non-negative and equal to the fitness variance.  (Precisely: Fisher gives $\Delta\bar{w}/\bar{w} \approx \text{Var}(\ln w)$, which is twice the per-generation KL — the factor of 2 comes directly from $D_{\text{KL}} \approx \frac{1}{2}\text{Var}(\ln w)$ in the weak-selection expansion above.  See [Frank (2012)](https://arxiv.org/abs/1211.4037), who handles the partial/total distinction carefully, for the full information-theoretic reading.)

## Selection as a noisy channel

*Finite populations add drift noise to the selection signal.  This section derives the exact noise, shows when it's well-approximated by a Gaussian channel, and identifies the capacity.*

Everything above was the infinite-population limit — deterministic selection, no noise.  Real populations are finite, and the reach of selection thereby constrained.

### The exact picture: binomial noise

In a population of effective size $N_e$ ($N_e$ is 'effective population' seen by drift, basically shunts some complexities we don't want to care about for now to the difference between $N$ and $N_e$), selection computes ideal next-generation frequencies $q_i = p_i w_i / \bar{w}$.  But the actual next generation is formed by **sampling**: each of $N_e$ offspring independently draws its type from the distribution $q$ — individual $k$ is type $i$ with probability $q_i$, independently across all $N_e$ individuals.  (This is the 'Wright-Fisher' model.)  The realized frequencies therefore fluctuate around $q$.  This is **genetic drift**: the information-destroying noise in the selection channel.  (well, _one_ form of noise.)

For a single allele at frequency $q$, the number of copies in the next generation is drawn from a binomial distribution, so the realized frequency $\hat{q}$ has:

$$\mathbb{E}[\hat{q}] = q, \qquad \text{Var}(\hat{q}) = \frac{q(1-q)}{N_e}$$

Formulating the problem as a noisy channel is exact — below we'll introduce some pretty reasonable approximations to make things tractable.

### The channel, formally

In information-theoretic terms, the selection channel is:

- **Input**: the post-selection frequency $q = p \cdot w / \bar{w}$ (what selection prescribes)
- **Output**: the realized frequency $\hat{q}$ (what drift delivers)
- **Transition kernel**: $P(\hat{q} \mid q) = \text{Bin}(N_e, q) / N_e$

The information transmitted per generation is the mutual information $I(q;\, \hat{q})$ — how much knowing the prescribed frequency reduces uncertainty about the realized frequency.  The channel capacity is:

$$C = \max_{p(q)} I(q;\, \hat{q})$$

maximized over possible input distributions (i.e., over selection regimes).  This relationship is well-defined in great generality.  Below we'll specify to the Gaussian case to get a look-see at what a closed form would look like.

### The Gaussian approximation

The exact distribution is discrete: the count of allele copies is $k \sim \text{Bin}(N_e, q)$, so the realized frequency $\hat{q} = k/N_e$ can only take values $0, 1/N_e, 2/N_e, \ldots, 1$.  But since $\hat{q}$ is the mean of $N_e$ independent Bernoulli$(q)$ draws (each individual either carries the allele or doesn't), the central limit theorem gives us, for large $N_e$ and $q$ away from 0 and 1:

$$\hat{q} \;\approx\; \mathcal{N}\!\left(q, \;\frac{q(1-q)}{N_e}\right) \qquad \text{(Gaussian approximation to } \text{Bin}(N_e, q)/N_e\text{)}$$

This replaces the exact discrete, bounded binomial with a continuous, unbounded Gaussian.  The approximation is good when $N_e q$ and $N_e(1-q)$ are both large — the regime that matters most, since alleles at intermediate frequency in large populations carry the bulk of information transmission.  It breaks down near fixation ($q \approx 0$ or $1$), where the binomial is skewed.

Under this approximation, the channel decomposes cleanly.  The **signal** is the deterministic frequency shift imposed by selection: $\Delta p = q - p \approx sp(1-p)$ (from the selection equation in the previous section, where $s$ is the selective advantage).  The **noise** is the drift fluctuation $\hat{q} - q$, with standard deviation $\sqrt{q(1-q)/N_e}$.  The per-generation signal-to-noise ratio for a single allele is therefore of order $s\sqrt{N_e}$ — this is an *amplitude* ratio (signal divided by noise standard deviation).  The capacity formula below uses a *power* SNR, which is the square of this: $N_e \cdot \text{Var}(\ln w) \sim N_e s^2$.  In any single generation the noise can swamp the signal.  But this is Shannon's setting: what rate of *reliable* transmission does the noise permit?

### Three kinds of randomness

Biological populations have several sources of randomness playing structurally different roles in the channel.  By analogy with a communication system: there is noise at the input, during transmission, and at readout.

**Drift** (sampling noise in reproduction) is **channel noise** — noise during transmission.  The next generation is a finite sample from the ideal post-selection distribution, so the realized frequencies deviate from what selection prescribed.  Drift destroys information already in transit.  Its magnitude is set by $N_e$, and it's what gives the channel its finite capacity.

**Phenotype noise** ($V_E$) is **readout noise**.  Selection acts on phenotype, but only genotype is inherited.  Since phenotype = genotype + noise ($z = g + \epsilon$), selection can only "read" the genetic signal through a noisy phenotypic measurement.  This degrades the effective SNR — it reduces how strongly genetic fitness differences translate into frequency changes — without being channel noise in the drift sense.  (I say "phenotype noise" rather than "environmental variance" deliberately: later we'll want to model time-varying fitness landscapes, which is a different kind of environmental variation.  Just beware that 'environmental variance' is commonly used for this)

**Mutations** are **input noise** — or more precisely, they alter the input distribution.  Mutation is uniquely important: it is the only force that prevents the absorbing-state (fixation) steady state.  Without mutation, every locus eventually fixes regardless of $N_e$ — drift guarantees it.  But all three sources shape the steady-state distribution jointly: drift broadens the frequency spectrum toward the fixation boundaries, phenotype noise weakens the effective selection that would otherwise concentrate probability at the optimum, and mutation maintains standing variation by creating flux away from those boundaries.

The distinction matters because these sources respond to different parameters.  Increasing $N_e$ reduces channel noise (and sharpens the steady-state distribution around its selective peak).  Reducing $V_E$ sharpens the readout (strengthening effective selection).  Mutation rate controls the input variance and, critically, whether polymorphism persists at all.

### The mapping

The selection channel, exact and under the Gaussian approximation (with a bit of duct tape).  The main piece of duct tape: the standard capacity formula $\frac{1}{2}\ln(1 + \text{SNR})$ assumes signal-independent additive noise, but the drift variance $q(1-q)/N_e$ depends on the allele frequency $q$ itself.  The approximation is reasonable because the alleles carrying most of the information are at intermediate frequencies, where $q(1-q)$ varies slowly (it's within a factor of 2 of its maximum $1/4$ for $q \in [0.15, 0.85]$).  Near fixation the noise vanishes and the channel becomes nearly noiseless — which is actually favorable, since it means drift can't easily undo a nearly-fixed allele.

| | Selection (exact) | Gaussian approximation |
|---|---|---|
| Channel | $q \to \hat{q} \sim \text{Bin}(N_e, q)/N_e$ | $\hat{q} \approx \mathcal{N}(q,\; q(1-q)/N_e)$ |
| Signal | Selective shift $q - p$ | Power: $\text{Var}(\ln w)$ |
| Noise | $\text{Var}(\hat{q} \mid q) = q(1-q)/N_e$ | $\approx 1/N_e$ (order of magnitude) |
| SNR | — | $\approx N_e \cdot \text{Var}(\ln w)$ |
| Capacity | $\max_{p(q)} I(q;\, \hat{q})$ (no closed form) | $\frac{1}{2}\ln(1 + N_e \cdot \text{Var}(\ln w))$ nats/gen |

In the exact column, the noise variance $q(1-q)/N_e$ depends on allele frequency; $1/N_e$ is the order of magnitude.  Signal power and SNR don't decompose as cleanly for the discrete binomial, so the exact column goes directly from noise to capacity via mutual information.

The boundary between neutral and selected variation — the most important divide in population genetics — is the **SNR $\approx$ 1 threshold**.  When $N_e s \ll 1$, drift dominates and selection can't resolve the fitness difference.  When $N_e s \gg 1$, the signal gets through.  The classical criterion $N_e s \approx 1$ is the channel's noise floor.

This also connects back to Haldane.  The channel capacity bounds the throughput in nats per generation; Haldane's cost gives the price per substitution ($-\ln p_0$ nats).  Together: the maximum rate of adaptive substitution $\approx$ capacity $/ (-\ln p_0)$.  You can't fix alleles faster than the channel allows.

## Why Gaussian — and why you can predict the width

*Under stabilizing selection, the channel argument predicts not just the shape of trait distributions but their equilibrium variance.*

Most complex traits sit under **stabilizing selection**: there's an optimal value $z^*$, and fitness falls off for deviations from it.  Near the optimum, the fitness function is well-approximated by a quadratic penalty:

$$\ln w(z) \approx \text{const} - \frac{H}{2}(z - z^*)^2$$

where $H$ measures the curvature of the fitness landscape (stronger stabilizing selection = larger $H$).  This quadratic log-fitness is precisely a Gaussian channel: the "noise" from environmental variance and drift is additive, and the penalty for deviating from the optimum is quadratic in the deviation.

For Gaussian channels, information theory tells us the capacity-achieving input distribution is Gaussian.  So the CLT gives you the *mechanism* (many small genetic contributions sum to a Gaussian), and the channel argument gives you the *optimality condition* (a Gaussian input distribution maximizes the information selection extracts per generation).  Populations under stabilizing selection converge to the distribution that makes best use of the available channel capacity.

The punchline is that the argument predicts the **width**, not just the shape.  Every generation, mutation injects new genetic variance at rate $V_m$ (the mutational variance).  Stabilizing selection removes variance — alleles far from the optimum are selected against.  At equilibrium, input balances removal.  [Lande (1975)](https://www.cambridge.org/core/journals/genetics-research/article/maintenance-of-genetic-variability-by-mutation-in-a-polygenic-character-with-linked-loci/D12E61BA54B9B4BE2480C13E15757432) showed the equilibrium genetic variance is:

$$V_G \approx \sqrt{V_m / H}$$

Here $V_G$ is the total genetic variance of the trait (summed across loci), $V_m$ is the total per-generation mutational variance, and $H$ is the curvature of the fitness landscape.  Tighter stabilizing selection (larger $H$) or lower mutational input (smaller $V_m$) means a narrower trait distribution.  This is a quantitative, testable prediction — but it's sensitive to assumptions about the distribution of mutational effect sizes.  Lande's result assumes a Gaussian model where each mutation has a small effect.  [Turelli (1984)](https://doi.org/10.1016/0040-5809(84)90006-X) showed that under a "house of cards" approximation — where each mutation's phenotypic effect is large relative to standing variation — the equilibrium shifts to $V_G \propto V_m$ instead.  Real populations likely live somewhere between these regimes, so the square-root scaling is a useful benchmark rather than a universal law.

One qualifier: this is the equilibrium result under stabilizing selection.  Directional selection — where the optimum is shifting — is a different regime with different dynamics, and is the setting where the channel capacity bound on adaptation rate bites hardest.

## Consequences

The channel picture gives population genetics a budget.  $N_e$ sets the bandwidth; everything else follows from how that bandwidth is spent.

**Most variation is neutral — forced by the throughput limit.**  This is [Kimura's neutral theory (1968)](https://www.nature.com/articles/217624a0), and the channel argument shows it's a consequence of the capacity bound — not just an empirical observation, but forced by the throughput limit.  The channel capacity bounds the rate of adaptive substitution; Haldane's cost sets the price per substitution.  Together they imply that selection can only act on a small fraction of loci at once.  Most variation *must* drift neutrally — there isn't enough bandwidth.  Kimura was originally motivated by Haldane's cost calculation: the observed rate of molecular substitution in mammals (~1 substitution per 300 generations; [Kimura 1968](https://www.nature.com/articles/217624a0)) seemed too high for all substitutions to be adaptive, given the genetic load each one imposes ([Haldane 1957](https://link.springer.com/article/10.1007/BF02984069)).  A further prediction: neutral substitutions accumulate at a rate equal to the per-individual per-generation mutation rate $\mu$, independent of population size — a population produces $2N\mu$ new neutral mutations per generation, each fixing with probability $1/(2N)$, giving a substitution rate of $\mu$.  The $N$ cancels.  This is the molecular clock, derived from neutral theory and broadly confirmed.

**Most of the bandwidth goes to maintenance.**  Most mutations are deleterious, and most of what selection actually does is remove them — Miller's "black rain" of mutation constantly degrading the genome, with purifying selection constantly bailing it out.  The channel capacity that remains for *adaptive* innovation is what's left after this upkeep.  (Miller's [*The Mating Mind* (2000)](https://en.wikipedia.org/wiki/The_Mating_Mind) is the best popular treatment of what this implies.  Its thesis about sexual selection is self-admittedly speculative, but the underlying model of how mutation load, purifying selection, and honest signaling fit together is carefully argued and genuinely illuminating.  See also Malmesbury's [The Talk](https://www.lesswrong.com/posts/yA8DWsHJeFZhDcQuo/the-talk-a-brief-explanation-of-sexual-dimorphism) on LessWrong for a concise version.)

## Where Next?

My ultimate interest is in neural networks - so whither Darwin?  I am exploring a selectionist theory of how structured computation arises when learners are trained on structured data.  I have two lines of thinking here:
1. Robustness to 'noise' should encourage 'modularity', and for different noise models, we should be able to estimate an 'effective loss' which encourages modularity.  This is the justification for why we add regularizers to our loss, but hopefully from a more top-down perspective.
2. Circuits arise out of competition between multiple contemporary circuits with different generalization properties - as data comes in, the poor-generalizers are 'outcompeted'.  [Ahuja et al. (2024)](https://arxiv.org/abs/2404.16367) find this occurs in transformers trained on synthetic grammars.

The relation to alignment is twofold - one, I want an account of how structured _data_ induces structured _computation_ in a learner, and for the moment this seems a promising way to reason about this.  Ideally this would let us predict _how structured_ a network should be.  Two, much more speculatively, I think that _hierarchical_ selection (e.g., selection over circuits-of-circuits) might be a good way to think about 'higher levels of organization' in neural networks.

I'm still working out the math, and the best way to correspond the selection picture to the traditional SGD picture.

**Further reading:** Steven Frank's [*Natural Selection*](https://stevefrank.org/natsel/natsel.html) series develops many of these information-theoretic connections with more depth and rigor than I have here.  I haven't read it thoroughly, but from what I've seen it covers similar ground from the perspective of someone who has spent decades on this — worth checking out if this post resonated.

---

*Written with help from Claude.*
