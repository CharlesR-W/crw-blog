---
title: "KL Divergence, Geometric Naturalness, and Optimal Transport"
date: 2025-07-11
math: true
---
# KL Divergence, Geometric Naturalness, and Optimal Transport

In a previous post, I discussed some of the theoretical shortcomings of differential entropy. Tldr it stinks because it doesn't transform right unless you add a funky scale factor that no one ever does.  I left the KL divergence alone because in that case that funky scale factor canceled, so the whole thing ends up making sense and being okay; now I'm going to bully the KL divergence (applied to continuous distributions) because it doesn't respect the geometry of the real numbers (or any space with a metric).  KL Divergence applied to discrete categorical distributions is still my buddy and I take no issue with it!

TLDR KL divergence assumes permutation invariance of the underlying space - that all the things which have probabilities are just labels - for real numbers this isn't true, in the sense that we want to think of 0 and $\epsilon$ as being "the same" or arbitrarily similar.  KL on real numbers is like a unit error in physics or a type error in computer science. This leads us to consider metric-aware metrics between probability distributions - the crowd favorite being the Wasserstein-2 distance, from which we can derive the Otto Calculus, which is the proper way to do calculus with probability distributions.

### The Problem: Permutation Invariance Is Unnatural If You Have A Metric

Let's make this concrete. At the end of the day, we want a measure of distance between probability distributions.  KL is this, but it's not "natural" to use on continuous distributions in that it doesn't respect the structure of the real numbers.  It's positive definite, sure, but it's like cold soup - works, but does not spark joy.

Here's the killer example: Consider $P_1 = \delta_0$, and $P_2 = \delta_\epsilon$ for any $\epsilon>0$.  Then $D_{KL}(P_1 \| P_2)$ is, depending on your persuasion, infinite or not-defined.  Remember when you were learning programming and they told you you're not allowed to check for equality between floats?  Is it wise and good to have a function which is infinity except when an ill-defined condition holds it's zero?  Nuh-uh.

### Two Perspectives On Distances Between Distributions

So everybody loves the information entropy.  You do, I do - it remains a monumental achievement of human intellectual endeavour - but it's not the right tool for the job.  It's defining feature, permutation invariance, is irreconcilable with having a notion of "locality".  Sometimes that's good, sometimes it's acceptable, sometimes it's bad.  Let's talk through it:

#### Perspective 1: Information Theory - The Power of Permutation Invariance

On the one hand we have classical information theory, where KL divergence, entropy, and mutual information live. The defining characteristic of this school is **permutation invariance**. This means that the "distance" between distributions only depends on the probability values, not the labels or locations of the outcomes. $D_{KL}([\frac{1}{2}, \frac{1}{2}, 0] ~\|~ [\frac{1}{4}, \frac{1}{4}, \frac{1}{2}])$ is the same whether the outcomes are {A, B, C} or {1, 10, 1000}.  Shannon and co. built these to work on categorical variables.  The argument I'll give about this stinking for reals actually also applies to ints if you don't think of ints as categorically different, but usually we do so meh.

Permutation invariance is, in a sense, the central insight of classical information theory - it tracks _number of partitions_ and doesn't care what those partitions are called.  As a direct consequence, we have the critical property called the **Data Processing Inequality**. This states that for any random variables $X, Y$ and any function $f$, we have:

$$
I(X; Y) \ge I(X; f(Y))
$$

In words: you cannot create information by processing data.  If you have an alternative 'information metric' you're trying to sell (and I do), and twiddling a few bits can """create""" """information""", it's not really concordant with what we understand information to _mean_. 

#### Perspective 2: Geometry - And Introducing Optimal Transport

