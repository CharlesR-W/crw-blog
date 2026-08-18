---
title: "Approximate Symmetry and Factorization of Discrete Neural Computations"
date: 2026-08-17
tags: [notes, ai]
kind: research note
math: true
---

*This is a theory-stage research note. The operator-algebraic ingredients are standard; their use as diagnostics for Voronoi-quantized neural computation is a proposal, not an empirical result.*

## Motivation

Suppose that intermediate neural activations admit a useful coarse discretization. In the motivating case, residual-stream activations are assigned to cells of a Voronoi partition,

$$
q:h\mapsto c\in\mathcal C,
$$

where $\mathcal C=\{1,\dots,N\}$ is a finite codebook.

The resulting object can be treated as a discrete computational state space. Rather than trying to identify "circuits" directly in weights or individual neurons, we can study the **algebra of transformations induced on these coarse states**.

This provides a natural framework for asking:

- Which distinctions between coarse states matter computationally?
- Which states or transformations are approximately interchangeable?
- Does the computation decompose into approximately independent factors?
- Can the same computation be described at several resolutions?
- How close is the observed computation to one possessing an exact symmetry or tensor-product structure?

The main mathematical tools are operator algebras, commutants, approximate symmetries, and approximate tensor factorizations.

---

## 1. From a discrete code to an operator algebra

Associate to the coarse code $\mathcal C$ the formal vector space

$$
\mathcal H_{\mathcal C}
=
\operatorname{span}\{|c\rangle:c\in\mathcal C\}
\simeq \mathbb C^N.
$$

The network induces transitions between coarse states. Depending on the experiment, these may represent layer-to-layer dynamics, token-conditioned transformations, attention/MLP updates, or more abstract computational primitives.

For a context or operation $\alpha$, define

$$
P_\alpha(j|i)
=
\Pr(c_{\mathrm{out}}=j
\mid
c_{\mathrm{in}}=i,\alpha).
$$

The family $\{P_\alpha\}$ generates a forward transition algebra

$$
\boxed{
\mathcal A_0
=
\operatorname{alg}\{P_\alpha\}.
}
$$

Here $\operatorname{alg}$ includes linear combinations and finite products (and, by convention, the identity), but not necessarily adjoints. This distinction matters later: $\mathcal A_0$ records forward compositions of the estimated transitions, while its adjoint-closed envelope is a different object.

The important point is that linearity here is representational rather than an assumption that the neural network is itself linear. Any finite-state computation can be represented linearly on the vector space of functions or formal distributions over its states.

The interesting question is whether this coarse representation is sufficiently low-dimensional and approximately closed to expose useful structure.

---

## 2. The commutant, and what it measures

A symmetry transformation should be an invertible, structured operator $U$ -- for example a permutation or unitary -- satisfying

$$
[U,P_\alpha]=0
\qquad
\forall\alpha.
$$

The ambient linear space containing all such transformations is the **commutant**

$$
\mathcal A_0'
=
\{X:[X,A]=0\ \forall A\in\mathcal A_0\}.
$$

Permutation matrices in $\mathcal A_0'$ correspond directly to relabelings of coarse states that leave the computation unchanged. Unitaries in $\mathcal A_0'$ form the full unitary symmetry group. More general commutant elements include invariant projectors and intertwiners between equivalent sectors. Those elements diagnose degeneracy or reducibility, but a singular projector is not itself a symmetry transformation. This is the first distinction to keep straight: **the commutant contains the symmetries, but not everything in it is a symmetry**.

### From exact commutation to a calibrated spectrum

For empirical systems exact commutation will generally be too restrictive. To turn commutation into a numerical diagnostic, first choose an inner product $G$ on the coarse state space -- uniform, occupancy-weighted, or otherwise justified by the experiment -- and use its induced Hilbert--Schmidt norm on operators. The corresponding adjoint is

$$
X^\dagger=G^{-1}X^\ast G.
$$

Normalize the generators as $\widehat P_\alpha=P_\alpha/\|P_\alpha\|_G$, choose context weights $w_\alpha$ with $\sum_\alpha w_\alpha=1$, and define

