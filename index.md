---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition

*Content*: This is the homepage of my blog.  I intend to write about physics, math, information theory and similar, with the occasional humanist divagation.  The plainness of the theming is deliberate.

See also: <a href="{{ '/seeds/' | relative_url }}">Seeds</a> · <a href="{{ '/shortform/' | relative_url }}">Shortform</a> · <a href="{{ '/nulla-dies/' | relative_url }}">Nulla Dies</a>

<h2 style="margin-bottom: 0.8em;">Posts</h2>

<div class="posts-list">
<ul>
{% for post in site.posts %}{% unless post.tags contains "seed" or post.tags contains "nulla-dies" or post.tags contains "shortform" %}
<li class="post-item">
  <a href="{{ site.baseurl }}{{ post.url }}" class="post-link">{{ post.title }}</a>
  <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
  {% if post.math %}<span class="badge">math</span>{% endif %}
  {% assign wc = post.content | number_of_words %}{% if wc > 3000 %}<span class="badge">long</span>{% endif %}
</li>
{% endunless %}{% endfor %}
</ul>
</div>

