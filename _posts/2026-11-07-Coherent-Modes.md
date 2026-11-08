---
title: "Coherent Modes: a Spectral Language for What a Network Does to Its Activations"
date: 2026-11-07
tags: [notes, ai]
kind: research note
math: true
---

*A theory and experiment plan, not results: nothing has been run yet. The ingredients (diffusion maps, Sinkhorn scaling, Froyland's coherent sets, kernel CCA / VAMP) are established mathematics; putting them on one shared index set to describe trained networks is the proposal.*

**Repo:** [github.com/CharlesR-W/CoherentModes](https://github.com/CharlesR-W/CoherentModes). If you want to engage with the math, start with [`PREREQUISITES.md`](https://github.com/CharlesR-W/CoherentModes/blob/main/PREREQUISITES.md), a short map of what to study and in what order (written so you can hand it to your own agents).

The short version: treat every input or token position the network sees as a *site*, shared across all layers. Each layer's geometry becomes a random walk on sites (cosine kernel, Sinkhorn-normalized so all layers share one stationary measure), and the SVD of a product of two layers' walks gives *coherent modes*: the distinctions the network keeps from one layer to the next, with depth playing the role of time. Modes map back to activation directions, units and gradients expand exactly in them, and a temperature knob interpolates from PCA / linear CKA through a possible dictionary-like regime. No sparsity assumption, nothing trained on top of the model, and nothing transformer-specific. Every claim in the theory is tagged as a theorem, conditional, or hypothesis, and the experiment plan runs from toy models of superposition and grokking through HMM belief states to Pythia.

Related earlier notes: [Dynamic Spectral Geometry for Identifying Computations]({{ site.baseurl }}/Dynamic-Spectral-Geometry-for-Identifying-Computations/) and [Mori–Zwanzig, Hankel Geometry, and Context-Free Memory]({{ site.baseurl }}/Mori-Zwanzig-Hankel-Geometry-and-Context-Free-Memory/).

---

## The README, live from GitHub

<div id="cm-readme" style="border-left: 3px solid var(--muted, #999); padding-left: 1em;">
<p><em>Loading the README from GitHub… If it does not appear, read it <a href="https://github.com/CharlesR-W/CoherentModes#readme">on GitHub</a>.</em></p>
</div>

<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script>
(function () {
  var REPO = "https://github.com/CharlesR-W/CoherentModes";
  var RAW = "https://raw.githubusercontent.com/CharlesR-W/CoherentModes/main/README.md";
  var el = document.getElementById("cm-readme");
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function typeset() {
    var tries = 0;
    (function wait() {
      if (window.MathJax && MathJax.typesetPromise && MathJax.startup && MathJax.startup.promise) {
        MathJax.startup.promise.then(function () { return MathJax.typesetPromise([el]); });
      } else if (tries++ < 50) { setTimeout(wait, 200); }
    })();
  }
  fetch(RAW, { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then(function (md) {
      md = md.replace(/^# .*\n/, "");                       // drop the repo title; the post has its own
      var math = [];                                         // protect math from markdown emphasis
      md = md.replace(/\$\$[\s\S]+?\$\$|\$[^$\n]+?\$/g, function (m) { math.push(m); return "@@CMMATH" + (math.length - 1) + "@@"; });
      var html = marked.parse(md);
      html = html.replace(/@@CMMATH(\d+)@@/g, function (_, i) { return esc(math[+i]); });
      el.innerHTML = html;
      el.querySelectorAll("a[href]").forEach(function (a) {
        var h = a.getAttribute("href");
        if (!/^(https?:|mailto:|#)/.test(h)) a.href = REPO + "/blob/main/" + h.replace(/^\.\//, "");
      });
      typeset();
    })
    .catch(function () { /* keep the fallback link */ });
})();
</script>

---

*LLM Usage Statement: the theory, experiment plan, README and this note were written by Claude models (Fable 5.1, Opus 5.5) from my ideas and a design interview, with GPT models doing adversarial mathematical review. The README section above is fetched from the repo on each page load, so it stays in sync.*