$$
\mathcal C(X)
=
\big(
w_1^{1/2}[X,\widehat P_1],\ldots,
w_m^{1/2}[X,\widehat P_m]
\big),
$$

with energy

$$
E_{\rm sym}(X)
=
\sum_\alpha
w_\alpha\|[X,\widehat P_\alpha]\|_G^2,
\qquad \|X\|_G=1.
$$

Equivalently, study the positive operator

$$
\mathcal C^\dagger\mathcal C.
$$

The normalization is not cosmetic. Rescaling a generator, duplicating a context, or changing the occupancy metric otherwise changes the eigenvalues without changing the exact commutant. With the choices fixed:

- zero modes are exact commutant elements;
- after removing the unavoidable scalar mode $I$, small eigenvalues identify **approximate commutant directions**;
- restricting $X$ to a structured class -- permutation matrices, unitaries, or the represented generators of a proposed Lie group -- turns the same energy into a score for breaking that particular symmetry.

For a specified transformation $U$ that is unitary with respect to $G$, for example, a dimensionless breaking score is

$$
b(U)
=
\frac{
\sum_\alpha w_\alpha
\|[U,\widehat P_\alpha]\|_G^2
}{4}.
$$

With the present normalization $0\le b(U)\le1$. This answers a targeted question: how badly does the observed computation violate the candidate symmetry $U$? By contrast, diagonalizing $\mathcal C^\dagger\mathcal C$ asks an exploratory question: which operator directions are closest to the centralizer? Its low modes should not be called group symmetries until their eigenoperators have been checked to be close to a structured transformation.

### Symmetry breaking as spectral splitting

Suppose $P_\alpha^{(0)}$ commute with a swap $S$, and the observed operators are

$$
P_\alpha^{(\varepsilon)}
=
P_\alpha^{(0)}+\varepsilon V_\alpha.
$$

Then

$$
E_{\rm sym}^{(\varepsilon)}(S)
=
\varepsilon^2
\sum_\alpha w_\alpha
\frac{\|[S,V_\alpha]\|_G^2}
{\|P_\alpha^{(0)}\|_G^2}
+O(\varepsilon^3)
$$

for nonzero $P_\alpha^{(0)}$; the change in normalization contributes only a term proportional to $P_\alpha^{(0)}$, which still commutes with $S$. The exact $S$-mode at $\varepsilon=0$ therefore lifts away from zero quadratically in the commutator energy. More generally, an exact $d$-dimensional commutant produces $d$ zero singular directions; perturbations split some of them into low but nonzero modes. Tracking that splitting across training time or models is the cleanest sense in which the spectrum quantifies symmetry breaking.

There is a conditioning caveat. If $\gamma$ is the smallest nonzero singular value of $\mathcal C$ and $\Pi$ projects onto its exact kernel, then

$$
\|X-\Pi X\|_G
\le
\frac{\|\mathcal C(X)\|_G}{\gamma}.
$$

A small residual licenses a nearby exact commutant element only when the gap $\gamma$ is not itself tiny. In data, this means reporting the spectral gap and comparing low modes against bootstrap or held-out estimation noise rather than declaring every small eigenvalue a discovered symmetry.

This replaces the binary question

$$
\text{"does the computation have symmetry }G\text{?"}
$$

with the more useful question

$$
\boxed{
\text{"which commutant directions survive, and at what scale are they broken?"}
}
$$

---

## 3. Incorporating the geometry of the residual code

The discrete transition structure need not be analyzed independently of the original residual geometry.

If $v_i$ is the centroid of cell $i$, define the centroid Gram matrix

$$
K_{ij}
=
\langle v_i,v_j\rangle.
$$

A symmetry may then be required to preserve both computation and representation geometry:

$$
E(X)
=
\lambda_K\|[X,K]\|^2
+
\sum_\alpha
\lambda_\alpha
\|[X,P_\alpha]\|^2.
$$

