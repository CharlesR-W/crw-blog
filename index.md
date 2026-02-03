---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition

*Content*: This is the homepage of my blog.  I intend to write about physics, math, information theory and similar, with the occasional humanist divagation.  The plainness of the theming is deliberate.

<div style="margin: 1.5em 0; padding: 1em; background: rgba(255,255,255,0.04); border-left: 4px solid var(--accent); border-radius: 4px;">
<strong><a href="{{ '/seeds/' | relative_url }}">Seeds</a></strong> (Experimental) — prompts for exploring topics with your own LLM. <em>Written by Claude, not yet read by me.</em> Under construction; use with appropriate skepticism.
</div>

<h2 style="margin-bottom: 0.8em;">Posts</h2>

<div class="posts-list">
<ul>
{% for post in site.posts %}{% unless post.tags contains "seed" %}
<li class="post-item">
  <a href="{{ site.baseurl }}{{ post.url }}" class="post-link">{{ post.title }}</a>
  <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
</li>
{% endunless %}{% endfor %}
</ul>
</div>

