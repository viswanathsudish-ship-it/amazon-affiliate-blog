---
layout: default
title: Categories
---

# Browse by Category

{% assign categories = "fitness-gear,smart-home,kitchen-gadgets,tech-accessories,outdoors" | split: "," %}

{% for category in categories %}
## {{ category | replace: "-", " " | capitalize }}

<ul>
{% for post in site.posts %}
  {% if post.categories contains category %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> — {{ post.date | date: "%B %d, %Y" }}</li>
  {% endif %}
{% endfor %}
</ul>
{% endfor %}