For permutation-like transformations, the geometric condition is equivalently

$$
XKX^\dagger\approx K.
$$

This allows one to distinguish:

- geometric symmetries that the computation breaks;
- computational symmetries not apparent in raw residual geometry;
- transformations respecting both.

The choice of norm should ideally be tied to an intrinsic Gram or occupancy metric rather than arbitrary coordinates.

---

## 4. Symmetry is not the same as factorization

A nontrivial global commutant is useful, but it is not sufficient for discovering subsystems.

A computation can factor as

$$
\mathcal H
\simeq
\mathcal H_A\otimes\mathcal H_B
$$

while the full computational algebra is

$$
\mathcal A
=
\operatorname{End}(\mathcal H_A)
\otimes
\operatorname{End}(\mathcal H_B)
=
\operatorname{End}(\mathcal H),
$$

whose commutant is only

$$
\mathcal A'=\mathbb CI.
$$

Thus meaningful factor structure can exist even when there are no nontrivial global symmetries.

The more general problem is therefore to identify **approximately commuting subalgebras**.

---

## 5. Approximate tensor-product structure

Suppose the apparent cell label secretly represents several latent variables,

$$
c\leftrightarrow(z_1,\ldots,z_k),
$$

so that

$$
\mathcal H_{\mathcal C}
\approx
\mathcal H_1\otimes\cdots\otimes\mathcal H_k.
$$

A very strong factorization would have

$$
P_\alpha
\approx
P_{\alpha,1}\otimes\cdots\otimes P_{\alpha,k}.
$$

A more realistic form is a local-plus-interaction expansion,

$$
L_\alpha
=
\sum_i L_{\alpha,i}
+
\sum_{i<j}L_{\alpha,ij}
+
\sum_{i<j<k}L_{\alpha,ijk}
+\cdots,
$$

where

$$
L_{\alpha,i}
=
I\otimes\cdots\otimes
\widetilde L_{\alpha,i}
\otimes\cdots\otimes I.
$$

The norms of the higher-order terms then quantify coupling between latent computational variables.

For example,

$$
\epsilon_{\rm int}
=
\frac{
\sum_{\alpha,i<j}\|L_{\alpha,ij}\|^2+\cdots
}{
\sum_\alpha\|L_\alpha\|^2
}
$$

provides a graded notion of subsystem independence.

The resulting coefficients define an effective interaction graph or hypergraph over the latent factors.

---

## 6. Approximately commuting computational subalgebras

An intrinsic formulation is to search for subalgebras

$$
\mathcal A_1,\ldots,\mathcal A_k
$$

such that

$$
[\mathcal A_i,\mathcal A_j]
\approx0
\qquad
(i\neq j),
$$

while together they explain most of the observed transition algebra.

For an exact bipartite factorization,

$$
\mathcal A_A
=
\operatorname{End}(\mathcal H_A)\otimes I,
$$

$$
\mathcal A_B
=
I\otimes\operatorname{End}(\mathcal H_B),
$$

and therefore

$$
[\mathcal A_A,\mathcal A_B]=0.
$$

This suggests defining factor discovery as an optimization over candidate subalgebras, balancing:

1. mutual commutation;
2. explanatory power for the observed operators;
3. simplicity or low dimensionality;
4. small residual interaction terms.

In this language, a computational subsystem is not fundamentally a set of neurons. It is a factor or subalgebra on which a coherent family of operations acts approximately locally.

---

## 7. Operator-Schmidt decomposition

Given a candidate tensor decomposition

$$
\mathcal H=\mathcal H_A\otimes\mathcal H_B,
$$

any operator can be written as

$$
P
=
\sum_r
\sigma_r A_r\otimes B_r,
$$

where $A_r$ and $B_r$ form orthonormal operator families.

This is the **operator-Schmidt decomposition**.

Its singular values $\sigma_r$ quantify how many product-operator terms are needed to represent $P$. They measure **separability complexity**, not locality by themselves. A single product $A\otimes B$ has operator-Schmidt rank one even when it acts nontrivially on both factors.

