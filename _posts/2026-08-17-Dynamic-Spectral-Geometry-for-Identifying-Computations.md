---
title: "Dynamic Spectral Geometry for Identifying Computations"
date: 2026-08-17
tags: [notes, ai]
kind: research note
math: true
---

*This is a theory-stage synthesis. Dynamic Laplacians, Grassmann geometry, information geometry, and the JKO construction are established mathematics; using a Grassmann-bundle dynamic Laplacian to search for persistent neural computations is a proposal. Geometric persistence is not by itself evidence that the recovered object performs a particular computation.*

## Core idea

A useful way to generalize coherent-structure theory beyond fluids is to separate three choices:

1. **What kind of thing can count as an object?**
   This determines a state space, manifold, graph, or fiber bundle $\mathcal X$.

2. **Which changes of such an object count as small or identity-preserving?**
   This determines a metric $g$, possibly together with a measure $\mu$, a connection, or a discrete analogue such as a graph Laplacian.

3. **How are candidate objects transported by the dynamics?**
   This determines a flow or lifted flow
   $$
   F_t:\mathcal X_0\to\mathcal X_t.
   $$

The dynamics pulls the chosen geometry back to the reference time. Spectral geometry then identifies regions of $\mathcal X$ whose boundaries remain unusually cheap under this transported geometry. These are the generalized coherent structures.

The central proposal is to use this as a theory of **persistent computational objects**. Rather than assuming in advance that a computation is a fixed set of neurons, parameters, or coordinates, choose a geometric space of candidate computations and ask which regions or subspaces in that space remain coherent under learning or inference.

The important conceptual point is that the choice of geometry is not merely technical. It defines an **ontology of objecthood**: it specifies which transformations count as harmless changes of representation and which count as genuine deformation.

One typing point will matter later. A point $x\in\mathcal X$ is a **candidate object**. A low-spectrum partition returns a **coherent region** $R\subset\mathcal X$, usually a family of nearby candidate objects. Turning that family into one intervention target requires a separate representative-selection rule, and attaching a computational meaning requires causal or behavioral validation.

---

## 1. Static spectral geometry as the base case

Let $(\mathcal X,g,\mu)$ be a Riemannian manifold with measure $\mu$. The weighted Laplacian is the self-adjoint operator associated with the Dirichlet form

$$
\mathcal E(f)
=
\int_{\mathcal X}
\|\nabla_g f\|_g^2\,d\mu.
$$

Equivalently,

$$
-\langle f,\Delta_{g,\mu}f\rangle_{L^2(\mu)}
=
\mathcal E(f).
$$

In local language,

$$
\Delta_{g,\mu}f
=
\operatorname{div}_{\mu}
\left(\nabla_g f\right).
$$

The low-frequency eigenfunctions minimize variation according to the chosen geometry. Through Cheeger-type correspondences, their level sets approximate regions with small boundary relative to volume.

Thus the general pattern is

$$
\boxed{
\text{geometry}
\longrightarrow
\text{Dirichlet energy}
\longrightarrow
\text{Laplacian}
\longrightarrow
\text{low-boundary objects}.
}
$$

This is already visible in ordinary spectral graph clustering.

---

## 2. Graph community detection is the discrete prototype

For a weighted graph with affinity matrix $W=(w_{ij})$, degree matrix

$$
D_{ii}=\sum_j w_{ij},
$$

and graph Laplacian

$$
L=D-W,
$$

the Dirichlet energy of a signal $f$ on the vertices is

$$
f^\top L f
=
\frac12\sum_{i,j}w_{ij}(f_i-f_j)^2.
$$

A function is cheap when it changes little across strongly weighted edges. Low graph-Laplacian eigenvectors therefore provide relaxed solutions to graph-cut and community-detection problems. Normalized Laplacians modify the measure with which cluster size is evaluated.

This is the finite/discrete version of the Riemannian story:

$$
\sum_{ij}w_{ij}(f_i-f_j)^2
\quad\leftrightarrow\quad
\int \|\nabla f\|^2\,d\mu.
$$

From this perspective, Lagrangian coherent-structure theory is not a fundamentally different idea. It is the **dynamic** version of the same spectral partitioning principle.

For a time-dependent graph $G_t$, if there is a known transport or correspondence operator $T_t$ taking reference vertices to vertices at time $t$, the direct analogue is to pull each graph energy back to the reference vertex set:

$$
\mathcal E^D(f)
=
\frac1T\int_0^T
\langle T_t f,L_t T_t f\rangle\,dt,
$$

