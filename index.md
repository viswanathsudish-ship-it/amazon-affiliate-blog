---
layout: default
---

<!-- Hero Section -->
<section class="hero">
  <div class="wrapper">
    <div class="hero-content">
      <div class="hero-badge">
        <span class="pulse"></span>
        Live Reviews Updated Daily
      </div>
      <h1>Find the Best <span>Gear</span> for 2026</h1>
      <p>Honest, in-depth reviews and buying guides for fitness gear, smart home, kitchen gadgets, and tech accessories. We test so you don't have to.</p>
      <div class="hero-buttons">
        <a href="#latest-posts" class="btn btn-primary">Browse Latest Reviews</a>
        <a href="/categories" class="btn btn-secondary">View Categories</a>
      </div>
    </div>
  </div>
</section>

<!-- Stats Bar -->
<section class="stats-bar">
  <div class="wrapper">
    <div class="stat-item">
      <div class="stat-number">{{ site.posts | size }}</div>
      <div class="stat-label">Reviews Published</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">5</div>
      <div class="stat-label">Categories</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">100%</div>
      <div class="stat-label">Honest Opinions</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">24h</div>
      <div class="stat-label">Fresh Content</div>
    </div>
  </div>
</section>

<!-- Latest Posts -->
<section class="posts-section" id="latest-posts">
  <div class="wrapper">
    <div class="section-header">
      <h2>Latest <span>Reviews</span></h2>
      <a href="/categories" class="view-all">View All →</a>
    </div>
    <div class="post-grid">
      {% for post in site.posts limit:6 %}
        <a href="{{ post.url | relative_url }}" class="post-card">
          <div class="post-card-image">
            <span>
              {% assign category = post.categories | first %}
              {% case category %}
                {% when 'fitness-gear' %}💪
                {% when 'smart-home' %}🏠
                {% when 'kitchen-gadgets' %}🍳
                {% when 'tech-accessories' %}📱
                {% when 'outdoors' %}🏕️
                {% else %}⭐
              {% endcase %}
            </span>
          </div>
          <div class="post-card-content">
            <div class="post-card-meta">
              <span class="post-card-category">{{ post.categories | first | replace: '-', ' ' }}</span>
              <span class="post-card-date">{{ post.date | date: "%b %d, %Y" }}</span>
            </div>
            <h3>{{ post.title }}</h3>
            <p>{{ post.excerpt | strip_html | truncatewords: 18 }}</p>
            <div class="post-card-footer">
              <span class="read-time">5 min read</span>
              <span class="read-more">Read Review →</span>
            </div>
          </div>
        </a>
      {% endfor %}
    </div>
  </div>
</section>

<!-- Categories -->
<section class="categories-section">
  <div class="wrapper">
    <div class="section-header">
      <h2>Browse by <span>Category</span></h2>
    </div>
    <div class="category-grid">
      <a href="/categories#fitness-gear" class="category-card">
        <div class="category-icon">💪</div>
        <h3>Fitness Gear</h3>
        <span>Equipment &amp; Accessories</span>
      </a>
      <a href="/categories#smart-home" class="category-card">
        <div class="category-icon">🏠</div>
        <h3>Smart Home</h3>
        <span>Devices &amp; Automation</span>
      </a>
      <a href="/categories#kitchen-gadgets" class="category-card">
        <div class="category-icon">🍳</div>
        <h3>Kitchen Gadgets</h3>
        <span>Tools &amp; Appliances</span>
      </a>
      <a href="/categories#tech-accessories" class="category-card">
        <div class="category-icon">📱</div>
        <h3>Tech Accessories</h3>
        <span>Gadgets &amp; Gear</span>
      </a>
      <a href="/categories#outdoors" class="category-card">
        <div class="category-icon">🏕️</div>
        <h3>Outdoors</h3>
        <span>Camping &amp; Hiking</span>
      </a>
    </div>
  </div>
</section>
