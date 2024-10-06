---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition
*Content*: This is the homepage of my blog.  I intend to write about some physics-related things I have been thinking about lately.  Potentially I will also attempt to practice writing in other languages which I'm learning (Latin, Attic Greek, Mandarin).

*Disclaimer, Attention Conservation Notice*: Please note that at this point, my primary goal is to 'write more', not to write well, nor to communicate clearly - I edit minimally, and would be unsurprised if a reader considered their time unrespected by my writing.  I'm exploring writing as a tool for _my thinking_ - I habitually write and speculate on things where there is a literature with which I'm mostly unfamiliar, at least with the specifics.  Anything written in a non-English language should be considered 'babble' for practice's sake, unrepresentative of my thoughts or beliefs on anything discussed.

Recent posts:

{% for post in site.posts %}
- [{{ post.title }}]({{ site.baseurl }}{{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