or, formally,

$$
L^D
=
\frac1T\int_0^T
T_t^\ast L_t T_t\,dt.
$$

For evolving graphs with explicit temporal copies of vertices, one can instead construct a spacetime or supra-Laplacian that includes both within-time edges and between-time transport edges. Dynamic and inflated dynamic Laplacians for time-evolving networks make this graph/LCS parallel precise.

The graph case is useful conceptually because it makes clear that a Laplacian is an **object-finding operator induced by a notion of local affinity**.

---

## 3. General dynamic spectral geometry

Now let candidate objects live in a manifold $\mathcal X$, equipped at each time with a Riemannian metric $g_t^{\mathrm{obs}}$ and measure $\mu_t$. Let

$$
F_t:\mathcal X_0\to\mathcal X_t
$$

be the transport of candidate objects.

For the differential construction below, assume that the $\mathcal X_t$ are finite-dimensional smooth manifolds, each $g_t^{\mathrm{obs}}$ is positive definite, $F_t$ is a smooth diffeomorphism over the time interval, and $\mu_0$ has a smooth positive density. Fix either Neumann or Dirichlet boundary conditions. Compactness (or an explicit confining restriction) is also needed for the clean discrete spectral picture used here. Without these assumptions the pullback can be degenerate, the inverse diffusion tensors below may not exist, or the low spectrum may not consist of isolated eigenvalues.

Pull the geometry back to the reference space:

$$
\widetilde g_t
=
F_t^\ast g_t^{\mathrm{obs}}.
$$

If the measure is materially transported,

$$
\mu_t=(F_t)_\ast\mu_0,
$$

then everything can be evaluated on the fixed reference space $(\mathcal X_0,\mu_0)$.

Define the **dynamic Dirichlet form**

$$
\boxed{
\mathcal E^D(f)
=
\frac1T\int_0^T
\int_{\mathcal X_0}
\|\nabla_{\widetilde g_t}f\|_{\widetilde g_t}^2
\,d\mu_0\,dt.
}
$$

The corresponding dynamic Laplacian is defined by

$$
-\langle f,\Delta^D f\rangle_{L^2(\mu_0)}
=
\mathcal E^D(f),
$$

hence formally

$$
\boxed{
\Delta^D
=
\frac1T\int_0^T
\Delta_{\widetilde g_t,\mu_0}\,dt.
}
$$

Under these assumptions, this is the natural general construction. A coherent object is a region of $\mathcal X_0$ whose boundary is inexpensive not merely at one instant, but on average after being transported by $F_t$.

The construction can therefore be summarized as

$$
\boxed{
(\mathcal X,g,\mu)
+
F_t
\quad\Longrightarrow\quad
F_t^\ast g
\quad\Longrightarrow\quad
\Delta^D
\quad\Longrightarrow\quad
\text{coherent objects}.
}
$$

This is the part of LCS theory that generalizes most cleanly.

---

## 4. The bundle version

For computations, the candidate object often does not live directly in the physical state space. It is an internal structure attached to each state. The natural setting is then a fiber bundle

$$
\pi:\mathcal E\to M.
$$

A point of the total space is

$$
(x,e),
\qquad
x\in M,\quad e\in\mathcal E_x.
$$

The base dynamics is

$$
\Phi_t:M\to M.
$$

To transport internal objects one needs a **lift**

$$
\widehat\Phi_t:\mathcal E\to\mathcal E
$$

satisfying

$$
\pi\circ\widehat\Phi_t
=
\Phi_t\circ\pi.
$$

Thus

$$
\widehat\Phi_t(x,e)
=
\bigl(\Phi_t(x),\,\text{transport of }e\bigr).
$$

A connection splits the tangent bundle of the total space into horizontal and vertical directions,

$$
T\mathcal E
=
H\mathcal E\oplus V\mathcal E.
$$

Given a metric $g_M$ on the base and a metric $g_V$ on the fibers, one may choose a bundle metric of the schematic form

$$
g_{\mathcal E}
=
\pi^\ast g_M
\oplus
\lambda^2g_V.
$$

The parameter $\lambda$ specifies the relative importance of moving in base space versus deforming the internal object.

The full dynamic bundle Laplacian is then simply

$$
\boxed{
\Delta_{\mathrm{bundle}}^D
=
\frac1T
\int_0^T
\Delta_{\widehat\Phi_t^\ast g_{\mathcal E},\,\mu_0}\,dt.
}
$$

