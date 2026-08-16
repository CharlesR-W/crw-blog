---
title: "Mori–Zwanzig, Hankel Geometry, and Spectral Reconstruction of Context-Free Memory"
date: 2026-08-16
tags: [notes, ai]
math: true
---

*These are AI-generated notes from a conversation with GPT5.5-Pro about extending Hankel realization ideas from finite-state systems to recursive, context-free memory.  I have not fully vetted the mathematical claims or references.  Treat this as a provisional research synthesis and construction sketch, not a polished publication.*

---

The motivating analogy is between two ways of replacing hidden state by observable predictive structure.

For weighted finite automata and hidden Markov models, the Hankel matrix packages the observable behavior of the system into an operator whose rank gives the minimal linear realization dimension. This does more than reconstruct a hidden model: it equips the space of predictive behaviors with a geometry, because two models are close when the functions they induce on future strings are close.

For Mori–Zwanzig reduction, one similarly projects a larger Markovian system onto a smaller set of resolved variables. Eliminating the unresolved state induces a memory kernel. The basic question is whether one can use this memory formalism to obtain an analogue of spectral reconstruction for systems with genuinely recursive, context-free memory—roughly, replacing finite-state automata by pushdown automata.

The central claim is:

> A Mori–Zwanzig memory kernel is not itself a stack. Rather, stack dynamics can be viewed as a particular Markovian realization of unresolved dynamics, and eliminating the stack produces a recursively structured first-return memory kernel. The correct spectral object is then not the ordinary word Hankel matrix, but a tree- or context-Hankel operator.

This suggests a hierarchy:

| Hidden Markovian realization | Effective memory | Algebraic class | Spectral object |
|---|---|---|---|
| finite-dimensional hidden state | finite-mode memory | rational series | ordinary/block Hankel matrix |
| finite control + unbounded stack | recursive first-return memory | algebraic/context-free series | tree or nested Hankel matrix |
| arbitrary unresolved system | arbitrary nonlocal memory | general formal series/operator | typically infinite-rank |

The rest of this note develops that analogy.

---

## 1. Hankel matrices as behavioral geometry

Let

$$
f:\Sigma^\ast\to\mathbb R
$$

be a weighted function on strings. Its Hankel matrix is

$$
H_f(u,v)=f(uv),
$$

with rows indexed by prefixes $u$ and columns by suffixes $v$.

For a stochastic process, one can take $f(w)=p(w)$. Up to normalization by $p(u)$, the row

$$
v\mapsto H_f(u,v)
$$

is the predictive distribution over futures after observing $u$.

A weighted finite automaton with $r$ latent states has the form

$$
f(w_1\cdots w_n)
=
\alpha^\top A_{w_1}\cdots A_{w_n}\omega.
$$

Hence

$$
H_f(u,v)
=
\alpha^\top A_uA_v\omega.
$$

Writing

$$
P(u,:)=\alpha^\top A_u,
\qquad
S(:,v)=A_v\omega,
$$

we obtain

$$
H_f=PS,
$$

so

$$
\operatorname{rank}H_f\le r.
$$

Conversely, finite Hankel rank characterizes rational formal series, equivalently weighted finite automata. Therefore

$$
r_\star=\operatorname{rank}H_f
$$

is the minimal linear predictive-state dimension.

This gives three useful viewpoints.

### 1.1 Behavioral quotient

Two different hidden-state parameterizations are equivalent if they compute the same observable function $f$.

Thus the primitive object is not the hidden model but its behavior.

### 1.2 Predictive states

A prefix $u$ induces the residual function

$$
\mathcal R_u:v\mapsto f(uv).
$$

Two prefixes are exactly equivalent if

