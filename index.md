---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition
*Content*: This is the homepage of my blog.  I intend to write about some physics-related things I have been thinking about lately.  Potentially I will also attempt to practice writing in other languages which I'm learning (Latin, Attic Greek, Mandarin).  The plainness of the theming is deliberate.

Posts:

{% for post in site.posts %}
- [{{ post.title }}]({{ site.baseurl }}{{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