There are two useful regimes:

- **Full bundle coherence:** identify coherent regions in joint $(x,e)$-space.
- **Vertical coherence along a trajectory:** follow $x_t=\Phi_t(x_0)$ and ask which internal fiber objects $e_t$ retain their identity as the base point moves.

The second is especially natural for neural networks: the network parameters move, while the candidate computational subspace is an object in the tangent space attached to the current parameters.

---

## 5. Ordinary Lagrangian coherent structures

Traditional LCS is recovered by taking

$$
\mathcal X=M
$$

to be the material domain and

$$
F_t=\Phi_t
$$

to be the material flow.

For a Euclidean or Riemannian metric, define the finite-time Cauchy--Green operator

$$
C_t
=
(D\Phi_t)^\dagger D\Phi_t.
$$

It satisfies

$$
g_{\Phi_t(x)}
(D\Phi_t v,D\Phi_t w)
=
g_x(v,C_t w).
$$

The pulled-back inverse metric is represented by $C_t^{-1}$. In the volume-preserving Euclidean case,

$$
\boxed{
\Delta_{\mathrm{LCS}}^D f
=
\frac1T\int_0^T
\nabla\cdot
\left(
C_t^{-1}\nabla f
\right)\,dt.
}
$$

Weighted Riemannian versions replace the ordinary divergence by the divergence associated with the transported measure.

The coherent sets are those whose boundaries undergo unusually little stretching under the flow. Froyland's dynamic-isoperimetric construction makes this equivalent, after spectral relaxation, to a low-eigenvalue problem for the dynamic Laplacian.

This gives the template we want to export:

$$
\text{material points}
\rightarrow
\text{candidate computational objects},
$$

$$
D\Phi_t
\rightarrow
\text{transport of computational structure},
$$

$$
C_t
\rightarrow
\text{induced deformation metric},
$$

$$
\Delta_{\mathrm{LCS}}^D
\rightarrow
\text{computational dynamic Laplacian}.
$$

---

## 6. Hamiltonian mechanics: dynamics and object geometry are distinct

Let $(M,\omega)$ be a symplectic phase space and $H:M\to\mathbb R$ a Hamiltonian. The Hamiltonian vector field is defined by

$$
\iota_{X_H}\omega=dH
$$

up to sign convention, and the state-space flow satisfies

$$
\dot x=X_H(x),
\qquad
x_t=\Phi_t(x_0).
$$

For an observable $f$,

$$
\frac{d}{dt}\Phi_t^\ast f
=
\Phi_t^\ast\{f,H\}.
$$

Thus, for autonomous $H$,

$$
\boxed{
\Phi_t^\ast
=
e^{t\,\operatorname{ad}_H},
\qquad
\operatorname{ad}_H f:=\{f,H\},
}
$$

again up to the convention for the Poisson bracket.

The important point for the present theory is that

$$
\boxed{
\omega\text{ generates/constrains the motion, but does not by itself define a Laplacian.}
}
$$

A symplectic form measures oriented phase-space area, not lengths of tangent vectors. To ask which material structures remain coherent, one must additionally choose a Riemannian metric $g$. Hamiltonian flow preserves

$$
\Phi_t^\ast\omega=\omega,
$$

but generally does not preserve $g$. Therefore the pullback metric

$$
\Phi_t^\ast g
$$

can contain nontrivial strain even though the motion is exactly symplectic.

This distinction is conceptually important for computation. The geometry that **generates the dynamics** and the geometry that **defines preservation of an object** need not be the same structure.

---

## 7. Quantum mechanics and density matrices

The same distinction appears especially cleanly in finite-dimensional quantum mechanics.

A density matrix evolves under closed-system dynamics as

$$
\dot\rho
=
-\frac{i}{\hbar}[H,\rho],
$$

with solution

$$
\rho_t
=
U_t\rho_0U_t^\dagger.
$$

Thus the commutator is the infinitesimal generator of the adjoint action, directly paralleling the Poisson-bracket formulation of classical Hamiltonian dynamics.

Density matrices with fixed spectrum form unitary coadjoint orbits. These carry a natural Kirillov--Kostant--Souriau symplectic structure. One can additionally equip density-matrix space with a Riemannian information metric, such as the Bures/quantum-Fisher metric.

There is an instructive limiting case here. A unitarily invariant metric is preserved by

$$
\rho\mapsto U\rho U^\dagger.
$$

