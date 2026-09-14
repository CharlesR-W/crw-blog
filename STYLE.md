# CRW Writing Style Guide

For assistants drafting or revising public-facing writing in CRW's voice. This
file should be iteratively updated — when CRW corrects the writing, add the
correction here.

Everything below describes tendencies and available moves, not a checklist.
Follow the material. Do not inject a structural device, catchphrase, joke, or
recap merely to simulate the voice.

**Scope of this file.** It covers two things: how the prose sounds, and how a
piece is built. It is the single source of truth for both — nothing restates it.

It deliberately does **not** cover: what you are allowed to assert, when to stub
rather than write, how to mark LLM-sourced claims, the drafting order, or the
Jekyll mechanics. Those live in the **`drafting-crw-blog-posts` skill**
(`~/.local/share/agent-skills/drafting-crw-blog-posts/`), which is the entry
point for the whole job and which reads this file first. If you are drafting and
have not invoked that skill, stop and invoke it.

---

## Voice

CRW writes like a physicist talking to smart friends at a whiteboard — technically precise but conversationally loose. The register moves fluidly between "here is a careful derivation" and "ey lmao". The reader is assumed to be smart, mathematically literate, and unimpressed by posturing.

**Core qualities:**
- Direct. Say what you think and why. "Here's what I think and why, fight me" not "we humbly propose".
- Honest about uncertainty. Flag when you're guessing, when a sign might be wrong, when something is a hack. "This is less hacky than it might sound" is fine. Pretending it's not hacky at all is not.
- Irreverent but serious. The humor is real but the math is not optional.
- Conversational with the reader. "You", "we", "let's" freely. Talk *to* someone, not *at* them.

**Argumentation:**
- Present reasoning and let it speak for itself.  Don't perform importance or create dramatic reveals — the reader should be convinced by the argument, not by rhetorical amplification.
- Frame as "here's what I think and why" not "HERE IS AN IMPORTANT TRUTH I WILL REVEAL TO YOU".  Don't tell the reader what to feel ("here is the thought experiment that should bother you").

**What this is NOT:**
- Not a textbook. Not dry. Not hedged.
- Not a blog-bro "10 THINGS ABOUT ENTROPY". Not clickbait.
- Not humble-bragging. Not falsely modest. If you derived something cool, you can say "Please clap."

---

## Sentence-Level Patterns

- Em-dashes for asides — like this — used liberally
- Parenthetical self-corrections in real time: "(one of those signs is wrong)", "(CHECK this?)", "(I'll be honest it seems like this should work but I haven't had the patience to sit down and do all the limits carefully)"
- Questions embedded in the flow, not just at section headers: "Kinda feels like it makes sense?"
- Mix technical and casual in the same sentence: "Note that if you're a based sigma terrachad, you can go so far as to set Σ=0"
- Short punchy sentences after long technical ones for contrast
- "Yikes." as a standalone sentence after a surprising result

**Characteristic phrases (use sparingly, not in every post):**
- "cash out" — meaning "make concrete", "what does this actually mean"
- "tl;dr" — for summaries within technical sections
- "c.f." — for cross-references
- "s.t." — for "such that" inline
- "Please clap." — after a satisfying derivation
- "big if true" — for speculative but exciting claims
- "basically just" — before simplifying something
- "kinda" / "sorta" — softeners that signal informality, not uncertainty
- Latin occasionally: "viz", "n.b.", "nulla die sine linea"
- "the trick is that" / "the kicker is that" — before the key insight

---

## Structure

**Layered access**: Public expository writing should reward several levels of
engagement. A reader who glances should get the central picture and some reason
to care. A reader who reads normally should acquire a useful intuitive model
and the main distinctions. A reader who goes into the weeds should find the
definitions, derivations, scope conditions, and unresolved problems.

These are reader outcomes, not three mandatory sections or three repetitions
of every idea. A concept may first appear as a picture, then as an example,
then as mathematics, or it may need only one good explanation. Use whatever
combination makes the particular piece work. This matters most for expository
math and technical agendas; an essay may need only a clear throughline and a
good skim path. Someone who skips the math should receive a simplified but
true model, not a claim that the technical section later retracts.