On the other hand, we can demand a metric-aware approach for our space-that-obviously-has-a-metric.  One such approach -the main one we'll consider - is called "Optimal Transport", basically just asks how much and _how far_ you'd have to move probability mass to make one distribution into the other.  The most famous 'Optimal Transport' metric is the **Earth Mover's Distance** (the stage name of the Wasserstein-1 distance $W_1$.  
$$
W_1(\mu , \nu) = \inf_{T: ~ T^\# \mu = \nu} \int_{\mathbb{R}} d(x,T(x)) ~ dx
$$
(T is the "transport plan", and the inf makes it 'optimal' - tah-dah - more on this in a second if this doesn't make a ton of sense)  TLDR is that $W_1(\mu , \nu)$ is (amount of probability mass moved) x (distance it got moved) needed to make $\mu$ into $\nu$. 

I like naturalness, but I won't claim that Wasserstein is the only metric-aware distance.  It is the one with the most nice properties for general use, afaik.

### Wasserstein Distance: A Metric for Measures

The Earth Mover's Distance is a slightly not-as-cool version of the general **Wasserstein-p distance**. For two probability measures $\mu$ and $\nu$ on a space $X$ with a metric $d(x,y)$, it is defined as:

$$
W_p(\mu, \nu) = \left( \inf_{\gamma \in \Pi(\mu, \nu)} \int_{X \times X} d(x, y)^p \,d\gamma(x, y) \right)^{1/p}
$$

Let's break this down (can you tell Gemini wrote this part lol?):
*   $\Pi(\mu, \nu)$ is the set of all joint probability distributions $\gamma(x,y)$ whose marginals are $\mu(x)$ and $\nu(y)$. You can think of $\gamma(x,y)$ as a **transport plan**: it specifies how much probability mass from location $x$ should be moved to location $y$.
*   The integral represents the total cost of executing a given plan $\gamma$, where the cost to move a unit of mass from $x$ to $y$ is $d(x,y)^p$.
*   The `inf` (infimum) means we are searching for the best possible transport plan—the one with the minimum cost.

The choice of $p$ is important, but a particularly special case is $p=2$. The **Wasserstein-2 distance, $W_2$**, is our friend because it endows the space of probability distributions with the structure of an (infinite-dimensional) Riemannian manifold.  This let's us do something called **Otto Calculus**, which is calculus on probability distributions.

### Otto Calculus: The Geometry of Probability

Calculating the $W_2$ distance by searching over all possible transport plans $\gamma$ is computationally intractable. The breakthrough comes from **Brenier's Theorem**. It states that for $W_2$ distance, if (blah-blah-blah weak condition that in practice always holds), then the optimal transport plan is the gradient of convex function:
$$
T(x) = \nabla \psi(x)
$$
Okay cool sure I guess - but actually it is: It connects optimal transport to convex analysis and, excitingly, to fluid dynamics. Specifically, the optimal transport is a potential flow, along which "probability fluid" is transported.

If the space of probability distributions over $X$, let's call it $\Delta X$, is a Riemannian manifold under the $W_2$ metric, we can do calculus on it. The most natural first thing to do on a manifold is to study motion along gradients (I mean okay yeah it's a _bit_ contrived, but not totally nuts). Specifically, we can ask about **gradient flow** under some scalar function $S$:

$$
\frac{d\mu_t}{dt} = - \text{grad}_W S(\mu_t)
$$

Here, $\text{grad}_W$ is the abstract gradient on Wasserstein space. To make this useful, we need to connect it to something we can actually compute. The link is the standard **variational derivative** $\frac{\delta S}{\delta \mu(x)}$, which acts as a sort of derivative with respect to the entire function $\mu$ (but irl it's just what you get by naively differentiating $S$ and pretending $\mu(x)$ is an independent variable for each $x$). The central formula of Otto calculus provides the dictionary:

$$
\text{grad}_W S(\mu) = \nabla_x \cdot \left(\mu \nabla_x \frac{\delta S}{\delta \mu(x)}\right)
$$

Here, the $\nabla_x$ is the _old_ gradient on the underlying space - so now we have a recipe to relate the two, and its quite the cutie. This equation translates the abstract geometric notion of a Wasserstein gradient into a concrete partial differential equation involving standard calculus.  It bears emphasizing that this is a transport term; in fluid mechanics, if you attach some scalar quantity $\phi$ to the fluid (like energy - anything that's "per kilogram"), it satisfies the transport equation that looks like

$$
\frac{\partial(\rho \phi)}{\partial t} + \nabla \cdot(\rho \vec{v} \phi) = \omega_\phi
$$
$$
(\textrm{local change}) + (\textrm{net accumulation}) = (\textrm{generation})
$$
Store that - we'll talk about it in a minute!

#### Heat Flow is Gradient Descent on Entropy

So we've been talking about "naturalness" and how optimal transport is "more natural" than KL in some sense.  Here we'll take a bit of a diversion so we can see how powerful (or at least interesting) naturalness makes us.

To some extent, there's nothing more natural than gradient-flow : you have a thing $w$ that depends on $t$, a single scalar function $L$.  You kinda have exactly one way to write a differential equation:
$$
\frac{\partial w}{\partial t} = - \epsilon ~\nabla_w L
$$
or in our case, we'll change the letters for flavor:
$$
\frac{\partial \mu}{\partial t} = - \epsilon ~\textrm{grad}_W S(\mu)
$$
i.e. 
$$
\frac{\partial \mu}{\partial t} + \epsilon \nabla_x \cdot \left(\mu \nabla_x \frac{\delta S}{\delta \mu(x)}\right) = 0
$$
Compare this to the fluid flow equation (with the transported equation $\phi=1$, so the quantity being transported is "probability mass" in a pretty literal sense) - Wasserstein gradient flow is how probability-density is transported by the velocity field $\nabla \frac{\delta S}{\delta \mu}$ !  Cute, yeah?

Moving right along, consider the negative entropy functional (i.e. the entropy functional for people who dislike minus signs - me!): $S(\mu) = \int \mu(x) \log \mu(x) \,dx$. Minimizing this functional is equivalent to maximizing entropy. What is its gradient flow?

1.  **Compute the Variational Derivative:** A standard result from calculus of variations is that $$\frac{\delta S}{\delta \mu(x)} = 1 + \log \mu(x)$$.

2.  **Plug and Play:** The gradient flow equation becomes:
    $$
    \frac{\partial \mu}{\partial t} = - \nabla \cdot \left(\mu \nabla (1 + \log \mu)\right)
		    $$
	so then,
    $$
    \frac{\partial \mu}{\partial t} = - \nabla^2 \mu
    $$

Ain't that neat! Let's play it again Sam: Wasserstein-gradient flow on the entropy functional is heat-diffusion!  We've shown that this physics-y PDE is actually a simple _geometric_ process.  Heat diffusion is the most efficient way for a distribution to spread out and maximize its entropy.  If you like, you can do this with the free energy to get the Fokker-Planck PDE too!

As a side note at the end of the physics here, think how wild it is that thermodynamics _works_ given that the whole ensemble thing _doesn't_ respect locality in the way we just showed!
### Practical Realities: Sample Complexity AHHHH

For all its theoretical beauty, $W_2$ has a major practical problem: estimating it from samples is  cursed (dimensionally, specifically) and requires a stupid number of samples to be accurate. Directly solving the transport problem is computationally expensive; and statistically estimating it also sucks.  Let's crack out the asymptotics (see [this video](https://www.youtube.com/watch?v=SZHumKEhgtA&ab_channel=MLSSAfrica) 1:12:15 ; all three of these talks are pretty fun):

For reference, let's talk about distributions over $n$ discrete points.  Then estimating MMD is $O(\frac{1}{\sqrt{n}})$.  Wasserstein is $O(\frac{1}{n^{1/d}})$, ($d$ the dimensionality of the space where these points live).  That's _baaaaaaad_ if you're working in a high-d space.

This is why practical applications often resort to clever workarounds. The famous **Wasserstein GAN (WGAN)** uses a different formulation for $W_1$ based on the Kantorovich-Rubinstein duality:

$$
W_1(\mu, \nu) = \sup_{\|f\|_L \le 1} \left( \mathbb{E}_{x \sim \mu}[f(x)] - \mathbb{E}_{x \sim \nu}[f(x)] \right)
$$

This dual formulation changes the problem from finding an optimal transport plan to finding a single 1-Lipschitz function $f$ that maximally separates the two distributions. This is a task a neural network can approximate well, sidestepping the direct OT problem.  But morally, you have to introduce a _whole neural network_ to evaluate this distance.

Another fix is the **Sinkhorn distance**. This approach adds an entropic regularization term to the original OT problem, penalizing transport plans $\gamma$ that are too "certain":

$$
\text{Cost}(\gamma) = \int d(x, y)^p \,d\gamma(x, y) - \epsilon H(\gamma)
$$

The magic of this regularization is that it makes the optimization problem "strictly convex" and allows for a very fast iterative algorithm (the Sinkhorn-Knopp algorithm) to find the solution. The catch is that you are no longer computing the true Wasserstein distance. The regularization parameter $\epsilon$ introduces a bias, creating a trade-off: higher speed and stability for a less accurate, "blurry" approximation of the true transport cost.

### Case Study: β-VAE and Implicit Geometry

This is more of a tangent since I was studying β-VAEs at the same time as this- I'll assume you know what that is - else check [Lili's post](https://lilianweng.github.io/posts/2018-08-12-vae/) because she's the bestestest); think of it like an intuition check where I say I'm full of it about all this optimal transport stuff because β-VAE learns geometry just fine thank you very much, then I argue with myself and it turns out that β-VAE really would love to not learn geometry if only it could have more output heads.

The loss function is:

$$
\mathcal{L} = \mathbb{E}_{q(z|x)}[\log p(x|z)] - \beta D_{KL}(q(z|x) \| p(z))
$$

This is the standard VAE loss, but with the hyperparameter $\beta$. For a standard VAE, $\beta=1$. By setting $\beta > 1$, we place a much stronger penalty on the KL divergence term. This term pushes the learned latent distribution for each input, $q(z\|x)$, towards a simple prior, $p(z)$ (e.g., an isotropic Gaussian).

Basically large β tries to make the VAE put all of its samples really close to the origin, even though this makes it way harder to reconstruct stuff - so you have these Gaussian blobs for different classes that it would love to just put infinity far away from each other, but now it can't, so it has to learn to be very judicious with how much it lets each blob spread out - it can only let classes have variance if they 'need it more' than other classes.  At the end of it, the idea is that now you can interpolate between two classes in latent space, and you will meaningfully interpolate in output space too.

Okay then so am I full of it?  In general yes but here I think no (I'm writing it after all) - this picture of how β-VAE works assumes you're encoding stuff as a Gaussian - if you pretend your encoder is unlimited by mortal constraints and can output an arbitrary probability distribution, then you should end up with a whacky convoluted thing that still pushes distributions near the origin, but can be arbitrarily discontinuous in achieving that as long as it preserves reconstruction loss.

### Conclusion: Okay You Can Go Back To Using KL Divergence - But At Least We Got Some Fun PDEs!

Okay, so the name of the game is naturalness.  In a space with a metric, like the real numbers or whatever, your metric on probability distributions should respect the underlying metric.  KL doesn't do this - and for tokens which really are just discrete ints where the actual number is meaningless, that's right.  If you want to be "natural", you need something metric-aware, and one of the best options for this is $W_2$.

$W_2$ gives you some really nice geometry - we talked about Otto calculus on the space of probability distributions, and this gives us some really nice PDEs.  Yay I love PDEs!