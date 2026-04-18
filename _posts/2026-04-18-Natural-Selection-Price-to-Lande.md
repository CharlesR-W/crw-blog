---
title: "Natural Selection: Price to Lande"
date: 2026-04-18
motivation: "Population genetics has a reputation as a thicket of folk theorems with strange names.  It's actually one theorem - the Price equation - and everything else (Fisher's fundamental theorem, the breeder's equation, Lande's multivariate response, replicator dynamics) is a specialization or reframing.  If you see the covariance, you see it all."
background: "Comfortable with basic probability (covariance, conditional expectation), some linear algebra (for the multivariate Lande), and willing to think of a population as a measure.  Genetics background not required - this is a math post that happens to be about biology."
llm: "Claude"
tags: [seed]
math: true
---

# Natural Selection: Price to Lande

## The One-Line Pitch

A population is a measure.  Selection reweights the measure by fitness.  Everything else is bookkeeping.

The bookkeeping produces, in order: the Price equation, Fisher's fundamental theorem, Haldane's cost, the breeder's equation, Lande's multivariate response, and the replicator equation as natural gradient.  They are all the same identity wearing different hats.

This is the first of two seeds.  The companion, "Natural Selection: Drift, Neutrality, and Resolution Limits", handles the finite-population stochastic story (Kimura, diffusion, drift barriers).  Here we stay in the deterministic / infinite-population limit and focus on the algebraic core.

I'm going to be cavalier about sex.  The clean statements are for asexual reproduction with faithful inheritance; sexual recombination breaks some things (transmission bias becomes nontrivial) and this post is not where I handle that.

## The Price Equation

*The one equation.  From a two-generation identity, with no assumptions about mechanism.*

### Setup

Let the parent population be a finite set indexed by $i$, with each individual $i$ having:

- a trait value $z_i$ (anything: height, allele frequency, a coin flip, whatever)
- a fitness $w_i \geq 0$ (number of offspring, or expected number)

Write $\bar{z} = \mathbb{E}[z]$ and $\bar{w} = \mathbb{E}[w]$ for population averages over parents.  The offspring of parent $i$ have mean trait value $z_i' = z_i + \Delta z_i$ where $\Delta z_i$ is the **transmission bias** - how much the offspring deviate on average from their parent.

The next generation's mean trait is
$$
\bar{z}' = \frac{1}{\sum_j w_j} \sum_i w_i z_i' = \frac{1}{\bar{w}} \mathbb{E}[w (z + \Delta z)].
$$

That's the definition.  Now just expand.

### Derivation

$$
\bar{z}' - \bar{z} = \frac{\mathbb{E}[w(z + \Delta z)]}{\bar{w}} - \bar{z} = \frac{\mathbb{E}[wz] - \bar{w}\bar{z}}{\bar{w}} + \frac{\mathbb{E}[w \Delta z]}{\bar{w}}.
$$

The first term is $\mathrm{Cov}(w, z)/\bar{w}$ by definition of covariance.  So:

$$
\boxed{\;\Delta \bar{z} \;=\; \frac{\mathrm{Cov}(w, z)}{\bar{w}} \;+\; \frac{\mathbb{E}[w\, \Delta z]}{\bar{w}}\;}
$$

This is the **Price equation** (Price 1970, 1972).  The two terms have names.

- $\mathrm{Cov}(w, z)/\bar{w}$ is the **selection term**.  If fitter individuals have higher trait values, the population mean increases.
- $\mathbb{E}[w\, \Delta z]/\bar{w}$ is the **transmission term**.  If offspring systematically differ from their parents, that differential propagates too, weighted by parental fitness.

What's remarkable is the derivation.  I used zero assumptions about biology, genetics, or mechanism.  It's a two-line consequence of how you add fractions.  If you can count, you can derive the Price equation.  The content is all in what $z$ and $w$ actually are in a given application.

(Frank's expository papers - [Frank 2012](https://arxiv.org/abs/1211.4037) is the cleanest one I know - go into the derivation at length and discuss what "meaningful" uses of the equation look like.  The critique that it's a tautology is correct but misses the point; tautologies can be useful organizing principles.)

### Specialization: faithful inheritance, asexual

