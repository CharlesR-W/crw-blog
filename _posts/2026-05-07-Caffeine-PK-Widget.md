---
title: "Caffeine in the Body — A PK Widget"
date: 2026-05-07
motivation: "How much caffeine is still in your body when you go to bed?  And how does that change if you swap one big morning coffee for two smaller ones?  The shape of the answer is a saturating-then-decaying curve, and the parameters are a few half-lives and one body-weight scaling."
background: "One-compartment pharmacokinetics with first-order absorption.  The model is a textbook in two equations; the interesting bits are the timing decisions you make on top of it."
llm: "Claude"
tags: [widget]
math: true
---

# Caffeine in the Body — A PK Widget

Drag the blue pill onto the timeline to drop a 100 mg bolus.  Drag boluses to retime them.  Double-click to remove.  The dashed line is bedtime; tweak it to your actual schedule.

<iframe src="{{ '/assets/widgets/caffeine.html' | relative_url }}"
        style="width:100%; height:680px; border:0; border-radius:12px; background:#000;"
        loading="lazy"
        title="Caffeine PK widget"></iframe>

## What the model is

One-compartment PK with first-order absorption.  A single bolus of dose $D$ taken at $t=0$ gives body load

$$m(t) = D \cdot \frac{k_a}{k_a - k_e}\bigl(e^{-k_e t} - e^{-k_a t}\bigr)$$

with $k_a$ the absorption rate (peak around 50 minutes for caffeine) and $k_e = \ln 2 / t_{1/2}$ the elimination rate.  Caffeine's half-life sits near 5 hours in a healthy non-smoker; smokers and heavy CYP1A2 inducers run shorter, oral contraceptives and pregnancy run longer.  The model is linear, so multiple doses superpose: every cup is its own little impulse response, and the visible curve is their sum.

The y-axis is mg/kg in body, not mg.  That is what makes body weight matter — the same 100 mg cup is a 1.4 mg/kg dose at 70 kg and a 2.0 mg/kg dose at 50 kg.  Typical ergogenic doses sit at 1–3 mg/kg; the LD50 in the literature is around 150–200 mg/kg.

## Paraxanthine and "effective" caffeine

About 84% of caffeine is demethylated to paraxanthine (1,7-dimethylxanthine) by CYP1A2.  Paraxanthine is itself a stimulant with a similar mechanism (adenosine receptor antagonism) and a half-life of about 3.1 hours.  So your subjective "caffeine" is really the sum of both compounds — flip on the *Effective caffeine* toggle to add a configurable share of paraxanthine to the body load.

The cascade is a two-compartment ODE,

$$\frac{dm_\text{par}}{dt} = f \cdot k_e \cdot m_\text{caf}(t) - k_\text{par} m_\text{par},\qquad f \approx 0.84$$

which the widget integrates with a one-minute Euler step.

## Things to play with

- **The two-coffee question.**  Drop one bolus at 8:00 and a second at noon.  Then move the noon dose earlier and watch what happens to the bedtime number.  Most of the bedtime caffeine you regret comes from the *afternoon* cup, not the morning one.
- **Half-life sensitivity.**  Crank the half-life from 5 to 8 hours (a real number for some people).  Bedtime caffeine roughly doubles on the same dose schedule.
- **Bolus size.**  Espresso shot ≈ 60 mg; drip coffee ≈ 100 mg; large cold brew ≈ 200 mg.  Change *Bolus size* before dragging.
- **Effective vs caffeine alone.**  At bedtime the paraxanthine you accumulated through the day is often a bigger fraction of total stimulant load than the caffeine itself.

## Caveats

Population averages.  CYP1A2 polymorphism alone produces a ~3-fold spread in elimination rate; smoking induces, oral contraceptives inhibit, pregnancy slows things to a crawl.  This is a back-of-envelope tool for thinking about your own schedule, not a clinical model.  It also ignores tolerance (chronic caffeine users have upregulated adenosine receptors) and the dose-response saturation in subjective stimulation.

---

*Written with Claude.*