For purely closed unitary evolution, the pullback metric is therefore unchanged and the corresponding dynamic Laplacian collapses to the static one:

$$
\Delta^D=\Delta.
$$

This is not a failure of the method. It says that, relative to a geometry that treats unitary conjugation as an exact isometry, closed quantum evolution produces no geometric strain from which to infer nontrivial coherent subobjects.

To obtain a nontrivial quantum coherent-structure problem one would need, for example,

- open-system or nonunitary dynamics;
- a coarse-graining map;
- a task-sensitive metric that is not invariant under all unitaries; or
- a bundle of restricted candidate substructures rather than the full density-matrix orbit.

This illustrates the general principle sharply:

> If the chosen geometry quotients out exactly the transformations produced by the dynamics, the dynamic coherence problem becomes trivial.

---

## 8. Neural networks: the Grassmann bundle of candidate computations

### 8.1 Parameter geometry and training flow

Let neural-network parameters form a manifold

$$
(\Theta,g),
$$

with $g$ taken, for example, to be a **positive-definite** Fisher metric on an identifiable parameter quotient. Raw neural parameterizations are usually redundant, so their Fisher matrix is commonly only positive semidefinite. In that case one must first quotient the null directions or declare a regularized metric such as $g_\lambda=g_F+\lambda g_{\rm ref}$. Regularization changes the geometry of objecthood and is part of the model, not a harmless numerical afterthought.

For natural-gradient flow,

$$
\boxed{
\dot\theta
=
-\operatorname{grad}_g L(\theta).
}
$$

Let

$$
\theta_t=\Phi_t(\theta_0)
$$

and define the tangent map

$$
J_t
=
D\Phi_t(\theta_0):
T_{\theta_0}\Theta\to T_{\theta_t}\Theta.
$$

The covariant variational equation is

$$
\boxed{
\nabla_t J_t
=
-\mathsf H_t J_t,
\qquad
\mathsf H_t
=
\left(\operatorname{Hess}_g L(\theta_t)\right)^\sharp.
}
$$

For Euclidean gradient flow this reduces to

$$
\dot J_t
=
-\nabla^2L(\theta_t)J_t.
$$

Hence the Hessian is the **infinitesimal generator of relative deformation between nearby training trajectories**.

A single parameter path $\theta(t)$ does not by itself determine this tangent transport. One needs the local vector field, the Hessian/Jacobian along the path, or perturbation experiments that estimate $D\Phi_t$.

---

### 8.2 Candidate computations as tangent subspaces

Suppose a candidate computation is represented not by a fixed coordinate subset but by a $k$-dimensional subspace

$$
E\subset T_\theta\Theta.
$$

The natural total space is the Grassmann bundle

$$
\boxed{
\operatorname{Gr}_k(T\Theta)
=
\bigsqcup_{\theta\in\Theta}
\operatorname{Gr}_k(T_\theta\Theta).
}
$$

A point is

$$
(\theta,E).
$$

The training flow has a canonical tangent lift

$$
\boxed{
\widehat\Phi_t(\theta,E)
=
\left(
\Phi_t(\theta),
D\Phi_t(\theta)E
\right).
}
$$

This is the direct analogue of material advection in ordinary LCS, except that the transported object is now a subspace attached to a moving point in parameter space.

The Levi-Civita connection of the chosen positive-definite base metric supplies a horizontal/vertical decomposition of the Grassmann bundle. Vertically,

$$
T_E\operatorname{Gr}_k(T_\theta\Theta)
\simeq
\operatorname{Hom}(E,E^\perp).
$$

Thus an infinitesimal deformation of a candidate computation is a linear map

$$
Z:E\to E^\perp,
$$

i.e. an infinitesimal tilt of the computational subspace into its complement.

The canonical Grassmann metric is

$$
\boxed{
\langle Z,W\rangle_{\mathrm{Gr}}
=
\operatorname{tr}(Z^\dagger W),
}
$$

where the adjoint is taken with respect to $g$.

A natural bundle metric is therefore

$$
\boxed{
g_{\mathrm{bundle}}
=
g^{\mathrm{horizontal}}
\oplus
\lambda^2g_{\mathrm{Gr}}^{\mathrm{vertical}}.
}
$$

The proposed full computational dynamic Laplacian is

$$
\boxed{
\Delta_{\mathrm{comp}}^D
=
\frac1T\int_0^T
\Delta_{\widehat\Phi_t^\ast g_{\mathrm{bundle}},\,\mu_0}\,dt.
}
$$

