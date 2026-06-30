---
layout: default
title: "Research"
---

# Research

My research writing: physics, math, information theory, learning theory, and the occasional adjacent topic.  The plainness of the theming is deliberate.

**The other pages:**

- <a href="{{ '/writing/' | relative_url }}">Writing</a> — non-technical pieces: essays, translations, poetry.
- <a href="{{ '/notes/' | relative_url }}">AI-Written Notes</a> — working notes on what I am currently thinking about, written up by an LLM from my drafts.
- <a href="{{ '/seeds/' | relative_url }}">Curated Tutorial Prompts</a> — mini-curricula and hands-on tutorials to feed to an LLM or work through yourself.
- <a href="{{ '/widgets/' | relative_url }}">Widgets</a> — small interactive toys that run in the browser.
- <a href="{{ '/cv/' | relative_url }}">About and CV</a> — who I am, and my CV.

<!-- hidden: · <a href="{{ '/nulla-dies/' | relative_url }}">Nulla Dies</a> -->

<h2 style="margin-bottom: 0.8em;">Posts</h2>

<div class="posts-list">
<ul>
{% for post in site.posts %}{% unless post.tags contains "seed" or post.tags contains "nulla-dies" or post.tags contains "personal" or post.tags contains "widget" or post.tags contains "notes" %}
<li class="post-item">
  <a href="{{ site.baseurl }}{{ post.url }}" class="post-link">{{ post.title }}</a>
  <span class="post-meta">
    <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    {% if post.kind %}<span class="badge">{{ post.kind }}</span>{% endif %}
    {% if post.math %}<span class="badge">math</span>{% endif %}
    {% assign wc = post.content | number_of_words %}{% if wc > 3000 %}<span class="badge">long</span>{% endif %}
  </span>
</li>
{% endunless %}{% endfor %}
</ul>
</div>