$$
\mathcal R_u=\mathcal R_{u'}.
$$

A natural approximate distance is

$$
d(u,u')^2
=
\sum_v \mu(v)
\left|
f(uv)-f(u'v)
\right|^2.
$$

So the Hankel construction induces a geometry on predictive states.

### 1.3 Spectral reconstruction

Choose finite prefix and suffix bases $\mathcal P,\mathcal S$, and form

$$
H=H_f[\mathcal P,\mathcal S],
$$

together with shifted Hankel blocks

$$
H_a(u,v)=f(uav).
$$

Take the truncated singular value decomposition

$$
H\approx U_r\Sigma_rV_r^\top,
$$

and define the balanced factorization

$$
L=U_r\Sigma_r^{1/2},
\qquad
R=\Sigma_r^{1/2}V_r^\top.
$$

Then the transition operators are reconstructed by

$$
\widehat A_a=L^+H_aR^+,
$$

with corresponding formulas for the initial and final vectors.

The important point is that this construction remains meaningful even when there is no literal ground-truth HMM. It reconstructs the best low-rank predictive realization.

---

## 2. Linear Mori–Zwanzig is already a realization problem

Consider a discrete-time linear system

$$
\begin{pmatrix}
x_{t+1}\\
y_{t+1}
\end{pmatrix}
=
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}
\begin{pmatrix}
x_t\\
y_t
\end{pmatrix},
$$

where $x_t$ is resolved and $y_t$ unresolved.

Iterating the unresolved dynamics gives

$$
y_t
=
D^ty_0+
\sum_{s=0}^{t-1}D^{t-1-s}Cx_s.
$$

Substituting back into the resolved dynamics,

$$
x_{t+1}
=
Ax_t
+
\sum_{j=0}^{t-1}
K_jx_{t-1-j}
+
\eta_t,
$$

with

$$
K_j=BD^jC,
$$

and

$$
\eta_t=BD^ty_0.
$$

This is a generalized Langevin equation: a Markovian term, a memory term, and an orthogonal or unresolved forcing term.

Now construct the block Hankel matrix

$$
\mathscr H_0
=
\begin{pmatrix}
K_0&K_1&K_2&\cdots\\
K_1&K_2&K_3&\cdots\\
K_2&K_3&K_4&\cdots\\
\vdots&\vdots&\vdots&
\end{pmatrix}.
$$

Using

$$
K_j=BD^jC,
$$

we obtain

$$
\mathscr H_0
=
\begin{bmatrix}
B\\
BD\\
BD^2\\
\vdots
\end{bmatrix}
\begin{bmatrix}
C&DC&D^2C&\cdots
\end{bmatrix}.
$$

Therefore

$$
\operatorname{rank}\mathscr H_0
\le \dim y.
$$

Under reachability and observability conditions, equality holds at the minimal realization.

Define the shifted block Hankel matrix

$$
\mathscr H_1(i,j)=K_{i+j+1}.
$$

If

$$
\mathscr H_0=LR
$$

is a rank factorization, then

$$
\widehat D=L^+\mathscr H_1R^+.
$$

This is essentially the Ho–Kalman realization theorem.

Thus there is already a direct correspondence

$$
\boxed{
\text{WFA spectral reconstruction}
\;\longleftrightarrow\;
\text{finite-dimensional realization of an MZ memory kernel}.
}
$$

At the transfer-function level,

$$
\widehat K(z)
=
\sum_{j\ge0}K_jz^j
=
B(I-zD)^{-1}C.
$$

Hence a finite-dimensional hidden bath produces a rational memory kernel.

---

## 3. Why generic memory is not a stack

It is important to distinguish different notions of memory.

A finite-state system has bounded internal state.

A generalized Langevin equation may have arbitrarily long temporal memory:

$$
x_{t+1}
=
Ax_t+\sum_{j\ge0}K_jx_{t-j}+\eta_t.
$$

But ordinary convolution memory is only indexed by lag. It does not provide a last-in-first-out data structure.

A pushdown automaton instead has an unbounded stack. Its current behavior can depend on which symbol was most recently pushed but not yet popped.

Therefore

$$
\text{long memory}
\not\Rightarrow
\text{stack memory}.
$$

The correct relation runs in the opposite direction:

1. A pushdown automaton is Markovian on the infinite configuration space
   $$
   (\text{finite control state},\text{stack contents}).
   $$

2. Project away the stack.

3. Mori–Zwanzig produces a non-Markovian effective dynamics on the finite control sector.

4. Because the eliminated dynamics is recursively organized by push and pop operations, the resulting kernel is not arbitrary; it belongs to an algebraic or context-free class.

So a pushdown automaton is a particular structured Markovian realization of a Mori–Zwanzig memory process.

---

## 4. First-return kernels and self-energies

Let $U_a$ be the transition operator associated with observed symbol $a$.

Let

$$
\Pi
$$

project onto a resolved boundary sector, for example states with empty stack, and define

$$
Q=I-\Pi.
$$

For a word

$$
w=a_1\cdots a_n,
$$

the projected total transfer is

$$
F(w)
=
\Pi U_{a_n}\cdots U_{a_1}\Pi.
$$

Now define the irreducible first-return transfer

$$
R(w)
=
\Pi U_{a_n}
Q U_{a_{n-1}}Q
\cdots
Q U_{a_2}Q
U_{a_1}\Pi.
$$

This sums paths which:

- start in the resolved sector,
- enter the unresolved sector,
- do not revisit the resolved sector in the middle,
- and finally return.

The total resolved behavior is built from concatenations of such excursions:

$$
F
=
\mathbf 1
+
R
+
R\star R
+
R\star R\star R+\cdots,
$$

where $\star$ is convolution over word concatenations.

Formally,

$$
F=(\mathbf 1-R)_{\star}^{-1}.
$$

This is simultaneously a renewal equation, a Dyson equation, and a Mori–Zwanzig memory expansion.

For a time-homogeneous linear system, the same structure reduces to

$$
K_j=BD^jC.
$$

At the resolvent level,

$$
\Pi(I-zU)^{-1}\Pi
=
\left[
I-zA-z^2B(I-zD)^{-1}C
\right]^{-1}.
$$

The quantity

$$
\Sigma(z)
=
z^2B(I-zD)^{-1}C
$$

acts as a memory self-energy.

Finite-dimensional $D$ gives a rational self-energy. Stack-structured $D$ gives an algebraic self-energy.

---

## 5. Why stack dynamics gives algebraic series

A weighted context-free grammar in binary normal form may be represented by a finite system

$$
S_i
=
e_i
+
\sum_{a\in\Sigma}b_{ia}a
+
\sum_{j,k}T_{ijk}S_jS_k.
$$

Here

- $S_i$ is the formal series generated by nonterminal $i$,
- $b_{ia}$ is the weight for emitting terminal $a$,
- $T_{ijk}$ is the weight of the production
  $$
  i\to jk,
  $$
- and $e_i$ represents an optional empty production.

The output series is

$$
f=\alpha^\top S.
$$

Because the $S_i$ satisfy polynomial equations, $f$ is an algebraic formal power series.

The pushdown interpretation is particularly useful. A nonterminal can be indexed schematically as

$$
[p,\gamma,q],
$$

meaning:

> the total weight of paths beginning in control state $p$ with stack symbol $\gamma$ exposed and ending in control state $q$ immediately after $\gamma$ has been removed.

These quantities obey polynomial recursions because execution beneath $\gamma$ may recursively contain further pushes and matching pops.

Thus the empty-stack first-return kernel of a weighted pushdown system is an algebraic formal series.

Schematically,

$$
\boxed{
\text{pushdown-realizable MZ kernel}
\;\simeq\;
\text{matrix-valued algebraic formal series}.
}
$$

This is the main bridge between Mori–Zwanzig and context-free computation.

---

## 6. Example: Dyck memory

Consider the grammar

$$
S\to \epsilon
$$

or

$$
S\to (S)S.
$$

Let each matched pair carry weight $\lambda$, and let $z$ count terminal symbols.

The generating function satisfies

$$
F(z)
=
1+\lambda z^2F(z)^2.
$$

The regular solution is

$$
F(z)
=
\frac{
1-\sqrt{1-4\lambda z^2}
}{
2\lambda z^2
}.
$$

The irreducible first-return excursion consists of one outer matched pair surrounding an arbitrary balanced structure, so

$$
R(z)
=
\lambda z^2F(z).
$$

The total generating function satisfies the renewal relation

$$
F(z)
=
1+R(z)F(z),
$$

hence

$$
F(z)
=
\frac{1}{1-R(z)}.
$$

The interpretation is immediate:

- $R$ is the first-return memory kernel,
- $F$ is the full projected propagator,
- recursion produces algebraic rather than rational memory,
- the square-root singularity prevents exact realization by a finite-dimensional linear bath.

The ordinary word Hankel matrix of Dyck behavior has unbounded rank with increasing depth. This is why the ordinary Hankel matrix is the wrong spectral object for context-free memory.

---

## 7. The correct replacement: a context Hankel operator

The deeper principle behind the Hankel construction is not concatenation itself.

Instead, one chooses

1. a class of fragments,
2. a class of contexts,
3. an operation that plugs a fragment into a context.

For strings, fragments and contexts interact by concatenation.

For recursive structure, the natural operation is substitution into a one-hole tree context.

### 7.1 Tree Hankel matrix

Let $\mathcal T$ denote a set of binary trees and $\mathcal C$ the corresponding one-hole contexts.

For a weighted tree function

$$
\widetilde f:\mathcal T\to\mathbb R,
$$

define the tree Hankel matrix

$$
H_{\widetilde f}(c,\tau)
=
\widetilde f(c[\tau]).
$$

A weighted tree automaton has parameters

$$
\alpha\in\mathbb R^r,
\qquad
b_a\in\mathbb R^r,
\qquad
T\in\mathbb R^{r\times r\times r}.
$$

Its recursive state representation is

$$
h(a)=b_a,
$$

and

$$
h((\tau_1,\tau_2))
=
T\bigl(h(\tau_1),h(\tau_2)\bigr).
$$

The final value is

$$
\widetilde f(\tau)
=
\alpha^\top h(\tau).
$$

The analogue of the WFA rank theorem is

$$
\operatorname{rank}H_{\widetilde f}
=
\text{minimal weighted-tree-automaton state dimension}.
$$

Thus the finite latent object is not a finite set of stack configurations. It is a finite-dimensional **composition algebra** for recursive subcomputations.

### 7.2 Nested Hankel matrices

If the observed alphabet itself marks calls, returns, and internal symbols, one may instead use a visibly pushdown representation.

For well-nested words, define

$$
H_{\mathrm{nest}}(u,v)
=
f(uv),
$$

with $u,v$ restricted to well-nested strings.

The rank of this restricted operator characterizes weighted visibly pushdown realizations, up to the familiar quadratic relation between control-state dimension and matrix-valued fragment states.

The tree construction is conceptually cleaner; the nested-word construction is often operationally more natural when boundaries are visible in the data.

---

## 8. Geometry of context-free predictive states

For a subtree $\tau$, define its contextual residual

$$
\mathcal R_\tau(c)
=
\widetilde f(c[\tau]).
$$

Two subtrees are behaviorally equivalent if

$$
\tau\sim\tau'
\quad\Longleftrightarrow\quad
\mathcal R_\tau
=
\mathcal R_{\tau'}.
$$

This is the context-free analogue of Myhill–Nerode or WFA predictive-state equivalence.

With a distribution $\mu_C$ over contexts, define

$$
d(\tau,\tau')^2
=
\sum_{c\in\mathcal C}
\mu_C(c)
\left|
\widetilde f(c[\tau])
-
\widetilde f(c[\tau'])
\right|^2.
$$

For a matrix-valued Mori–Zwanzig kernel, use the Frobenius norm:

$$
d(\tau,\tau')^2
=
\sum_c
\mu_C(c)
\left\|
\widetilde{\mathcal K}(c[\tau])
-
\widetilde{\mathcal K}(c[\tau'])
\right\|_F^2.
$$

Similarly, two entire models can be compared by

$$
d(\widetilde f,\widetilde g)^2
=
\sum_{c,\tau}
\mu_C(c)\mu_T(\tau)
\left|
\widetilde f(c[\tau])
-
\widetilde g(c[\tau])
\right|^2.
$$

Equivalently,

$$
d(\widetilde f,\widetilde g)
=
\left\|
D_C^{1/2}
\left(
H_{\widetilde f}
-
H_{\widetilde g}
\right)
D_T^{1/2}
\right\|_{\mathrm{HS}}.
$$

So the context Hankel operator gives a geometry on the behavioral quotient space of grammars.

---

## 9. Soft nonterminals from the SVD

Let

$$
H
=
U\Sigma V^\top.
$$

Then a balanced latent representation of a subtree $\tau$ may be defined as

$$
z_\tau
=
\Sigma^{1/2}V^\top e_\tau.
$$

Large singular directions correspond to distinctions between subtrees that strongly affect many contexts.

Small singular directions correspond to distinctions that are nearly behaviorally irrelevant.

These latent directions are best thought of as **soft nonterminals**.

They are not necessarily discrete symbolic categories. Instead they span the minimal finite-dimensional space required to compose recursive predictive states.

This is closely analogous to balanced truncation.

The inside computation plays the role of reachability or controllability: which latent states can be generated by subtrees?

The outside context plays the role of observability: how much does a latent state affect the completed structure?

The singular values quantify the product of these two effects.

---

## 10. Gauge equivalence

The latent coordinates themselves are not unique.

For any invertible matrix $Q$,

$$
b_a
\mapsto
Q^{-1}b_a,
$$

$$
\alpha
\mapsto
Q^\top\alpha,
$$

and

$$
T
\mapsto
Q^{-1}T(Q\otimes Q)
$$

leave the represented tree function unchanged.

This is the nonlinear-bilinear analogue of similarity transformations in linear state-space models.

After balancing, the remaining ambiguity consists of sign changes and rotations within degenerate singular subspaces.

Therefore nearby behaviors need not produce nearby individual nonterminal labels.

What is stable is the recovered latent subspace.

If

$$
\sigma_r-\sigma_{r+1}>0,
$$

then perturbation theory gives schematically

$$
\|\sin\Theta(\widehat U_r,U_r)\|
\lesssim
\frac{
\|\widehat H-H\|
}{
\sigma_r-\sigma_{r+1}
}.
$$

Thus spectral gaps control identifiability of the approximate grammatical state space.

---

## 11. An algebraic-kernel generalized Langevin equation

Suppose the observed data consist of resolved variables

$$
g_t\in\mathbb R^d
$$

and event labels

$$
a_t\in\Sigma.
$$

We want to learn a matrix-valued memory series

$$
\mathcal K:\Sigma^+\to\mathbb R^{d\times d}
$$

constrained to have context-free recursive structure.

Choose

- a latent grammatical dimension $r$,
- terminal vectors
  $$
  b_a\in\mathbb R^r,
  $$
- a bilinear tensor
  $$
  T:\mathbb R^r\times\mathbb R^r\to\mathbb R^r,
  $$
- and matrix-valued readouts
  $$
  K_1,\ldots,K_r\in\mathbb R^{d\times d}.
  $$

For a span $a_i\cdots a_{j-1}$, define

$$
h_{i,i+1}
=
b_{a_i},
$$

and

$$
h_{i,j}
=
\sum_{k=i+1}^{j-1}
T(h_{i,k},h_{k,j}).
$$

The sum over split points implements a weighted sum over binary parse trees.

Define

$$
\mathcal K(a_i\cdots a_{j-1})
=
\mathcal O(h_{i,j}),
$$

where

$$
\mathcal O(h)
=
\sum_{q=1}^r
h_qK_q.
$$

Then the resolved dynamics is

$$
g_{t+1}
=
Ag_t
+
\sum_{\ell=1}^{\min(L,t)}
\mathcal K(a_{t-\ell+1:t})
\phi(g_{t-\ell})
+
\eta_{t+1}.
$$

For a linear model,

$$
\phi(g)=g.
$$

For nonlinear reduced dynamics, $\phi$ may be a fixed observable dictionary or learned feature map.

This is an **algebraic-kernel generalized Langevin equation**.

Ordinary MZ has a lag-indexed kernel

$$
K_\ell.
$$

The context-free version replaces it by a word-indexed kernel

$$
\mathcal K(w)
$$

whose dependence on $w$ is recursively compressed by the finite tensor algebra $(b_a,T,\mathcal O)$.

---

## 12. Computational cost

For unrestricted binary parsing of a sequence of length $n$,

- there are $O(n^2)$ spans,
- each span has $O(n)$ split points,
- a dense bilinear composition costs $O(r^3)$.

Thus the naive complexity is

$$
O(n^3r^3).
$$

With a finite memory horizon $L$, the streaming cost becomes approximately

$$
O(nL^2r^3).
$$

A low-rank CP factorization

$$
T_{ijk}
=
\sum_{m=1}^q
u_{im}v_{jm}w_{km}
$$

can reduce one bilinear composition to roughly $O(qr)$, giving

$$
O(nL^2qr).
$$

This makes the model computationally plausible for moderate $L$ and $r$.

---

## 13. Estimating the ordinary MZ kernel from correlations

For stationary resolved observables, write

$$
g_{t+1}
=
\sum_{\ell=0}^{t}
\Omega_\ell g_{t-\ell}
+
W_t.
$$

Let

$$
C_k
=
\mathbb E[g_{t+k}g_t^\top].
$$

The Mori orthogonality condition gives

$$
C_{k+1}
=
\sum_{\ell=0}^{k}
\Omega_\ell C_{k-\ell}.
$$

Hence

$$
\Omega_0
=
C_1C_0^+,
$$

and recursively,

$$
\Omega_k
=
\left[
C_{k+1}
-
\sum_{\ell=0}^{k-1}
\Omega_\ell C_{k-\ell}
\right]
C_0^+.
$$

This is a Volterra or renewal deconvolution.

The context-free generalization is to estimate word-conditioned moments

$$
C(w)
=
\mathbb E
\left[
g_{t+|w|}
g_t^\top
\mathbf 1
\{
a_{t+1:t+|w|}=w
\}
\right].
$$

Joint moments are often preferable to conditional moments because they avoid division by small probabilities $p(w)$.

The time-convolution identity is then replaced schematically by convolution over word factorizations:

$$
C(w)
=
\sum_{w=uv}
\Omega(v)C(u),
$$

with chronological ordering fixed consistently.

This gives two possible learning strategies.

### Strategy A: kernel first

1. Estimate $\Omega(w)$ on observed words or spans.
2. Construct a context Hankel operator.
3. Fit a low-rank algebraic realization.

### Strategy B: direct structured prediction

Directly fit the recursive parameters

$$
(b_a,T,\mathcal O)
$$

to the correlation identities and resolved prediction loss.

The first approach is more spectral and interpretable.

The second is likely more statistically efficient when long words are sparse.

---

## 14. Spectral reconstruction with observed tree structure

Suppose a weighted tree series $\widetilde f$ is available.

Choose basis trees

$$
\mathcal T_0
=
\{\tau_1,\ldots,\tau_s\}
$$

and one-hole contexts

$$
\mathcal C_0
=
\{c_1,\ldots,c_m\}.
$$

Construct

$$
H_{ij}
=
\widetilde f(c_i[\tau_j]).
$$

Also construct the binary-composition block

$$
H^{(2)}_{i,(j,k)}
=
\widetilde f
\left(
c_i[(\tau_j,\tau_k)]
\right),
$$

terminal columns

$$
h_a(i)
=
\widetilde f(c_i[a]),
$$

and the root row

$$
h_\circ(j)
=
\widetilde f(\tau_j).
$$

Compute a rank-$r$ factorization

$$
H
\approx
LR.
$$

Then recover

$$
b_a
=
L^+h_a,
$$

$$
T_{(1)}
=
L^+H^{(2)}
(R\otimes R)^+,
$$

and

$$
\alpha^\top
=
h_\circ^\top R^+.
$$

Here $T_{(1)}$ is the mode-one matricization of the composition tensor.

Compare this with the WFA formula

$$
A_a
=
L^+H_aR^+.
$$

The essential change is therefore

$$
\boxed{
\text{linear transition }A_az
\quad\longrightarrow\quad
\text{bilinear composition }T(z_1,z_2).
}
$$

This is the cleanest spectral analogue of the WFA construction.

---

## 15. The latent-tree problem

If only unbracketed sequences are observed, then the grammar defines a string series

$$
f(w)
=
\sum_{\tau:\operatorname{yield}(\tau)=w}
\widetilde f(\tau).
$$

The tree Hankel matrix belongs to $\widetilde f$, but the data only reveal the pushforward $f$.

This creates a real identifiability problem.

Different distributions over latent parse trees may induce exactly the same distribution over observed strings.

A natural complexity measure for a string behavior $f$ is therefore

$$
\mathfrak r_{\mathrm{CFG}}(f)
=
\min_{\widetilde f}
\left\{
\operatorname{rank}H_{\widetilde f}
:
f(w)
=
\sum_{\tau:\operatorname{yield}(\tau)=w}
\widetilde f(\tau)
\right\}.
$$

For an MZ kernel,

$$
\mathfrak r_{\mathrm{CFG}}(\mathcal K)
=
\min_{\widetilde{\mathcal K}}
\left\{
\operatorname{rank}H_{\widetilde{\mathcal K}}
:
\mathcal K(w)
=
\sum_{\tau:\operatorname{yield}(\tau)=w}
\widetilde{\mathcal K}(\tau)
\right\}.
$$

This is a behaviorally invariant notion of minimal context-free memory dimension.

It is not generally easy to compute.

A finite-data relaxation is

$$
\min_{\widetilde H}
\mathcal L_{\mathrm{obs}}(\widetilde H)
+
\lambda
\|\widetilde H\|_\ast
$$

subject to approximate inside/outside recursion constraints.

A more practical nonconvex approach would alternate:

1. initialize a soft distribution over parse trees,
2. estimate posterior tree/context moments,
3. construct a tree Hankel matrix,
4. truncate its SVD,
5. reconstruct $b_a,T,\alpha$,
6. re-estimate soft parses,
7. fine-tune using the MZ prediction objective.

Spectral initialization keeps the latent grammar induction problem anchored to a low-rank behavioral geometry.

---

## 16. What should count as minimal memory?

Penalizing only memory duration or memory norm is not enough.

A kernel can be

- long-lived but generated by one grammatical state,
- short-lived but require many grammatical states,
- small in amplitude but structurally complicated,
- or large in amplitude but rank one.

Several complexity axes should be separated:

$$
d
=
\text{resolved-state dimension},
$$

$$
r
=
\text{context-Hankel rank},
$$

$$
|\Gamma|
=
\text{stack alphabet or rule complexity},
$$

$$
D_{\mathrm{stack}}
=
\text{effective stack depth}.
$$

There is also a fundamental tradeoff between resolved state and explicit memory.

By enlarging the resolved state, one can make the process more nearly Markovian.

By aggressively projecting onto a small resolved space, one pushes more structure into the memory kernel.

Therefore minimizing only

$$
\|K\|
$$

is degenerate.

A better objective is

$$
\begin{aligned}
\min_{\Pi,\Theta}
\quad
&
\mathcal L_{\mathrm{pred}}(\Pi,\Theta)
+
\lambda_x
\dim\operatorname{ran}\Pi
\\
&
+
\lambda_H
\left\|
D_C^{1/2}
H_{\widetilde{\mathcal K}_\Theta}
D_T^{1/2}
\right\|_\ast
\\
&
+
\lambda_{\mathrm{rule}}
\mathcal R_{\mathrm{rule}}(T)
+
\lambda_{\mathrm{depth}}
\mathbb E_\Theta[\text{stack occupancy}]
\\
&
+
\lambda_{\mathrm{stab}}
\Psi_{\mathrm{stab}}(\Theta)
+
\lambda_{\mathrm{orth}}
\Psi_{\mathrm{orth}}(\Pi,\Theta).
\end{aligned}
$$

The prediction term is

$$
\mathcal L_{\mathrm{pred}}
=
\frac{1}{N}
\sum_t
\|g_{t+1}-\widehat g_{t+1}\|_W^2.
$$

The nuclear norm

$$
\|H\|_\ast
$$

acts as a convex surrogate for context-Hankel rank.

For a factorization

$$
H=LR,
$$

we have

$$
\|H\|_\ast
=
\min_{H=LR}
\frac12
\left(
\|L\|_F^2+\|R\|_F^2
\right).
$$

A group-sparsity penalty on $T$ can remove complete rule families or nonterminal directions.

The depth penalty should normally measure expected stack occupancy under the empirical data distribution rather than worst-case depth.

The MZ orthogonality penalty can be written as

$$
\Psi_{\mathrm{orth}}
=
\sum_k
\left\|
\widehat{\mathbb E}
[
\eta_{t+k}g_t^\top
]
\right\|_F^2.
$$

This discourages the residual from retaining predictable structure that should instead be assigned to the learned kernel.

---

## 17. Stability of the recursive kernel

For a positive grammar, let the total-mass fixed point obey

$$
m
=
b+T(m,m).
$$

The linearization around $m$ is

$$
J(m)[\delta m]
=
T(\delta m,m)
+
T(m,\delta m).
$$

A natural subcriticality condition is

$$
\rho(J(m))<1.
$$

This prevents recursive mass from blowing up.

For signed physical kernels, one may instead constrain an absolutely convergent majorizing system.

Thus the recursive-memory analogue of stability in linear realization theory is a contraction or subcriticality condition on the composition algebra.

---

## 18. Behavioral equivalence and approximate similarity

For two pushdown realizations $\mathcal M_1$ and $\mathcal M_2$, define exact behavioral equivalence by

$$
\mathcal M_1
\sim
\mathcal M_2
$$

if

$$
F_{\mathcal M_1}(w)
=
F_{\mathcal M_2}(w)
$$

for every word $w$.

If the Mori projection $\Pi$ is fixed, one may instead compare first-return kernels:

$$
R_{\mathcal M_1}(w)
=
R_{\mathcal M_2}(w).
$$

But the memory kernel itself depends on the resolved/unresolved decomposition.

Two different choices of $\Pi$ may induce different instantaneous terms and different kernels while generating the same observable behavior.

Therefore the most invariant metric is generally placed on the total projected behavior:

$$
d_{\mathrm{beh}}(\mathcal M_1,\mathcal M_2)^2
=
\sum_w
\rho(w)
\left\|
F_{\mathcal M_1}(w)
-
F_{\mathcal M_2}(w)
\right\|_F^2.
$$

The context-sensitive version is

$$
d_{\mathrm{ctx}}(\mathcal M_1,\mathcal M_2)^2
=
\sum_{c,\tau}
\mu_C(c)\mu_T(\tau)
\left\|
\widetilde F_1(c[\tau])
-
\widetilde F_2(c[\tau])
\right\|_F^2.
$$

Thus:

- exact behavioral equivalence gives distance zero,
- approximately prediction-equivalent systems are nearby,
- SVD gives canonical approximate coordinates,
- low-rank truncation gives a principled approximate minimal realization.

---

## 19. A practical proof-of-concept experiment

A useful first experiment would couple a Dyck-2 or Motzkin process to a low-dimensional continuous state.

Generate call and return symbols of two types, and let a low-dimensional recursive grammatical state control a matrix-valued memory kernel:

$$
g_{t+1}
=
Ag_t
+
\sum_{\ell=1}^{t}
\mathcal K(a_{t-\ell+1:t})g_{t-\ell}
+
\epsilon_{t+1}.
$$

Choose $\mathcal K(w)$ to be significant primarily on balanced or irreducibly balanced spans.

Train on sequence lengths up to approximately $20$ or $30$, then test on lengths $50$ to $100$.

Compare four models:

1. finite-lag autoregression or ordinary discrete MZ,
2. Prony-style rational memory,
3. WFA learned from the ordinary word Hankel matrix,
4. tree-Hankel or visibly-pushdown algebraic memory.

Useful diagnostics include

$$
\text{one-step prediction error},
$$

$$
\text{multi-step prediction error},
$$

$$
\text{generalization to longer sequences},
$$

$$
\text{residual orthogonality},
$$

$$
\text{ordinary Hankel spectrum},
$$

$$
\text{tree Hankel spectrum},
$$

$$
\text{recovered grammatical dimension},
$$

and

$$
\text{effective stack depth}.
$$

The expected qualitative signature is:

- ordinary word-Hankel rank grows with nesting depth,
- tree-Hankel rank remains approximately fixed,
- finite-lag and rational models fit the training regime but extrapolate poorly,
- the algebraic model extrapolates recursive structure to substantially greater depth.

This would distinguish genuinely recursive memory from merely long temporal correlation.

---

## 20. What is standard and what is proposed

The following ingredients are standard or close to standard:

- finite-dimensional linear MZ memory admits a finite-rank block-Hankel realization,
- finite word-Hankel rank characterizes weighted finite automata,
- finite tree-Hankel rank characterizes weighted tree automata,
- weighted tree automata provide finite-dimensional composition algebras for weighted context-free structure,
- weighted pushdown systems and weighted CFGs define algebraic formal series,
- visibly pushdown behavior admits an appropriate restricted Hankel characterization,
- latent-variable PCFGs can in restricted settings be learned by spectral methods.

The proposed synthesis is:

1. treat a weighted pushdown system as a Markovian lift of a generalized Langevin equation;
2. identify its MZ kernel with an empty-stack first-return series or self-energy;
3. treat that kernel as a matrix-valued algebraic formal series;
4. lift it to trees or nested contexts;
5. factor the corresponding context Hankel operator;
6. reconstruct the minimal bilinear composition algebra;
7. jointly regularize resolved-state dimension, context-Hankel rank, recursive rule complexity, and stack occupancy;
8. impose Mori–Zwanzig orthogonality as a moment condition during estimation.

In compressed form,

$$
\boxed{
\begin{gathered}
\text{project a weighted pushdown Markov lift onto a finite boundary sector;}\$$4pt]
\text{interpret the resulting MZ first-return kernel as an algebraic series;}\$$4pt]
\text{lift the series to trees or nested contexts;}\$$4pt]
\text{factor its context Hankel operator;}\$$4pt]
\text{reconstruct the minimal bilinear nonterminal algebra.}
\end{gathered}
}
$$

This is the natural context-free analogue of spectral WFA reconstruction.

---

## 21. Conceptual summary

The most important shift is to stop asking for a canonical pushdown automaton directly.

For finite-state systems, spectral learning works because it reconstructs a minimal predictive state space from observable behavior rather than identifying hidden states one by one.

The context-free analogue should do the same.

The primitive object is not the stack configuration. It is the map

$$
\text{recursive fragment}
\longmapsto
\text{its effect in arbitrary future contexts}.
$$

The context Hankel operator collects these effects.

Its rank measures the dimension of the finite recursive composition algebra underlying an otherwise unbounded stack process.

The resulting picture is

$$
\text{hidden Markov state}
\quad\longrightarrow\quad
\text{predictive Hankel state},
$$

and

$$
\text{hidden stack configuration}
\quad\longrightarrow\quad
\text{contextual Hankel state}.
$$

Mori–Zwanzig provides the dynamical interpretation: the stack is unresolved state, while the recursively structured first-return kernel is the observable memory it leaves behind.

That combination gives a plausible route toward a genuinely spectral theory of learned context-free dynamics.

---

*LLM Usage Statement:* This post was written by GPT5.5-Pro based on its conversation with me, then lightly edited for publication formatting by Codex.