On a compact restricted domain, its lowest nonconstant eigenfunctions define coherent regions in the joint space of parameter states and candidate computational subspaces. On the full noncompact parameter manifold this displayed operator is only formal until a reference probability measure, domain, and boundary conditions have been specified.

The output is a region $R\subset\operatorname{Gr}_k(T\Theta)$, not automatically one subspace. At a chosen parameter state $\theta$, the fiber slice

$$
R_\theta
=
R\cap\operatorname{Gr}_k(T_\theta\Theta)
$$

is a family of candidate subspaces. A concrete intervention can use a declared representative -- for example a weighted Grassmann Fréchet medoid -- or a smoothly selected section $E(\theta)\in R_\theta$. Which selection is appropriate is an empirical question.

---

### 8.3 Explicit vertical Grassmann deformation tensor

Along a fixed training trajectory, the construction can be reduced to the fibers.

Let

$$
E\in\operatorname{Gr}_k(T_{\theta_0}\Theta)
$$

and let

$$
P:T_{\theta_0}\Theta\to E
$$

be the $g$-orthogonal projector. Set

$$
Q=I-P.
$$

Assume throughout this subsection that $g$ is positive definite and the training flow is a diffeomorphism, so $J_t$ is invertible. Then $C_t$, $A_t$, and the Schur complement $B_t$ below are positive definite and their inverses exist. Define the Fisher Cauchy--Green operator

$$
\boxed{
C_t
=
J_t^\dagger J_t,
}
$$

where $J_t^\dagger$ is the adjoint from $T_{\theta_t}\Theta$ back to $T_{\theta_0}\Theta$.

Define the restriction to the candidate computation,

$$
\boxed{
A_t
=
P C_t P\big|_E:E\to E,
}
$$

and the complementary Schur-complement operator

$$
\boxed{
B_t
=
Q
\left[
C_t
-
C_tP A_t^{-1}P C_t
\right]
Q\big|_{E^\perp}
:
E^\perp\to E^\perp.
}
$$

For a Grassmann tangent vector

$$
Z:E\to E^\perp,
$$

the proposed pulled-back vertical metric acts as

$$
\boxed{
G_t[Z]
=
B_t Z A_t^{-1}.
}
$$

Its inverse is therefore

$$
\boxed{
D_t[Z]
=
G_t^{-1}[Z]
=
B_t^{-1}ZA_t.
}
$$

This $D_t$ is the Grassmann-bundle analogue of $C_t^{-1}$ in ordinary LCS.

Using the canonical Grassmann metric as the reference metric and a fixed smooth reference measure $\mu_0$ on the reference fiber, the vertical dynamic Laplacian is consequently

$$
\boxed{
\Delta_{\mathrm{Gr}}^D f
=
\frac1T\int_0^T
\operatorname{div}_{\mu_0}
\left(
D_t\nabla_{\mathrm{Gr}}f
\right)\,dt.
}
$$

Schematically,

$$
\boxed{
\mathsf H_t
\longrightarrow
J_t
\longrightarrow
C_t
\longrightarrow
D_t
\longrightarrow
\Delta_{\mathrm{Gr}}^D.
}
$$

The Hessian is not itself the dynamic Laplacian. It is the local generator whose finite-time accumulation produces the deformation tensor that enters the dynamic Laplacian. As a sanity check, for $J=\operatorname{diag}(a,b)$ and $E=\operatorname{span}(e_1)$, these formulas give $G=(b/a)^2$ and $D=(a/b)^2$, as expected for the change in the slope coordinate on $\operatorname{Gr}_1(\mathbb R^2)$.

---

### 8.4 The Hessian commutator as the local coherence criterion

The same construction has a simple infinitesimal limit.

Let $P_t$ be the orthogonal projector onto the naturally transported subspace $J_tE$. Under gradient flow,

$$
\boxed{
\nabla_tP_t
=
-[[\mathsf H_t,P_t],P_t].
}
$$

The off-subspace component

$$
(I-P_t)\mathsf H_tP_t
$$

is the instantaneous mixing of the candidate computation with its complement. Since the Riemannian Hessian is self-adjoint,

$$
\boxed{
\ell_t(P_t)
=
\|(I-P_t)\mathsf H_tP_t\|_{\rm HS}^2
=
\frac12\|[\mathsf H_t,P_t]\|_{\rm HS}^2.
}
$$

Hence

$$
[\mathsf H_t,P_t]=0
$$