Set $\Delta z_i = 0$ for all $i$.  Offspring inherit their parent's trait exactly.  Then

$$
\Delta \bar{z} = \frac{\mathrm{Cov}(w, z)}{\bar{w}}.
$$

This is the version you'll mostly use.  Selection *is* covariance with fitness, divided by mean fitness.  Nothing else happens.

## Fisher's Fundamental Theorem

*Take $z = w$ in the Price equation.  Write the result down.  You are done.*

Set the trait to be fitness itself.  $\mathrm{Cov}(w, w) = \mathrm{Var}(w)$.  So:

$$
\Delta \bar{w} = \frac{\mathrm{Var}(w)}{\bar{w}}.
$$

The rate of change of mean fitness equals the variance in fitness, over the mean fitness.  That's Fisher's fundamental theorem (Fisher 1930).  Two lines from Price.

One subtlety.  Fisher's original statement is about the **partial** change in mean fitness due to natural selection alone, holding environment and frequency-dependent effects fixed.  The total $\Delta \bar{w}$ can decrease if the environment is changing or if fitness itself is frequency-dependent.  The clean Price derivation above sidesteps this by assuming $w_i$ is fixed (exogenous, not a function of the population), which is exactly the regime where "Fisher's fundamental theorem" is literally true.

In the quantitative-genetics version, "variance in fitness" gets refined to **additive genetic variance in fitness** $V_A(w)$, not total variance.  This matters because not all variance is heritable.  We'll see why when we do the breeder's equation below.

### The KL-divergence view

Quick connection for people who've read "Selection As Noisy Channel" (see my post of the same name for more).  Define $q_i = p_i w_i / \bar{w}$, the post-selection distribution.  Under weak selection $w_i = 1 + s_i$ with $s_i$ small,

$$
D_{\mathrm{KL}}(q \lVert p) \approx \tfrac{1}{2}\mathrm{Var}_p(\ln w) \approx \tfrac{1}{2\bar{w}^2}\mathrm{Var}(w).
$$

So Fisher's theorem says: the KL-information extracted per generation equals half the fitness variance (in the $\ln$-fitness scale).  The "rate of adaptation" is "information per generation".  One statement, two dialects.

## Haldane's Cost of Natural Selection

*Substituting a favorable allele costs exactly $-\ln p_0$ nats in accumulated fitness shortfall, regardless of selection strength.  The $s$ cancels.*

This is also covered at length in "Selection As Noisy Channel" - see that post for the full derivation.  Quick sketch for completeness.

A favored allele at frequency $p$ with selective advantage $s$ (carriers have fitness $1+s$, others $1$) imposes per-generation **genetic load**
$$
L(p) = \frac{s(1-p)}{1+s} \approx s(1-p).
$$

Under pure selection, $\dot p \approx sp(1-p)$, so one generation corresponds to $dp / [sp(1-p)]$ in frequency space.  Total accumulated load from $p_0$ to fixation:

$$
C = \int_{p_0}^{1} \frac{s(1-p)}{sp(1-p)} \, dp = \int_{p_0}^{1} \frac{dp}{p} = -\ln p_0.
$$

The $s$ cancels.  The total load is the **surprisal** of the initial frequency: fixing a rare allele is expensive precisely because it's rare, and strong selection doesn't help - it just amortizes the cost over fewer generations.

Haldane's original calculation had a practical punchline: if mammalian populations can only afford a load of $\sim 0.1$ per generation, and each substitution costs $\sim \ln(1/p_0) \sim 10$ nats (for $p_0 \sim e^{-10}$), then the maximum rate of adaptive substitution is $\sim 1$ per $100$ generations.  Observed molecular substitution rates are much higher - which is part of what drove Kimura to neutral theory.  I handle that in the companion seed.

## Breeder's Equation

*The quantitative-genetics specialization.  Phenotype = genotype + noise.  Response to selection is heritability times selection differential.*

Quantitative genetics is the regime where you don't know the underlying loci but you have trait data and pedigrees.  Decompose the phenotype:

$$
z = g + e
$$

