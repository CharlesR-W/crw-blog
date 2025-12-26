---
layout: default
title: "Fruit of Preterition"
---

# Fruit of Preterition

 
*Content*: This is the homepage of my blog.  I intend to write about physics, math, information theory and similar, with the occasional humanist divagation.  The plainness of the theming is deliberate.

Posts:

<div class="posts-list">
<ul>
{% for post in site.posts %}
	<li class="post-item">
		<a class="post-link" href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
		<span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
	</li>
{% endfor %}
</ul>
</div>