A nearly local transformation should be dominated by terms of the form

$$
A\otimes I
$$

and

$$
I\otimes B,
$$

with relatively little weight in genuinely joint terms. A direct interaction score should therefore project onto the local operator subspace

$$
\mathcal L
=
\operatorname{End}(\mathcal H_A)\otimes I
+
I\otimes\operatorname{End}(\mathcal H_B)
$$

and measure

$$
\epsilon_{\rm joint}(P)
=
\frac{\|P-\Pi_{\mathcal L}P\|^2}{\|P\|^2}.
$$

Thus the operator-Schmidt spectrum is a useful complementary diagnostic for a proposed factorization, while $\epsilon_{\rm joint}$ measures the more specific claim that the operator is local-plus-local.

---

## 8. Discovering factor coordinates directly from the cells

A factorization should ideally simplify both the cell geometry and the transition dynamics.

Seek coordinates

$$
c
\mapsto
(z_1(c),\ldots,z_k(c))
$$

with several possible signatures.

### Product transition graph

If the cell graph approximately factorizes as

$$
G_{\mathcal C}
\approx
G_1\square G_2,
$$

its Laplacian should approximately have the Kronecker-sum form

$$
L
\approx
L_1\otimes I
+
I\otimes L_2.
$$

Consequently, its spectrum approximately obeys

$$
\lambda_{ij}
\approx
\lambda_i^{(1)}
+
\lambda_j^{(2)}.
$$

### Commuting coordinate observables

Seek self-adjoint (or, more generally, normal) observables

$$
Z_1,\ldots,Z_k
$$

that approximately commute,

$$
[Z_i,Z_j]\approx0,
$$

and whose joint approximate eigenvalues distinguish the cells. Exact commuting normal operators are simultaneously diagonalizable; in the approximate case, the quality and stability of a joint basis must be checked rather than assumed from a small commutator alone.

The joint spectrum then supplies latent coordinates

$$
c\leftrightarrow
(z_1,\ldots,z_k).
$$

### Low interaction complexity

After rewriting the transition operators in these coordinates, test whether they admit a sparse local-plus-interaction expansion.

The same factorization should ideally explain both the static code geometry and the dynamic operator algebra.

---

## 9. Relation to finite-dimensional $*$-algebras

For especially clean decomposition theory, one can enlarge the computational algebra to the unital $*$-algebra generated by the transition operators,

$$
\mathcal B
=
\operatorname{alg}
\left(
I,
P_1,P_1^\dagger,
\ldots,
P_m,P_m^\dagger
\right).
$$

A unital $*$-algebra is simply an operator algebra that:

- contains the identity;
- is closed under addition and multiplication;
- is closed under Hermitian adjoint.

The adjoint depends on the chosen inner product, so this construction incorporates the metric $G$ selected above. Adjoining the reverse-looking operations $P_\alpha^\dagger$ can materially enlarge a nonnormal forward transition algebra. The envelope $\mathcal B$ is therefore an analytically convenient observational algebra, but it is not automatically the same thing as the semigroup of physically available forward computations $\mathcal A_0$.

Finite-dimensional unital $*$-algebras admit a particularly simple decomposition:

$$
\boxed{
\mathcal H
=
\bigoplus_\lambda
V_\lambda\otimes M_\lambda,
}
$$

such that

$$
\boxed{
\mathcal B
=
\bigoplus_\lambda
\operatorname{End}(V_\lambda)
\otimes
I_{M_\lambda},
}
$$

and

$$
\boxed{
\mathcal B'
=
\bigoplus_\lambda
I_{V_\lambda}
\otimes
\operatorname{End}(M_\lambda).
}
$$

This is the relevant finite-dimensional Wedderburn structure.

The space $V_\lambda$ is an irreducible computational sector. The **multiplicity space** $M_\lambda$ counts equivalent copies of that sector: the computation acts identically on each copy and is therefore blind to the multiplicity coordinate.

The algebra and its commutant exchange these two roles.

---

