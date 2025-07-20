---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition
### $\heartsuit \; \big( \; \heartsuit p \;\rightarrow\; p \; \big) \;\rightarrow\; p$

 
*Content*: This is the homepage of my blog.  I intend to write about physics, math, information theory and similar, with the occasional humanist divagation.  The plainness of the theming is deliberate.

Posts:

{% for post in site.posts %}
- [{{ post.title }}]({{ site.baseurl }}{{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