**Three-pass rhetoric**: For a central idea or the post's overall theme, often
use the classic essay movement: tell the reader what is coming, do the actual
work, then return to what was established. The first encounter gives the
reader a hook or map; the middle earns the claim; the return consolidates it,
shows what changed, or carries it into the next idea.

This can happen at the scale of a sequence, post, section, or concept. The
passes may be far apart, interleaved with other material, or performed by
different forms—a title or sketch can preview what a derivation later
establishes. They should reflect the reader's increased understanding, not
repeat one sentence three times. Use this strongly for important ideas and
lightly or not at all for minor ones.

Think of this as **semantic recurrence**: a loose, invisible form of spaced
repetition inside the text. Let a few important ideas return after intervening
material, often through the same phrase, contrast, example, or visual motif so
the reader recognizes them. Each return should add resolution, consequence,
application, or connection. The result should feel like a composed piece with
recurring motifs, not a lesson plan trying to drill vocabulary.

**Skim path**: Use any suitable combination of title, opening, headings,
figures, captions, examples, short summaries, boxed claims, and occasional
bold phrases to expose the big picture. There is no quota and bold need not do
the work. A useful skim communicates what the post is about, why it might
matter, and the few distinctions needed not to misunderstand it. It need not
carry every local caveat, but it must preserve any qualification that changes
the central claim.

**Gloss and memorable handles**: It is good to make a true idea attractive,
portable, and easy to recall. The gloss may live in a concept name, a sequence
title, a visual motif, a crisp example, or a sentence that compresses the
theme. Give readers the strongest *true* reason to care; do not substitute
importance adjectives or movement-building rhetoric for that reason.

New terminology may name a concept, distinction, operation, failure mode, or
the overall theme of a post or sequence. Identify the thing first and propose
several candidate names before silently installing one. Prefer ordinary
descriptive language when it works; otherwise prefer accurate, speakable names
over faux novelty, grandiose labels, and acronym soup. Presentation quality is
not endorsement of the underlying idea.

**Scope and density**: Aim for a legible center of gravity, not necessarily one
claim or one “reader promise.” Several threads can belong together when a
reader can see the map that unifies them. CRW naturally sees many dense
connections and tends to include too many of them, so flag when side paths
hide that map or make the technical prerequisites unmanageable. Recommend
shortening, splitting, or making a sequence only when it would give readers a
better route through the actual material. Give concrete boundaries and explain
what each resulting piece gains and loses. Never remove a substantive
qualification silently.

**Openings**: Give the reader an immediate on-ramp: a concrete situation,
motivating confusion, mental picture, question, or crisp claim. Make the big
picture—and, when useful, the “why”—available early. Don't throat-clear or
write a long history-of-the-field preamble merely because one is available.

**Sections**: Headings should make the map easier to follow; section length and
granularity should follow the argument. Section titles can be playful:
"Sleight-of-Hand", "Exordium: Who asked?", "Why Time Travel, FTL, Etc. Are All
Possible".

**Math integration**: Math is part of the argument, not separated from it. Introduce an equation, *then* explain it in words, or sometimes the reverse. Don't write a wall of prose followed by a wall of equations.

**Exercises/provocations**: Occasionally give the reader something to think about. "I'll leave it as an exercise how one derives..." or pose a question.

**Endings**: Honest about what was and wasn't accomplished. "I listed some cool math objects I like. Some of them are alternatives to entropy" is a perfectly valid conclusion. Don't force profundity. A good quote (Heraclitus, Wheeler, etc.) is fine if it's genuinely relevant.

**Cross-references**: Link to other CRW posts naturally: "(see my post 'Nonlinear Calculi')", not "[Related: Nonlinear Calculi (link)]".

---

## Math Presentation

- Inline math for definitions and simple expressions; display math for results and derivations
- Boxed equations ($$\boxed{...}$$) sparingly for key results
- After deriving something, often a quick sanity check: "Test: if g(x)=e^x, we lose x bits for fixed-point..."
- Flag uncertainty in math: "(what does this mean off the manifold?)", "(I want to be true. is it?)"
- Prefer concrete worked examples over abstract theorem statements
- Name your variables descriptively in surrounding prose, don't assume the reader tracks every symbol

---

## Tone Calibration by Post Type