## 10. Exactly when the bicommutant is enough

Now the hypotheses can be stated without sleight of hand. Let $\mathcal H$ be a finite-dimensional complex Hilbert space, and let $\mathcal B\subseteq\operatorname{End}(\mathcal H)$ be a concrete algebra that contains $I$ and is closed under the adjoint defined by $G$. Then

$$
\boxed{
\mathcal B''=\mathcal B.
}
$$

Thus, in this setting, the full collection of operators commuting with $\mathcal B$ determines $\mathcal B$ itself. Finite dimensionality makes all the relevant operator topologies equivalent, so no extra closure hypothesis is needed.

Each condition is doing work. Consider the unital algebra of upper-triangular matrices

$$
\mathcal T_2
=
\left\{
\begin{pmatrix}
a&b\\
0&d
\end{pmatrix}
:a,b,d\in\mathbb C
\right\}.
$$

It is finite-dimensional but not adjoint-closed. Its commutant is only $\mathbb CI$, so

$$
\mathcal T_2''=M_2(\mathbb C)\neq\mathcal T_2.
$$

Likewise, dropping the identity can make the bicommutant add missing diagonal operations. In infinite dimensions, the bicommutant of a unital $*$-algebra is its strong-operator (equivalently weak-operator) closure; equality requires the represented algebra already to be a von Neumann algebra.

So there are two scientifically different claims:

1. The commutant determines the adjoint-closed observational algebra $\mathcal B$ exactly under the finite-dimensional hypotheses above.
2. It determines the raw forward algebra $\mathcal A_0$ only if $\mathcal A_0$ is itself bicommutant-closed. This is not automatic for stochastic transition operators.

Conceptually,

$$
\mathcal B
=
\text{operations in the adjoint-closed observational envelope},
$$

while

$$
\mathcal B'
=
\text{degrees of freedom those operations cannot distinguish}.
$$

For $\mathcal B$, the bicommutant relation expresses a duality between computational action and computational equivalence. Calling elements of $\mathcal B$ operations the network *can perform* is safe only if adjoint closure has a physical justification; otherwise they are operations in the chosen observational envelope.

For empirical systems, there is no generic theorem saying that an approximate commutant reconstructs a nearby exact algebra. Recovery depends on spectral gaps, conditioning, the norm, and the structured model class. The practical test is stability under resampling and controlled synthetic perturbations.

---

## 11. Multiscale or "zoomable" computation

The discrete representation should not necessarily be fixed at one resolution.

Introduce a hierarchy of partitions

$$
\Pi_0
\prec
\Pi_1
\prec
\cdots
\prec
\Pi_L,
$$

where $\Pi_0$ groups many Voronoi cells into coarse macrostates and successive levels refine selected distinctions.

At each scale there is a computational state space

$$
\mathcal H^{(\ell)}
$$

and corresponding transition algebra

$$
\mathcal A^{(\ell)}.
$$

Because these algebras act on spaces of different dimensions, they are not literally nested without additional embeddings. The natural structure is instead a family of coarse-graining maps

$$
R_{\ell+1\to\ell}:
\mathcal H^{(\ell+1)}\to\mathcal H^{(\ell)}
$$

that approximately intertwine the transition operators:

$$
R_{\ell+1\to\ell}P_\alpha^{(\ell+1)}
\approx
P_\alpha^{(\ell)}R_{\ell+1\to\ell}.
$$

The intended semantics is that a coarse rule such as

$$
A\to B
$$

may refine into

$$
A=A_0\cup A_1,
$$

with

$$
A_0\to B,
\qquad
A_1\to C.
$$

Thus the coarse computation is a quotient that suppresses conditional exceptions.

---

## 12. Lumpability as a criterion for refinement

A natural criterion for whether a coarse partition is computationally adequate is approximate **lumpability**.

Suppose cells $i,j$ are grouped into the same macrostate $A$. They can be treated as equivalent at the coarse level only if, for every relevant context $\alpha$, they have approximately the same transition probabilities into every macrostate $B$:

