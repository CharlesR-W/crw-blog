---
layout: default
title: About and CV
permalink: /cv/
---

<style>
  .cv-section {
    margin: 0.85rem 0;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.025);
  }

  .cv-section summary {
    padding: 0.85rem 1rem;
    cursor: pointer;
    color: var(--text);
    font-size: 1.05rem;
    font-weight: 650;
  }

  .cv-section summary::marker {
    color: var(--accent);
  }

  .cv-section summary:hover,
  .cv-section summary:focus-visible {
    color: var(--accent);
  }

  .cv-section summary:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 3px;
    border-radius: 5px;
  }

  .cv-section[open] summary {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .cv-section > :not(summary) {
    margin-right: 1rem;
    margin-left: 1rem;
  }

  .cv-section > summary + * {
    margin-top: 1rem;
  }

  .cv-section > :last-child {
    margin-bottom: 1rem;
  }

  @media print {
    .cv-section {
      border: 0;
      break-inside: avoid;
      background: transparent;
    }

    .cv-section > summary {
      display: none;
    }

    .cv-section:not([open]) > :not(summary) {
      display: block !important;
    }
  }
</style>

<script>
  (() => {
    let sectionsClosedBeforePrint = [];

    window.addEventListener("beforeprint", () => {
      const sections = [...document.querySelectorAll(".cv-section")];
      sectionsClosedBeforePrint = sections.filter((section) => !section.open);
      sectionsClosedBeforePrint.forEach((section) => {
        section.open = true;
      });
    });

    window.addEventListener("afterprint", () => {
      sectionsClosedBeforePrint.forEach((section) => {
        section.open = false;
      });
      sectionsClosedBeforePrint = [];
    });
  })();
</script>

<details class="cv-section" markdown="1">
<summary>About</summary>

I'm Charles Renshaw-Whitman, a researcher in AI cognition and alignment.  

Outside of my work, I enjoy studying physics, pharmacology, economics, philosophy, and history.  I am an avid language-learner, and am proficient in Chinese, Latin, and Ancient Greek.  I can read French and Portuguese, and am working on Russian.  I also enjoy running, zhan zhuang, and meditation.

I value hard work, simplicity, curiosity, and integrity.  I believe in a moral imperative, *sed prudentius*, technologically to eliminate intense involuntary suffering.

</details>

## CV

**Charles Renshaw-Whitman**
[Email](mailto:CharlesRW@protonmail.com) **|** [LinkedIn](https://www.linkedin.com/in/charles-renshaw-whitman/) **|** [GitHub](https://github.com/CharlesR-W) **|** [Personal Website and Blog](https://charlesr-w.github.io/crw-blog/)

I study the foundations of interpretability with the aim of building better ontologies for understanding cognition and neural networks.  Tongue-fifty-percent-in-cheek, my guiding aim is to "solve neuroscience".

<details class="cv-section" markdown="1">
<summary>Research profile</summary>

My background spans mechanical engineering, applied physics, sustainable energy technology, and self-directed study in mathematics and machine learning. My research combines technical work in mathematical ML with broader questions from neuroscience, agent foundations, alignment, and cognitive science.

I aim to find ways to make the alignment problem tractable by characterising the actual architecture of learned intelligences - insofar as humans are not argmaxers, I wish to understand why.  I hope that better understanding these constraints will permit us to 'thread the needle' of the alignment problem.

My technical work has drawn on spectral methods, asymptotics, universality, information geometry, and statistical physics.  I have historically focused on asymptotic arguments and universality to try and understand neural learning systems; more recently, I have been thinking about alternative routes to natural ontologies for neural learners.  My more exotic interests in this connection include neural Darwinism and Kantian/Heideggerian philosophies of cognition.

</details>

<details class="cv-section" markdown="1">
<summary>Selected research and writing</summary>

**Published research notes**

* [**Power Laws in NNs: A Possible Mechanism for Inductive Bias towards Sparse Representations**](https://charlesr-w.github.io/crw-blog/Power-Laws-for-Mechinterp/) (2026). Investigates whether heavy-tailed weight spectra provide a mechanism for learned sparse representations.
* [**Coalitional Darwinism**](https://charlesr-w.github.io/crw-blog/Coalitional-Darwinism/) (2026). Uses selection under noise to study selectability, coalitions, and the emergence of higher-level units of agency.
* [**Information in Continua**](https://charlesr-w.github.io/crw-blog/Information-in-Continua-I-Functions-as-Signals/) (2026; three-part research draft). Develops a resolution-centered, kernel-based analogue of information theory for continuous spaces and computations. The underlying ideas are active research; the structure and exposition remain under revision. [Part II](https://charlesr-w.github.io/crw-blog/Information-in-Continua-II-Precision-Bounded-Beliefs/) · [Part III](https://charlesr-w.github.io/crw-blog/Information-in-Continua-III-Sequential-Computations/)

**Work in progress**

* **Free-Body Diagrams for Neural Networks.** An empirical and conceptual project asking whether neural-network subsystems can be studied by holding their surroundings approximately fixed, tested through controlled activation replay and downstream relaxation.
* **Feature Learning in the Genome.** Develops a mathematical correspondence between selection for evolvability in biological genomes and feature learning in neural networks, with proposed applications to interpretability and alignment.
* **Analogy Machines.** An early-stage account of scale-free analogical structure in LLMs and humans, connecting representation learning with cognition, neuroscience, and epistemology.

</details>

<details class="cv-section" markdown="1">
<summary>Research and teaching experience</summary>

**Iliad Fellow**<br>
*Foundations of Interpretability*<br>
Remote, under Dmitry Vaintrob<br>
June 2026 – Present

* Pursuing technical and conceptual approaches to the foundations of interpretability, including work on power laws, neural-network subsystem boundaries, and analogical accounts of representation.
* Primary curriculum owner and instructor for the Iliad Intensive's full-day modules on computational mechanics and statistical field theory.
* Designed the computational-mechanics day around guided mathematical derivations of hidden Markov models, belief-state geometry, transformer representations, predictive state representations, and Hankel methods.

**MATS Scholar and Extension Researcher**<br>
*Foundations of Interpretability*<br>
Remote, under Richard Ngo<br>
January – March 2026; extension ongoing but paused during the Iliad Fellowship

* Developed *A Spectral Theory of Computation*, a final report on a spectral framework for describing information routing through neural-network hidden states.
* During the extension, developed *Coalitional Darwinism* and the forthcoming *Feature Learning in the Genome*, connecting biological selection, learned representations, and interpretability.

**EleutherAI Summer of AI Research (SOAR)**
*Improving Automated Interpretability*
Remote, Under Gonçalo Paulo
August 2025

* Developed pipeline for iterative refinement of natural-language explanations of SAE latent activations.
* Contributed to open-source Delphi automated-interpretability package.

**SERI MATS Scholar**
[*Infra-Bayesianism for People Who Don't Know Measure-Theory*](https://charlesr-w.github.io/crw-blog/Infra-Bayesianism-Distillation/)
Remote, under John Wentworth
June – September 2022

* Studied theoretical work on aligning advanced AI systems to human values.
* Self-taught convex analysis and measure theory to produce an accessible distillation of infra-Bayesianism.

</details>

<details class="cv-section" markdown="1">
<summary>Languages</summary>

* **English:** Native
* **Chinese:** Advanced
* **Latin:** Advanced
* **Ancient Greek:** Upper-intermediate
* **Russian:** Early-intermediate
* **Portuguese:** Upper-intermediate (reading only)
* **French:** Upper-intermediate (reading only)

</details>

<details class="cv-section" markdown="1">
<summary>Education</summary>

**Technische Universiteit Delft**, Delft, Netherlands
*September 2021 – August 2023*
*GPA: 8.51 of 10.0*

* **Degrees**: MSc. in Applied Physics (*cum laude*); MSc. in Sustainable Energy Technology earned simultaneously within the allotted two years
* **Relevant coursework:** Statistical Learning Theory, Deep Reinforcement Learning, Quantum Information (RL-based quantum circuit design)
* **Theses:** *Electrostatic Modelling of Quantum Dot Arrays*; *Reinforcement Learning Methodology for Electricity Market Design*
* **Leadership Roles**:
  * President, TU Delft Debating Society (2022-2023)
  * Secretary, TU Delft Debating Society (2021-2022)

**McGill University**, Montréal, Canada
*September 2017 – April 2021*
*GPA: 3.74 of 4.00*

* **Degree**: B.Eng. in Honors Mechanical Engineering with an Honors Track minor in Physics
* **Honors Thesis:** *Dynamics of Multiheaded Waves in the Rotating Detonation Engine*

</details>

<details class="cv-section" markdown="1">
<summary>Professional experience</summary>

**Machine Learning Researcher**, Makena AI (f.k.a. Neuron3D)
*July 2025 – December 2025*

* Built commercial product using Gaussian splatting to generate 3D models for property management.
* Designed a synthetic-data pipeline using NVIDIA's Difix LoRA to enhance model quality.
* Performed end-to-end design and analysis of machine learning workflow to ensure performance and quality.

**Operations Director**, Del Buono's Bakery
*September 2023 – June 2025*

* Oversaw financial operations, auditing cash flow for four major retail locations.
* Coordinated payroll for over 140 employees.
* Advised the company's leadership during debt restructuring, improving financial sustainability.
* Oversaw a doubling of production in three weeks after the sudden closure of a competitor.

**Propulsion System Lead**, McGill Rocket Team
*September 2019 – June 2020*

* Developed a system-level propulsion simulator to analyze the performance of hot-fire tests.
* Designed test infrastructure for hybrid motor propulsion systems, facilitating accurate measurement of flow properties.
* Managed cross-disciplinary engineering teams in iterative development of test-site infrastructure.

**Engineering Intern**, Argospire Medical
*May 2017 – August 2017*

* Coordinated with medical professionals to identify requirements for a novel respiratory medical device.
* Collaborated to design, prototype, and test iterations of the device.
* Performed numerical simulations of fluid flow to determine performance and measurement characteristics.

</details>

<details class="cv-section" markdown="1">
<summary>Earlier publications</summary>

1. **Renshaw-Whitman, C.**, Zobernig, V., Cremer, J. L., & de Vries, L. (2024). Non-stationarity in multiagent reinforcement learning in electricity market simulation. *Electric Power Systems Research, 235*, Article 110712. [doi:10.1016/j.epsr.2024.110712](https://doi.org/10.1016/j.epsr.2024.110712)
2. Gualtieri, V., **Renshaw-Whitman, C.**, Hernandes, V., & Greplova, E. (2025). QDsim: A user-friendly toolbox for simulating large-scale quantum dot devices. *SciPost Physics Codebases, 46*. [doi:10.21468/SciPostPhysCodeb.46](https://doi.org/10.21468/SciPostPhysCodeb.46)
3. **Renshaw-Whitman, C.**, Mi, X., & Higgins, A. J. (2020). Computational simulation of multi-headed detonation dynamics in rotating detonation engines. *AIAA Conference Proceedings*. [doi:10.2514/6.2020-3877](https://doi.org/10.2514/6.2020-3877)

</details>

<details class="cv-section" markdown="1">
<summary>Technical background</summary>

* **Research methods:** Spectral and kernel methods; asymptotic analysis; information geometry; statistical physics and field theory; convex optimization; stochastic processes; computational mechanics
* **Programming:** Python (PyTorch, NumPy, SciPy), MATLAB, C/C++, Linux/Bash
* **Additional study:** Real analysis, topology, differential geometry, deep learning theory, mechanistic interpretability, representation learning

</details>

<small>*Revised with Claude.*</small>
