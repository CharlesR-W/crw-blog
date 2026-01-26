---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition


*Content*: This is the homepage of my blog.  I intend to write about physics, math, information theory and similar, with the occasional humanist divagation.  The plainness of the theming is deliberate.

<div style="margin: 1.5em 0; padding: 1em; background: #f8f8f0; border-left: 4px solid #7a9e7a;">
<strong><a href="{{ '/seeds/' | relative_url }}">Seeds</a></strong> — polished excerpts from LLM conversations. Ideas that emerged from dialogue rather than solitary writing.
</div>

Posts:

{% for post in site.posts %}{% unless post.tags contains "seed" %}
- [{{ post.title }}]({{ site.baseurl }}{{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endunless %}{% endfor %}