$$
\sum_{k\in B}P_\alpha(k|i)
\approx
\sum_{k\in B}P_\alpha(k|j).
$$

Define, for example,

$$
E_{\rm lump}(A)
=
\sum_\alpha w_\alpha
\sum_{i,j\in A}
\sum_B
\left|
P_\alpha(B|i)-P_\alpha(B|j)
\right|^2.
$$

If this error is small, the coarse state $A$ is computationally sufficient.

If it is large, $A$ hides an important conditional distinction and should be refined.

This gives an adaptive notion of zooming:

$$
\boxed{
\text{coarse quotient}
\rightarrow
\text{detect failure of lumpability}
\rightarrow
\text{refine only where needed}.
}
$$

One can therefore represent a computation at multiple scales without committing to one globally uniform cell size.

---

## 13. Proposed experimental pipeline

Given a Voronoi-quantized residual stream:

1. **Construct the coarse state space**
   $$
   h\mapsto c\in\mathcal C.
   $$

2. **Estimate contextual transition operators**
   $$
   P_\alpha.
   $$

3. **Construct the transition algebra**
   $$
   \mathcal A_0=\operatorname{alg}\{P_\alpha\}.
   $$

4. **Search for approximate commutant directions**
   by diagonalizing
   $$
   \mathcal C^\dagger\mathcal C,
   \qquad
   \mathcal C(X)=([X,P_\alpha])_\alpha.
   $$

5. **Optionally include residual geometry**
   through the centroid Gram matrix $K$.

6. **Search for latent factor coordinates**
   using product-graph structure, commuting observables, or direct optimization of tensor decompositions.

7. **Measure factor quality**
   using operator-Schmidt spectra and the magnitude of interaction terms.

8. **Identify approximately commuting subalgebras**
   corresponding to candidate computational subsystems.

9. **Construct a multiscale hierarchy**
   by merging computationally equivalent cells and refining macrostates when lumpability fails.

10. **Compare the resulting algebraic structures across layers, contexts, models, or training time.**

The ultimate object is therefore not merely a clustering of neural activations, but a coarse-grained **algebraic model of computation**.

---

## 14. Conceptual summary

The central proposal is

$$
\boxed{
\text{residual activations}
\rightarrow
\text{discrete cells}
\rightarrow
\text{transition operators}
\rightarrow
\text{computational algebra}.
}
$$

From this algebra one can extract several complementary kinds of structure:

$$
\boxed{
\begin{aligned}
\text{commutant}
&\rightarrow
\text{symmetries and computational degeneracies},\\
\text{calibrated low commutator modes}
&\rightarrow
\text{approximate centralizer directions},\\
\text{commuting subalgebras}
&\rightarrow
\text{candidate subsystems},\\
\text{tensor decomposition}
&\rightarrow
\text{factored computational variables},\\
\text{interaction terms}
&\rightarrow
\text{coupling between factors},\\
\text{partition filtration}
&\rightarrow
\text{multiscale computation}.
\end{aligned}
}
$$

The broader aim is to replace a brittle ontology of exact circuits or exact symbolic states with a graded description in which symmetries, subsystems, factorization, and abstraction can all hold approximately and at scale-dependent resolution.

This suggests a possible bridge between apparently continuous neural computation and discrete computational descriptions: the relevant discrete objects need not be individual neurons or exact symbolic states, but **coarse computational equivalence classes whose transition algebra possesses approximately factored structure**.

---

## References

- V. S. Sunder, [*Finite-dimensional $C^*$-algebras*](https://www.imsc.res.in/~knr/mathasp14/ss_notes.pdf). See especially the double-commutant theorem and finite-dimensional structure theorem.
- M. B. Hastings, [*Making Almost Commuting Matrices Commute*](https://arxiv.org/abs/0808.2474). This illustrates why approximate-commutation claims require explicit operator classes and norms rather than a generic appeal to the exact theorem.

*LLM Usage Statement:* This post was written by an LLM based on my research direction, then technically reviewed and edited for publication by Codex.