where $g$ is the **breeding value** (the additive genetic contribution, defined below) and $e$ is everything else (dominance, environment, measurement noise), with $\mathrm{Cov}(g, e) = 0$ by construction.  Write $V_P = \mathrm{Var}(z)$, $V_A = \mathrm{Var}(g)$, $V_E = \mathrm{Var}(e) = V_P - V_A$.  The **narrow-sense heritability** is

$$
h^2 = \frac{V_A}{V_P}.
$$

Between 0 and 1.  How much of the phenotypic variance is heritable in the additive sense.

### The derivation

Let selection choose parents with mean phenotype $\bar{z}^* = \bar{z} + S$, where $S$ is the **selection differential** - the gap between the selected group's mean and the population mean.

The response $R = \bar{z}' - \bar{z}$ is what ends up in the next generation.  Assume offspring inherit the mean breeding value of their parents (standard in the additive model).  Then the offspring mean is

$$
\bar{z}' = \bar{g}^* = \bar{g} + \frac{\mathrm{Cov}(g, z)}{\mathrm{Var}(z)} \cdot S = \bar{g} + \frac{V_A}{V_P} S
$$

where I used the linear regression of $g$ on $z$ (valid because $\mathrm{Cov}(g,z) = \mathrm{Cov}(g, g+e) = V_A$ and $\mathrm{Var}(z) = V_P$).  Since $\bar{g} = \bar{z}$, we get the **breeder's equation**:

$$
\boxed{\;R = h^2 S\;}
$$

Response is heritability times differential.  If $h^2 = 0$, no response no matter how hard you select.  If $h^2 = 1$, the population fully tracks the selected parents.

### Where this is the Price equation

Not obvious but worth seeing.  The selection differential is related to covariance: if we define "parental fitness" as the indicator of being selected, $w_i \in \{0, 1\}$, then $\mathrm{Cov}(w, z)/\bar{w} = S$ (selection differential for trait $z$).  The Price equation under faithful inheritance of breeding values gives $\Delta \bar{g} = \mathrm{Cov}(w, g)/\bar{w}$, and by the regression identity $\mathrm{Cov}(w, g) = h^2 \mathrm{Cov}(w, z)$, so

$$
\Delta \bar{g} = h^2 \cdot \mathrm{Cov}(w, z)/\bar{w} = h^2 S.
$$

The breeder's equation is Price, filtered through the additive model and the regression $\mathbb{E}[g \mid z]$.  Good.

## The Lande Expansion

*What the breeder's equation looks like when you take the regression idea seriously.*

The idea.  Start with the Price equation for breeding values, $\Delta \bar{g} = \mathrm{Cov}(w, g)/\bar{w}$.  We want to express the right side in terms of measurable phenotype quantities.  Write $w$ as a function of $z$ (selection acts on phenotype) and expand.

If $w = w(z)$ and selection is weak enough that we can Taylor-expand, linear regression gives
$$
\mathrm{Cov}(w, g) = \mathrm{Cov}(\beta z + \text{residual}, g) = \beta \mathrm{Cov}(z, g) = \beta V_A
$$
where $\beta = \mathrm{Cov}(w, z)/\mathrm{Var}(z)$ is the **selection gradient** - the linear regression coefficient of fitness on phenotype.  Then

$$
\Delta \bar{z} = \Delta \bar{g} = \frac{V_A}{\bar{w}} \beta.
$$

In the notation Lande used, with $\beta$ absorbing $1/\bar{w}$, this is

$$
\Delta \bar{z} = V_A \beta.
$$

Same content as the breeder's equation.  The payoff is that $\beta$ makes the multivariate generalization trivial.

### Multivariate Lande

Let $\mathbf{z} \in \mathbb{R}^n$ be a vector of traits with additive genetic covariance matrix $G$ (analog of $V_A$) and phenotypic covariance $P$.  Define the selection gradient $\boldsymbol{\beta}$ as the vector of partial regression coefficients of fitness on each trait:

$$
\boldsymbol{\beta} = P^{-1} \mathbf{s}, \qquad \mathbf{s} = \mathrm{Cov}(w, \mathbf{z})/\bar{w}.
$$