means that the transported subspace $J_tE$ is an instantaneous invariant subspace of the linearized learning dynamics.

This gives two related notions of persistent computation:

1. **Local leakage criterion**
   $$
   \|[\mathsf H_t,P_t]\|_{\rm HS}^2
   $$
   measures instantaneous failure of a proposed subspace to remain dynamically autonomous.

2. **Dynamic-Laplacian criterion**
   $$
   \Delta_{\mathrm{Gr}}^D
   $$
   identifies finite-time coherent regions in the space of candidate subspaces.

The first is local and pointwise. The second is global, finite-time, and spectral.

This also clarifies the role of basis invariance. A point of the Grassmannian is a subspace rather than a chosen basis. Rotations internal to the subspace are quotiented out before coherence is measured. The geometry therefore encodes the claim that a computation should survive harmless representational rotations while being sensitive to genuine mixing with its complement.

---

## 9. Wasserstein geometry and JKO as a complementary case

Wasserstein geometry is useful because it shows that the geometry can play an even stronger role: it can define not only object similarity, but the dynamics itself.

Let

$$
\mathcal P_2(M)
$$

be the space of probability measures with finite second moment. Formally, a tangent vector at a density $\rho$ can be represented by a potential $\phi$ through

$$
\dot\rho
=
-\nabla\cdot(\rho\nabla\phi),
$$

with Otto metric

$$
\|\dot\rho\|_\rho^2
=
\int_M
|\nabla\phi|^2\rho\,dx.
$$

Given a free-energy functional $\mathcal F[\rho]$, the Jordan--Kinderlehrer--Otto time step is

$$
\boxed{
\rho_{n+1}
=
\arg\min_\rho
\left\{
\mathcal F[\rho]
+
\frac{1}{2\tau}
W_2^2(\rho,\rho_n)
\right\}.
}
$$

In the small-step limit this generates Wasserstein gradient flow; the classical JKO construction recovers an important class of Fokker--Planck equations.

This is almost the conceptual dual of LCS:

- **LCS:** dynamics is given; geometry determines which transported objects count as coherent.
- **JKO:** geometry and an energy functional determine the dynamics by steepest descent.

For computation, this suggests another possible ontology. If a computation is inherently distributional—for example a distribution over latent states, activations, hypotheses, or subroutines—then one can take probability distributions themselves as the candidate object space and use an optimal-transport geometry to decide which changes preserve identity.

One should be cautious about writing a literal Laplace--Beltrami operator on the infinite-dimensional Wasserstein space without further analytic work. The robust point is the structural one:

$$
\boxed{
\text{choice of metric}
\quad\Longleftrightarrow\quad
\text{choice of which redistributions count as small}.
}
$$

A practical finite-data implementation could instead use graph, kernel, entropic-OT, or finite-dimensional manifold approximations.

---

## 10. Unified picture

The main examples can be arranged as follows.

| Setting | Candidate-object space | Geometry defining similarity | Dynamics / lift | Coherence operator |
|---|---|---|---|---|
| Static graph | vertices | edge weights / graph metric | none | graph Laplacian $L$ |
| Time-varying graph | vertices across time | graph + temporal affinities | vertex correspondence / temporal coupling | dynamic or supra-Laplacian |
| Fluid LCS | material manifold $M$ | spatial Riemannian metric | $\Phi_t$ | dynamic Laplacian from $C_t^{-1}$ |
| Hamiltonian mechanics | phase space $M$ | chosen Riemannian metric in addition to $\omega$ | Hamiltonian flow $\Phi_t$ | dynamic Laplacian of pulled-back metric |
| Quantum states | density-matrix orbit | e.g. Bures/QFI metric in addition to KKS structure | $\rho\mapsto U\rho U^\dagger$ | static under fully unitary-invariant geometry; nontrivial after symmetry breaking/open dynamics |
| General bundle | $\mathcal E\to M$ | horizontal + vertical bundle metric | lifted flow $\widehat\Phi_t$ | bundle dynamic Laplacian |
| Neural computation | $\operatorname{Gr}_k(T\Theta)$ | Fisher base metric + Grassmann fiber metric | $(\theta,E)\mapsto(\Phi_t(\theta),D\Phi_tE)$ | Grassmann-bundle dynamic Laplacian |
| Wasserstein/JKO | $\mathcal P_2(M)$ | $W_2$ | gradient flow generated by $\mathcal F$ | geometry primarily generates dynamics; spectral extension is possible but subtler |

The common structure is

