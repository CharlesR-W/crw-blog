---
title: "How I Use Anki (and How I Learn Languages With It)"
date: 2026-06-01
tags: [personal]
---

A friend recently asked me to walk him through my entire Anki setup, and I ended up giving him a forty-minute brain dump.  This is that brain dump, cleaned up.  It is part philosophy, part card-design rules, and part the specific pipeline I use to learn languages.  None of it is novel, but it is what actually works for me after five years of doing this nearly every day.

## The one idea you should buy

The thing that got me into spaced repetition was [Gwern's essay on it](https://gwern.net/spaced-repetition).  I will be honest: I have not read deeply into the literature, but I understand the basis of the algorithm and the concept is obviously reasonable, and Gwern also sells you on the right mental framing.

The framing is the important part.  Anki is not a toy for memorizing things.  It is a technology that makes remembering things *a choice*.  That is the whole pitch.  Once you internalize it, you stop asking "should I bother making a card for this" and start treating your memory as something you get to decide about.

If you read two things before starting, read Gwern and the [SuperMemo "20 Rules of Formulating Knowledge"](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge).  Between them you get the why and the how.

## The rule that everything else follows from

You cannot *learn* things from flashcards.  You can only *remember* them.

This sounds like a small distinction and it is actually the whole game.  The default failure mode, for almost everybody, is to download a deck of 800 Chinese vocab words, flip each card over, and stare at the back until it "sticks."  This is rubbing your face against a brick wall.  It works about an order of magnitude worse than doing it the right way, and it is miserable, so you quit.

The right way: you make cards of things you *already know*.  Acquisition happens somewhere else, in a lecture, a textbook, a chapter of a novel.  The card is there to keep a thing you have already understood from decaying.  If you try to do the understanding *on* the card, you are using a screwdriver as a hammer.

Almost every other rule below is a corollary of this one.

## Make cards stupidly, insultingly simple

No card should be annoying.  If I find a card that annoys me, I delete it on the spot.  Whatever your instinct is for how granular to make things, make five to ten times as many cards that are each really, really easy.

A complicated thing does not become one hard card.  It becomes ten or fifteen trivial ones.  Take a single figure from a lecture on boundary layer theory: you have a curve, and the argument is that in one region this quantity is small, in another region that quantity is small, and you bridge them.  That is not one card.  That is ten or fifteen cards, each asking one tiny thing, each with the relevant equation and a picture right there on the front.

The oldest card in my collection, the very first one I ever made, is this:

> **Front:** State the Picard-Lindelof theorem.  `dx/dt = f(x,t)` has a unique solution IFF \_\_\_\_\_\_
>
> **Back:** The ODE `dx/dt = f(x,t)` has a unique solution if f is continuous in t and Lipschitz continuous in x.

It is the worst card I own, and I keep it around as a reminder of what not to do.  Look at what it asks: "state the theorem" (open-ended), *and* fill in a blank, *and* the blank wants the entire hypothesis (two separate conditions) at once.  There is no topic header, so cold, a year from now, you have to reconstruct the whole frame before you can even start.  It is three cards crammed into one, and the format fights you.  If I needed this material today I would make ten cards out of it, which is exactly what the next section is about.

You should be forgetting about 10% of your cards.  If you are forgetting more, your cards are too hard or you are trying to learn from them.  If you are forgetting almost none, fine, but see the section on hitting "Easy" below.

## Context-load the front

The corollary of "you can only remember, not learn" is that the card has to be recallable with *zero* context ten months, or five years, from now.  So I load the front with context.

Three things do most of the work:

- **A topic header.**  One line at the top that tells you instantly what this card is about.  Half the difficulty of a cold card is just figuring out what universe you are in.
- **The relevant equation.**  I am a symbol gremlin; for me, seeing the equation loads the whole context into my head in about a second.
- **A picture.**  This makes the card faster to *make*, and it gives you a lot of memory context for free.

So the front of a good hard card looks like: topic header, the question, the equation, a picture, and any especially important context items.  The back is short, just the answer, sometimes with a note or "nearly the answer" hint for the genuinely annoying ones.  Yes, a front that long is a little annoying.  But for something genuinely complicated it is roughly as good as I can do, and it beats the alternative of a card you bounce off of forever.

Here is the pattern in the wild.  I was learning about the "dynamic Cheeger ratio" (an object from the theory of coherent structures in fluid flows), which is defined by this figure:

<img src="{{ site.baseurl }}/images/2026-06-01-anki/cheeger-ratio.png" alt="The dynamic Cheeger ratio: infimum over regions A of (flux through the boundary of A, averaged over time) divided by the measure of A." style="max-width:340px; display:block; margin:1em auto; background:#2a2a2a; padding:8px; border-radius:6px;">

Rather than make one card that says "explain the dynamic Cheeger ratio," I made a little cluster of cards that all share the topic header `dynamic Cheeger ratio` and all put that same picture on the front, each asking exactly one tiny thing:

> **Front:** *dynamic Cheeger ratio* [figure] morally asking for what? → **Back:** the minimum-flux surface
>
> **Front:** *dynamic Cheeger ratio* [figure] why is this SO COOL? → **Back:** it's the minimum-flux surface!  optimal partitioning
>
> **Front:** *dynamic Cheeger ratio* [figure] what cool object lets us "solve" for it? → **Back:** the dynamical Laplacian

Three cards, each trivial, each anchored by the same header and the same image.  The picture does the context-loading for free, and because I see the figure on every card, the visual itself becomes part of what I remember.  None of these would survive on its own as the lone "Cheeger ratio card," but together they actually stick.

It works for messier objects too.  Here is the front-of-card figure for a cluster on the Levy-Khintchine decomposition of a Levy measure:

<img src="{{ site.baseurl }}/images/2026-06-01-anki/levy-decomposition.jpg" alt="A Levy measure decomposed into a normalized tail part nu and an unnormalized central part mu, with the corresponding split of the Levy-Khintchine integral." style="max-width:560px; display:block; margin:1em auto; background:#fff; padding:8px; border-radius:6px;">

Same move: the equation lives on the front of several cards, and each card blanks out one piece of it ("`generalized Poisson = const*(Poisson) + ?`", "`= ? + (compensated generalized Poisson)`", "morally, what two components?").  Blanking one term at a time turns an intimidating formula into a handful of cards that each feel easy, and the figure carries the context that a bare "state the decomposition" prompt would force you to rebuild from scratch.

## One giant deck

A normal person would have three or four decks split by topic, studied separately.  I have one deck.  Everything, every language and every subject, interlaced into a single pile.

There are three reasons, in increasing order of honesty:

1. Managing separate decks is annoying.
2. My old system worked this way and I never changed it.
3. If I had a separate deck for Latin and one for Russian, I would get tired of one, ignore it for a week, and then it would quietly stop working.  One big pile means I always do everything, because there is only one thing to do.

This is really an instance of a more general principle: [beware trivial inconveniences](https://www.lesswrong.com/posts/reitXJgJXFzKpdKyd/beware-trivial-inconveniences).  My life is dominated by trivial inconveniences, and I have become an expert at engineering them out of my own way.  A single deck removes a decision I would otherwise fail to make.

## The compounding-load myth

People warn each other not to get over-ambitious, because supposedly once you start learning too many things, the algorithm chains you to reviewing that many things forever.  This is mostly not true.

The load goes *down* quickly, because the spacing grows.  If you add 20 cards a day, you settle at roughly 20 reviews a day, not an ever-growing mountain.  On any given day, nearly half of my due cards were added within the last month; the old stuff has spaced itself out into the distance.

The people who actually get crushed are the ones doing the brick-wall thing: sitting down to *memorize from the card*.  That is what makes the load feel unbearable.  The compounding-load complaint is downstream of bad card practice, not an inherent property of the algorithm.

For the record, I do something like 337 cards on a typical day.  This is not necessary and you should not take it as a target; I do it because I genuinely get that much value out of it.  It is also easy to slot into dead time: I can do five or six cards in the twenty seconds while Claude is thinking, or while walking to work.  You do it to the extent that you get value, and Anki has all the knobs to cap how many new cards and reviews you see per day.

## Scheduling without losing your mind

Anki rates each answer 1 to 4 (Again / Hard / Good / Easy).  A 1 throws the card into the "forgot" pile; 2, 3, and 4 just make it come back sooner or later.

The one piece of setup I actually care about: I do not want to see a card I just failed again *during the same session*.  I like having a green pile I march through, and then the wrong ones at the end, and Anki does not make this easy out of the box.  So I set lapses to re-show a forgotten card about 30 minutes later rather than immediately.  By the time it comes back around, I have done everything else.

I will be honest that I do not fully understand all of Anki's learning-step and lapse-step internals, and I am not in love with how mine are set up.  There is a little "?" you can click to read the docs; do that rather than trusting me on the exact numbers.  The high-level behavior is what matters.

Two buttons worth knowing:

- **Suspend** = "go away, I never want to see you again."  It parks the card in a pile you can revisit later.
- **Bury** = "not now, show me tomorrow."

If you know something cold, you do not actually need to suspend it.  Just hit Easy.  The spacing grows exponentially, so an easy card effectively suspends itself, and it is nice to have it surface once in a blue moon.  This is the ideal state for your whole collection, by the way: **all your cards should feel easy.**  You are not supposed to be suffering.  If a card is hard, that is information that it is a bad card.

And: never download a 500-card deck.  Almost never.  I have done it maybe twice.  (Language vocab decks, which come pre-split by chapter, are the exception, and even then you only ever turn on one chapter at a time.  More on that below.)

## Tooling

The desktop client is much better than the mobile app for anything involving editing (hit `E` to edit a card; on [AnkiDroid](https://github.com/ankidroid/Anki-Android) this is genuinely painful, and there may be a better unofficial Android app).  The desktop app also just looks better; mine looks nothing like the default Windows install because I changed the theme to match my system.  If you care, you could have Claude Code write you a frontend, and there are gamification add-ons, including a gloriously cringe [Call of Duty / Halo killstreak mod](https://github.com/jac241/anki_killstreaks) that awards you a Triple Kill for answering cards fast.

The genuinely useful move is to offload the boring parts to an LLM.  I had Claude Code translate my entire old deck into Anki format.  It can OCR a textbook page and turn the vocab into cards, or convert a CSV export into something Anki will import.  I never bothered to learn Anki's native import flow because I did not have to.

## Learning a language with this

About half of my use is languages (Latin, Greek, Russian, Chinese), and the method is specific enough to be worth its own section.

### Comprehensible input, and don't translate

The way the human brain learns a language is **comprehensible input**: you read material you can *mostly* understand, in the target language, and the gaps fill themselves in from context.  It is faintly preposterous that we do not teach everything this way.

The gold standard is [*Lingua Latina Per Se Illustrata*](https://en.wikipedia.org/wiki/Lingua_Latina_per_se_Illustrata) (LLPSI), the best language textbook humanity has produced.  The conceit is that every single word in it is Latin.  Chapter one opens *Roma in Italia est, Italia in Europa est*, and as long as you can read, Latin simply starts to make sense as you go.  There are pictures.  It is brutally well graded: maybe twenty new words per chapter over fifty to eighty sentences, and it deliberately re-sprinkles old vocab and grammar so things keep coming back before you forget them.  The grammar notes (the *pensa*) live at the end, partly because I do not have a good story for how to study grammar directly.

The corollary for your cards: **do not translate.**  When you learn a vocab word, do not attach an English label to it; try to *visualize* what it means.  The back of the card should have the English only as a fallback for when you genuinely blank.  The reason is that translating builds the wrong structure.  You already have a rich semantic web in English; word-by-word translation just hangs a second node off each English node, a thin projection.  Reading directly in the language builds a *native* web instead, which is denser and recalls faster.

I will flag honestly that this is contested.  My friend pushed back that he translates constantly and his comprehension seems fine, and I conceded that if you already have enough background it may not hurt your *understanding* much.  But I still recommend against it, I am fairly sure it is better, and I am reasonably sure it is no more effort once it is a habit.  The failure-mode version is someone seeing a word and thinking the English word, every time, forever; that person tends not to actually remember the words, precisely because they never built the native structure.

One more rule of thumb: in any sentence you study, **80 to 90% of the words should already be known.**  No more than about one new word per sentence.  (I sometimes violate this spectacularly for Chinese and dump 200 cards at once, but that is me hating myself, not a recommendation.)

### Grammar and output, briefly and honestly

Does enough input give you grammar and the ability to speak for free?  I have tried hard to make this true and it is mostly not, though it may not matter as much as you would think.  My evidence: I have comparable input in Latin and Greek; I can speak Latin and I cannot output in Greek at all, purely because I never *tried* to output in Greek.  Maxing your reading makes learning to output much easier, but you still have to actually learn to output.  Early on it is probably not worth much of your time; later, you go find exercises and grind it.

Reading versus writing is the same story.  In Chinese I am slowly forgetting how to *write* characters but not how to *read* them, because I practice the one and not the other.  If you only care about reading, you can skip learning to write, and you will save yourself a lot of pain.

### The actual pipeline

The skeleton is the same for every language:

1. **Acquisition pass.**  Read the chapter (or section, or whatever unit) once, in the language.  Understand what you can.
2. **Add the cards.**  This is itself a second pass over the vocab.  I often realize I did not actually know a word until the card makes me confront it.
3. **Reread.**  The next day, do the new cards as part of my normal review and/or read the chapter again.  Two passes plus the cards is usually enough; after that the words just come up in reviews as they come up.

Crucially, I do *not* make vocab cards by hand.  That is cancer and I would simply never do it, which means it would not happen.  The pipeline has to be frictionless or I will not do it.  Concretely, per language:

- **Latin (LLPSI):** read the chapter, then either have Claude make cards for all the words or grab the existing community deck, which is organized by chapter.  I just tick "activate chapter one," which turns on forty or fifty cards at a time, a very reasonable dose.  I never download the whole 3,000-card thing at once.
- **Russian ([LingQ](https://www.lingq.com/)):** the shittier-but-real version of LLPSI as an app.  Its beginner material is good, you can import your own texts, and its CSV export includes the example sentence automatically, which is why my Russian cards have a sentence on the back for context.  About $10/month; I use it enough that it is worth it.  (Full disclosure: I have been lazy and *not* following my own rules for Russian lately, raw-dogging it and getting a bunch wrong, and I can feel the failure mode it produces.)
- **Chinese ([Pleco](https://www.pleco.com/)):** a different beast, because there is no LLPSI equivalent and early on every word is new, so you just grind through the bootstrapping phase.  My textbook was *Integrated Chinese* ([Cheng & Tsui](https://www.cheng-tsui.com/), six volumes, decks findable online; it front-loads a lot of vocab per chapter on purpose).  Pleco is the engine: with the document-reader add-on you read a book *inside the app*, tap a word to see the definition, hit `+` to add it, then export the batch as a CSV and import it (or have Claude convert it).  A truly unhinged Pleco binge can add a hundred words at once.  Anything you do not want, you just deactivate.

The throughline: someone else (or an LLM) makes the cards, you select what you need a chapter at a time, and you keep the friction as close to zero as you can.  The whole reason I finally switched my old system over to Anki is that now it is on my phone, and being able to do it in bed instead of at my desk makes my life about 3% better.  That 3% is the difference between doing it and not.

## tl;dr

- Anki makes remembering a choice.  That is the point.
- You cannot learn from cards, only remember.  Acquire elsewhere; use cards to retain.
- Make cards stupidly simple.  Five to ten times more easy cards than you think.  Delete anything annoying.
- Context-load the front (topic header, equation, picture).  Decompose hard things into many trivial cards.
- One big deck beats many small ones, because it removes a decision you will otherwise fumble.
- The load does not compound the way people fear, *if* your cards are right.
- All your cards should feel easy.  Aim to forget about 10%.
- For languages: comprehensible input, don't translate, keep 80-90% of words known, and make the card pipeline frictionless so you actually do it.

*Written up from a conversation, with Claude.*
