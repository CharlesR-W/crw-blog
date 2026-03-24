---
title: "A Spectral Theory of Computation"
date: 2026-03-23
math: true
tags: [math]
---

*MATS 9.0 Final Report, under the mentorship of Richard Ngo.  This is a working draft -- comments and corrections welcome.*

---

Any computation that passes through a hidden state -- such as a neural network split at an intermediate layer -- can be decomposed into an encoder (input to hidden) and a decoder (hidden to output).  We develop a spectral theory for this decomposition using kernel canonical correlation analysis, which extracts independent *modes*: channels of information flow from input to output through the hidden state.  Each mode has an encoder strength (how much input information it carries), a decoder strength (how well it predicts the output), and a routing weight (how the encoder mode connects to the decoder mode through the hidden state).  The central object is the *routing matrix* $$R$$, whose entries $$R_{jk}$$ give the overlap between encoder and decoder modes in the hidden-state RKHS.  The routing matrix is gauge-invariant: it depends only on the immediate inputs and outputs of the hidden state, not on how the hidden state is parameterized or how the surrounding computation is organized.  We prove that the routing data $$(\sigma, \tau, R)$$ is the complete invariant of a factored computation up to reparameterization, that truncating to the top modes is optimal in a precise sense, that information-routing strengths can only decay with depth, and that estimation requires a number of samples controlled by the spectral gap.  The output in the decomposition is a free parameter: replacing it with any behavioral measure (e.g., a truthfulness probe, a toxicity score) gives a behavior-specific routing matrix, and these compose under post-processing.

[Read the full paper (PDF).]({{ site.baseurl }}/assets/spectral-theory-of-computation.pdf)

---

*Written with Claude.*