$$
\boxed{
\text{choose candidate-object space}
\rightarrow
\text{choose identity-preserving geometry}
\rightarrow
\text{transport that geometry}
\rightarrow
\text{spectrally identify persistent regions}.
}
$$

---

## 11. Interpretation for computation

The proposed computational interpretation is:

> A candidate computation is a point in a chosen geometric space; the spectral construction identifies dynamically persistent families of such candidates.

This deliberately moves the burden away from selecting a preferred coordinate description. A neural computation need not be a fixed set of neurons or weights. It might instead be

- a subspace of tangent directions;
- a subspace of activation space;
- an equivalence class under internal basis rotations;
- a distribution over latent states;
- a graph community;
- a section or coherent region of a fiber bundle.

Once the candidate-object space has been specified, the metric says which perturbations are semantically harmless.

For neural networks, two choices are especially significant:

### Fisher geometry on the base

Using a positive-definite Fisher quotient metric makes parameter displacement sensitive to changes in the represented input-output distribution rather than merely Euclidean parameter distance. If a damped Fisher metric is used instead, the damping reference metric also contributes to this notion of distance.

### Grassmann geometry in the fiber

Using the Grassmannian quotients out arbitrary choices of basis inside a candidate subspace. A candidate is the subspace itself, not its coordinate representation; the spectral output is generally a coherent family of such subspaces.

The resulting dynamic Laplacian then asks for structures that remain distinguishable from their complements under the actual training dynamics.

This gives a geometric interpretation of **forcedness**. A candidate object that the ambient dynamics continually shears into its complement requires continual corrective forcing to maintain a fixed identity. Locally, this appears as

$$
\|(I-P_t)\mathsf H_t P_t\|_{\rm HS}^2.
$$

Globally, it appears as increased dynamic boundary/Dirichlet energy in the transported Grassmann geometry.

---

## 12. What is proposed here

Several ingredients are standard independently:

- graph Laplacians and spectral partitioning;
- dynamic Laplacians and dynamic isoperimetry for LCS;
- weighted Riemannian versions of the dynamic Laplacian;
- canonical differential geometry of Grassmann manifolds;
- Fisher/natural-gradient geometry;
- Wasserstein gradient flows and the JKO construction.

The proposed synthesis is to treat **the choice of candidate computational ontology as the choice of a manifold or fiber bundle**, then use the induced differential geometry and dynamically pulled-back Laplacian to identify persistent candidate families. I have not done an exhaustive novelty search for this exact synthesis; the claim here is that these ingredients fit together naturally, not that no equivalent construction exists in the literature.

In particular, the Grassmann-bundle proposal adds three pieces:

1. the base point $\theta$ moves during training;
2. a candidate computational subspace $E\subset T_\theta\Theta$ is transported by $D\Phi_t$;
3. the relevant coherent-structure operator acts on the Grassmann bundle, or vertically on its fibers along a training trajectory.

The proposed Schur-complement expression above gives an explicit vertical metric for this synthesis. I have checked its basic finite-dimensional consistency, but do not know a primary source deriving that exact formula in this context. The Hessian-commutator criterion

$$
[\mathsf H,P]
$$

is then the infinitesimal limit of a broader finite-time geometric construction rather than an isolated heuristic.

---

## 13. Practical research program

For empirical identification of computations in a neural network:

1. **Choose the candidate-object bundle.**
   The first case to test is
   $$
   \operatorname{Gr}_k(T\Theta),
   $$
   but activation-space Grassmann bundles or bundles of low-rank operators may be more computationally practical.

2. **Choose the base metric and remove degeneracies.**
   Candidates include an identifiable Fisher quotient, a declared damped Fisher metric, generalized Gauss--Newton, activation-space covariance metrics, or an observability/task metric. Verify positive definiteness on the sampled domain.

3. **Estimate tangent transport.**
   For gradient flow this comes from the Hessian variational equation
   $$
   \nabla_tJ_t=-\mathsf H_tJ_t.
   $$
   In practice one can use Hessian-vector products, Jacobian-vector products, or ensembles of perturbed trajectories.

4. **Construct the induced Grassmann diffusion tensor.**
   Compute
   $$
   C_t=J_t^\dagger J_t
   $$
   and from it the vertical operator
   $$
   D_t[Z]=B_t^{-1}ZA_t.
   $$

5. **Approximate the dynamic Dirichlet form.**
   It may be unnecessary to explicitly construct the differential operator. A graph over sampled candidate subspaces can approximate the same geometry.