Then ([Lande 1979](https://onlinelibrary.wiley.com/doi/10.1111/j.1558-5646.1979.tb04694.x)):

$$
\boxed{\;\Delta \bar{\mathbf{z}} = G \boldsymbol{\beta}\;}
$$

The response is the $G$-matrix dotted with the selection gradient.  If traits are genetically correlated, selecting on one drags others along - this is how $G$ captures evolutionary constraints.  A direction $\mathbf{v}$ with $G\mathbf{v} = 0$ is **evolutionarily inert**: no selection gradient can move the population in that direction.  A zero eigenvalue of $G$ is a constraint.

Note the elegance: $G$ is an intrinsic property of the population (its genetic architecture), $\boldsymbol{\beta}$ is a property of the selective regime (the shape of fitness as a function of traits).  The response factorizes cleanly into "what the population can do" times "what selection is asking for".

### Higher-order: why the expansion matters

The Lande equation is the **first-order** response.  What about higher-order effects?

Go back to $\Delta \bar{z} = \mathrm{Cov}(w, z)/\bar{w}$ and expand $w(z) = w_0 + w'(\bar z)(z - \bar z) + \tfrac{1}{2} w''(\bar z)(z-\bar z)^2 + \ldots$  The covariance of $w$ with $z$ picks up contributions from higher central moments of the phenotype distribution.  The **linear** term gives $\mathrm{Cov}(w, z) = w'(\bar z) \mathrm{Var}(z)$, recovering Lande's $\beta V_P$ once you rescale.  The **quadratic** term in $w$ contributes $\tfrac{1}{2} w''(\bar z) \mathbb{E}[(z-\bar z)^3]$, i.e. the third central moment (skewness).  Etc.

For a Gaussian phenotype distribution, odd central moments vanish, so only the linear-in-$w$ piece contributes to $\Delta \bar{z}$ at leading order.  **This is why Lande's first-order result is exact for Gaussian traits under selection that can be expressed through its first two moments.**  Beautiful special case.

For non-Gaussian traits or stronger selection, you need higher-order terms.  The formal machinery is the **cumulant expansion** of selection response, and it gets ugly fast.  In practice, people estimate $\beta$ empirically via linear regression of fitness on traits and call it a day, knowing they're dropping higher-order terms.

### Why non-additive variance doesn't respond

Total genetic variance can be decomposed:
$$
V_G = V_A + V_D + V_I
$$
where $V_D$ is **dominance variance** (variance from allele interactions at a single locus) and $V_I$ is **epistatic variance** (across-locus interactions), which itself decomposes further: $V_I = V_{AA} + V_{AD} + V_{DD} + \ldots$.  This is the Falconer-Mackay / Cockerham decomposition.

The reason $h^2 = V_A / V_P$ has only $V_A$ in the numerator is that $V_D$ and $V_I$ don't contribute to the **one-generation** response to selection.  Here's why.

Dominance variance comes from heterozygote effects.  Under random mating, the distribution of heterozygotes in the offspring is determined by allele frequencies, not by which individuals were selected.  So selecting strongly for high-trait individuals doesn't preferentially produce more heterozygotes of the favorable kind - the randomizing step of mating destroys that information.

Epistatic variance comes from combinations of alleles at different loci.  Recombination in the next generation breaks up the favorable combinations that selection preserved.  So $V_I$ is evanescent: it affects the parents-selected distribution but not their offspring.

**Short version**: the regression $\mathbb{E}[\text{offspring breeding value} \mid \text{parental phenotype}]$ only picks up $V_A$, because dominance and epistasis don't transmit cleanly across a mating step.

Non-additive variance does show up in longer-term dynamics.  **Conversion of epistatic to additive variance** is a real thing: populations under directional selection can convert $V_{AA}$ into $V_A$ over generations as allele frequencies shift ([Carter, Hermisson, Hansen 2005](https://doi.org/10.1016/j.tpb.2004.11.002) for the canonical treatment).  This is the "evolution of evolvability" literature.  The one-generation breeder's equation is the cleanest result; multigenerational dynamics are messier but ultimately still bookkeeping.

## Replicator Equation as Natural Gradient

*On the simplex with the Fisher (Shahshahani) metric, the replicator equation is steepest ascent on mean fitness.*

This is the bridge to information geometry.  Covered as a preview in "Information Geometry Basics" (see my post of the same name); here is the actual derivation.

### The replicator equation

Let the population state be $\mathbf{p} \in \Delta^{n-1}$, the $(n-1)$-simplex of frequencies $p_i$ ($p_i \geq 0$, $\sum p_i = 1$).  Each type has fitness $f_i$ (possibly frequency-dependent, $f_i = f_i(\mathbf{p})$).  Mean fitness is $\bar{f}(\mathbf{p}) = \sum_j p_j f_j(\mathbf{p})$.  The continuous-time **replicator equation** is

$$
\dot{p}_i = p_i (f_i - \bar{f}).
$$

Above-average types grow, below-average shrink, the simplex constraint is preserved ($\sum \dot p_i = \bar f - \bar f = 0$).  This is the continuous limit of the discrete selection $p_i' = p_i f_i / \bar{f}$ for small $f_i - 1$.

### The Shahshahani / Fisher metric on the simplex

Parametrize $\Delta^{n-1}$ by $n-1$ of the $p_i$ (the last is determined).  The **Shahshahani metric**, which is the Fisher information metric for the categorical distribution, is

$$
g_{ij}(\mathbf{p}) = \frac{\delta_{ij}}{p_i}.
$$

Diagonal in the natural simplex coordinates, with $1/p_i$ on the diagonal.  This metric has two key features: (a) it blows up near the boundary of the simplex (types near extinction are "far" from others), and (b) it's the unique (up to scale) metric on the simplex invariant under sufficient statistics (Chentsov's theorem).

The inverse metric is $g^{ij} = p_i \delta_{ij}$ (diagonal, with $p_i$).

### Natural gradient ascent on mean fitness

Natural gradient of a function $L(\mathbf{p})$ is $g^{-1} \nabla L$ - the gradient preconditioned by the inverse metric.  Take $L(\mathbf{p}) = \bar{f}(\mathbf{p})$ (mean fitness, to be ascended).

When fitnesses are frequency-independent ($f_i$ constant), $\partial \bar{f} / \partial p_i = f_i$.  The natural gradient in direction $i$ is $g^{ii} \partial_i \bar{f} = p_i f_i$.  But we have to project onto the tangent space of the simplex (the subspace $\sum v_i = 0$).  Subtract off the component along $(1, 1, \ldots, 1)$ weighted appropriately:

$$
(\tilde{\nabla} \bar{f})_i = p_i f_i - p_i \sum_j p_j f_j = p_i (f_i - \bar{f}).
$$

That's the replicator equation.  Natural gradient ascent on mean fitness on the simplex with the Fisher metric **is** replicator dynamics.

(For frequency-dependent fitness there's an extra subtlety - the "gradient" isn't quite the gradient of mean fitness because of the self-referential term.  But the computation still goes through for the interpretation: selection ascends the loss in the Fisher metric.  See [Harper 2009](https://arxiv.org/abs/0911.1383) or [Shahshahani 1979](https://www.ams.org/books/memo/0211/) for the careful treatment.)

### Why the Fisher metric is the right one

Two answers, the second more compelling than the first.

One: on the simplex, it's the unique reparametrization-invariant metric (Chentsov).  So if you want selection-as-gradient-flow to not depend on arbitrary coordinate choices, you have to use Fisher.

Two: the **information-theoretic interpretation**.  Infinitesimal KL divergence between nearby distributions is, to leading order, the Fisher metric:
$$
D_{\mathrm{KL}}(\mathbf{p} \lVert \mathbf{p} + d\mathbf{p}) = \tfrac{1}{2} g_{ij} \, dp^i \, dp^j + O(dp^3).
$$

So "gradient descent in the Fisher metric" means "gradient descent under the constraint that each step has a fixed KL-budget".  Selection isn't moving fastest in Euclidean space on the simplex - it's moving fastest in information space, where "fast" means "updating the distribution most informatively per unit of adaptive pressure".

This connects back to Fisher's fundamental theorem.  Under replicator dynamics, $\dot{\bar{f}} = \mathrm{Var}_p(f)$ (just differentiate $\bar{f} = \sum p_i f_i$ and plug in).  The rate of ascent equals the fitness variance.  Natural gradient plus Fisher's theorem give you the same equation from different directions.

## Unifying Thread: It's All Price

To recap what this post has been:

- **Price equation**: $\Delta \bar{z} = \mathrm{Cov}(w, z)/\bar{w} + \mathbb{E}[w \Delta z]/\bar{w}$.  Derived from counting.
- **Fisher's fundamental theorem**: set $z = w$.  $\Delta \bar{w} = \mathrm{Var}(w)/\bar{w}$.
- **Haldane's cost**: integrate the genetic load along the trajectory of a sweep.  $C = -\ln p_0$.
- **Breeder's equation**: Price plus phenotypic decomposition.  $R = h^2 S$.
- **Lande (univariate)**: expand the covariance in Lande's selection gradient.  $\Delta \bar{z} = V_A \beta$.
- **Lande (multivariate)**: matrix form.  $\Delta \bar{\mathbf{z}} = G \boldsymbol{\beta}$.
- **Replicator equation**: continuous-time Price on the simplex.  Natural gradient ascent in the Fisher metric.

Everything traces back to one identity.  The value of the equation isn't in its derivation (two lines), it's in the organizing perspective: whenever you see a selection argument, ask "what is $z$, what is $w$, what's being covaried?"  If you can answer that, the rest usually falls out.

## Selection = Bayesian Update

One more reframe before I stop.  In the asexual, faithful-inheritance case, the selection step is

$$
p_i' = \frac{p_i w_i}{\bar w}.
$$

This is Bayes' rule.  $p_i$ is the prior over types, $w_i / \bar{w}$ is the likelihood ratio "given survival-and-reproduction", $p_i'$ is the posterior.  "Being selected" is conditioning on an event.

More in "Probability as Operators" (see my post of the same name) - selection is one of the canonical linear operations on a probability measure, alongside marginalization and conditioning.  The replicator equation is the infinitesimal generator of continuous Bayesian updating against a time-varying likelihood.

This reframe also makes the information-theoretic content transparent.  The KL divergence from prior to posterior is the information gained by the update.  Fisher's fundamental theorem says this equals (half) the fitness variance.  Natural selection is Bayesian inference over a population, with evidence = reproductive success.

## What's Next

In the companion seed "Natural Selection: Drift, Neutrality, and Resolution Limits" I take up the finite-population story.  The Price / Lande / replicator setup here is all infinite-population, noiseless.  Real populations are finite; genetic drift adds noise to the channel.  That noise has a specific structure (Wright-Fisher, Moran, diffusion limit), a specific SNR threshold ($N_e s \sim 1$), and specific consequences (neutral theory, the molecular clock, drift barriers on adaptation).

A few pointers beyond that:

- **Kin selection and multilevel selection**: Price's real obsession.  The equation extends to group-structured populations, and the decomposition $\mathrm{Cov}(w, z) = \mathrm{Cov}_{\text{between}} + \mathbb{E}[\mathrm{Cov}_{\text{within}}]$ is the formal statement of Hamilton's rule.  Hamilton-Price is the foundation of social evolution theory.
- **Evolvability and the $G$-matrix**: the eigenstructure of $G$ tells you which trait combinations evolve easily.  Long-term evolution of $G$ itself is the "evolvability" literature ([Hansen-Houle 2008](https://onlinelibrary.wiley.com/doi/10.1111/j.1420-9101.2008.01573.x)).
- **Price under weak assumptions**: the original equation doesn't require anything about mating, ploidy, or genetic architecture.  Use it with things that aren't "genes" (cultural traits, neural circuits, market strategies).  [Frank 1997](https://onlinelibrary.wiley.com/doi/10.1111/j.1558-5646.1997.tb03650.x) is a good entry point.
- **Information-theoretic evolution**: besides the Frank papers, [Bergstrom-Lachmann](https://www.pnas.org/doi/10.1073/pnas.0409583101) on the value of information, and the bet-hedging / Kelly connections in my own [Fitness Value of Information notebook](/2026/02/12/Fitness-Value-of-Information.html).

Please clap.

*Written with Claude.*
