---
layout: default
title: Categories
---

<section class="categories-hero">
  <div class="wrapper">
    <h1>Browse Categories</h1>
    <p>Find reviews for every type of gear you need.</p>
  </div>
</section>

<div class="wrapper" style="padding: 48px 24px;">
  {% assign categories = "fitness-gear,smart-home,kitchen-gadgets,tech-accessories,outdoors" | split: "," %}
  {% assign icons = "💪,🏠,🍳,📱,🏕️" | split: "," %}
  {% assign descriptions = "Equipment & Accessories,Devices & Automation,Tools & Appliances,Gadgets & Gear,Camping & Hiking" | split: "," %}

  {% for category in categories %}
  <section class="category-section" id="{{ category }}">
    <h2><span>{{ icons[forloop.index0] }}</span> {{ category | replace: "-", " " | capitalize }}</h2>
    <div class="post-grid" style="margin-top: 20px;">
      {% assign has_posts = false %}
      {% for post in site.posts %}
        {% if post.categories contains category %}
          {% assign has_posts = true %}
          <a href="{{ post.url | relative_url }}" class="post-card">
            <div class="post-card-image">
              <span>{{ icons[forloop.parentloop.index0] }}</span>
            </div>
            <div class="post-card-content">
              <div class="post-card-meta">
                <span class="post-card-category">{{ category | replace: "-", " " }}</span>
                <span class="post-card-date">{{ post.date | date: "%b %d, %Y" }}</span>
              </div>
              <h3>{{ post.title }}</h3>
              <p>{{ post.excerpt | strip_html | truncatewords: 15 }}</p>
              <div class="post-card-footer">
                <span class="read-time">5 min read</span>
                <span class="read-more">Read Review →</span>
              </div>
            </div>
          </a>
        {% endif %}
      {% endfor %}
      {% unless has_posts %}
        <p style="color: var(--text-lighter); padding: 20px 0;">No posts in this category yet. Check back soon!</p>
      {% endunless %}
    </div>
  </section>
  {% endfor %}
</div>