6. **Solve the low-spectrum problem.**
   Identify low-eigenvalue eigenfunctions or sparse combinations corresponding to coherent regions $R$ of candidate-computation space.

7. **Compare against the local leakage criterion.**
   Test whether spectrally identified structures also have small
   $$
   \|[\mathsf H_t,P_t]\|_{\rm HS}
   $$
   over the relevant interval.

8. **Select and validate an intervention target.**
   At the parameter state of interest, select a representative subspace from the fiber slice $R_\theta$ by a declared rule, or test several representatives for robustness. Perturb, ablate, or intervene along that subspace and its complement. Geometric persistence alone identifies a dynamical family; causal experiments determine whether it corresponds to a computation of interest.

---

## 14. Summary

The main conceptual move is to stop treating Lagrangian coherent structures as a fluid-specific construction.

At a higher level, the theory says:

$$
\boxed{
\text{objects are low-boundary regions defined by a geometry;}
}
$$

$$
\boxed{
\text{persistent objects are low-boundary regions after that geometry is transported by dynamics.}
}
$$

Graphs provide the discrete prototype. LCS provides the classical dynamic realization. Hamiltonian mechanics shows that the structure generating motion and the metric defining objecthood can be different. Quantum mechanics gives an instructive symmetry limit in which an invariant metric makes unitary motion geometrically trivial. Fiber bundles allow the candidate object to be an internal structure attached to a moving base state. The Grassmann bundle then provides a natural space in which neural computations can be represented as basis-independent subspaces transported by learning.

For gradient flow on a Fisher parameter manifold, the chain is

$$
\boxed{
L,g_F
\longrightarrow
\Phi_t
\longrightarrow
J_t=D\Phi_t
\longrightarrow
C_t=J_t^\dagger J_t
\longrightarrow
\widehat\Phi_t^\ast g_{\mathrm{bundle}}
\longrightarrow
\Delta_{\mathrm{comp}}^D.
}
$$

Infinitesimally,

$$
\boxed{
\mathsf H_t
\longrightarrow
[\mathsf H_t,P_t]
}
$$

measures leakage of a transported candidate subspace into its complement. Finite-time dynamic spectral geometry upgrades this local criterion into a global theory of persistent candidate families.

The broad research thesis is therefore:

> **A theory of persistent computational candidates can be built by choosing geometries on spaces of possible objects, then identifying the families that remain coherent under the system's natural dynamics. Their computational interpretation remains an empirical question.**

---

## References

- Edelman, A., Arias, T. A., & Smith, S. T. (1998). *The Geometry of Algorithms with Orthogonality Constraints*. SIAM Journal on Matrix Analysis and Applications, 20(2), 303--353. arXiv:physics/9806030.
- Froyland, G. (2015). *Dynamic Isoperimetry and the Geometry of Lagrangian Coherent Structures*. Nonlinearity, 28(10), 3587--3622. arXiv:1411.7186.
- Froyland, G., & Kwok, E. (2020). *A Dynamic Laplacian for Identifying Lagrangian Coherent Structures on Weighted Riemannian Manifolds*. Journal of Nonlinear Science, 30, 1889--1971. arXiv:1610.01128.
- Froyland, G. (2024/2025). *A Tutorial on the Dynamic Laplacian*. arXiv:2408.04149.
- Froyland, G., Kalia, M., & Koltai, P. (2024; revised subsequently). *Spectral Clustering of Time-Evolving Networks Using the Inflated Dynamic Laplacian for Graphs*. arXiv:2409.11984.
- Jordan, R., Kinderlehrer, D., & Otto, F. (1998). *The Variational Formulation of the Fokker--Planck Equation*. SIAM Journal on Mathematical Analysis, 29(1), 1--17. DOI: 10.1137/S0036141096303359.
- Shi, J., & Malik, J. (2000). *Normalized Cuts and Image Segmentation*. IEEE Transactions on Pattern Analysis and Machine Intelligence, 22(8), 888--905. DOI: 10.1109/34.868688.
- Contreras, I. (2016). *Geometrical Aspects of Quantum Mechanics*. arXiv:1501.00054. [For density matrices as unitary coadjoint orbits and the relation between symplectic and information-geometric structures.]
- Dittmann, J. (1999). *Note on Explicit Formulae for the Bures Metric*. Journal of Physics A. arXiv:quant-ph/9808044.

*LLM Usage Statement:* This post was written by an LLM based on my research direction, then technically reviewed and edited for publication by Codex.