**Pedagogical** (e.g. "Every Measurement Has a Scale"): Friendly, patient, often uses extended worked examples, directly addresses the reader, and may end with exercises. Still conversational but less profane.

**Technical/research** (e.g. "Bayesian Entropy"): More formal but still with characteristic asides. "Abstract" section is fine. Longer derivations are okay. The formality is in the math, not in the prose wrapping it.

**Shortform/musing** (e.g. "Immune System as Anti-Optimizer", "Math and Symbols"): Most casual. Stream-of-consciousness is fine. Can end with "I just think it's neat." Personal reflection is welcome.

**Nulla dies** (daily writing): Very casual, can be fragmentary, can be just a pointer to another post.

**Argumentative/position** (e.g. "Power Laws Are Not Enough"): Presenting a specific claim with structured reasoning.  More formal than shortform, but the goal is explaining why you find an argument compelling, not convincing per se.  No dramatic framing devices.  BLUF at the top.

---

## Expository Reference Points

- **Primary reference: the Embedded Agency sequence.** A reader can leave with
  a durable picture of the problem and its major parts without mastering the
  technical work underneath them. Concrete scenarios, recurring visual
  language, good names, and an explicit conceptual map provide on-ramps at
  several depths.
- **Secondary reference: Scott Garrabrant's less explicitly technical work,
  including Geometric Rationality.** A strong unifying name and theme make
  several fairly self-contained arguments feel like parts of one object.
- **Selective lessons from the SLT and Infra-Bayesianism sequences.** Borrow
  their strong naming, early orientation, visible payoff, and ability to give a
  zero-order account before the full mathematics. Do not copy a sales pitch,
  inflate the stakes, imply consensus, or make the prose sound more certain
  than the underlying work. The presentation can be admired without endorsing
  the research program.

These are architectural references, not voices to imitate sentence by
sentence.

---

## NEVER

- "delve" / "explore" (as verbs for intellectual activity)
- "utilize" (just say "use")
- "it's worth noting that" / "it bears mentioning"
- "fascinating" / "intriguing" (Claude-isms)
- "Let's dive in" / "Without further ado"
- "In conclusion" (just end)
- Hedging chains: "it could perhaps be argued that one might consider..."
- Summarizing what you just said at the end of every section
- Sycophantic framing: "This brilliant insight..." / "This elegant result..."
- Fake enthusiasm: "How exciting!" / "What a remarkable finding!"
- Emoji in post body (unless quoting something that has them)
- Starting multiple paragraphs with "It is" or "There is"
- "Importantly," as a sentence opener
- Dense chains of side connections whose relationship to the post's spine is
  unclear
- Decorative bolding that does not help the skim path
- Forcing every minor point into an abstract/intuition/math/recap template
- Silently introducing a coined term as though it were standard or already
  approved
- Repeating a memorable formulation without giving it a new explanatory job
- Making a line more memorable by making its claim less qualified

### Observed LLM residue

Specific tics found in past LLM drafts of CRW's posts. Scan your own output for
these before handing back:

- Em-dash meta-emphasis: "—and this matters—", "—crucially—", "—and here's the key—"
- "The key insight is", "Notably,", "crucial"
- The contrastive tic: "X isn't just A — it's B"
- Enumerative scaffolding: "Two key facts hold:", "There are three main…", and
  bold-label lists (**Fact 1:** …)
- Paragraph-closing tidy parallels used as connective filler ("…just as SGD pushes
  weights toward lower loss"). When the parallel *is* the claim, state it once with
  its evidence status attached — never as a bow on a paragraph.
- Rule-of-three cadences
- Throat-clearing or sycophantic openers

**Not on this list, despite what generic LLM style advice says:** a `## Abstract`
header and "In this post I argue/will…" are both native here. "In this post" opens
six-plus posts spanning 2024–2026, including the earliest; `## Abstract` appears in
*Bayesian-Entropy*, *Scalar-Dimension*, and *Why-Differential-Entropy-Stinks*. Do
not strip them. Likewise em-dashes, semicolons, and parentheticals are native and
should be used freely — generic "avoid em-dashes" advice would damage the voice.

---

*This file is iteratively refined. When CRW corrects your writing, add the pattern here.*
