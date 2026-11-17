---
layout: default
title: "Materials for functional and energy"
excerpt: "Bo Jiang studies structure, defects and reactions in functional and energy materials."
permalink: /
author_profile: false
redirect_from:
  - /about/
  - /about.html
---

<main id="main-content" class="research-home">
  <section class="research-home__intro" aria-labelledby="bo-jiang">
    <div class="research-home__bio">
      <h1 id="bo-jiang">{{ site.author.name | escape }}</h1>
      <p class="research-home__affiliation">Materials researcher · University of Oslo</p>
      <p>I study how atomic structure and defects govern the properties of crystalline, disordered and nanostructured materials. In the Electrochemistry group at the University of Oslo, I investigate redox exsolution and hydration in functional oxides for electrochemical energy conversion.</p>
      <p>My work brings together synchrotron X-ray and neutron scattering, X-ray absorption spectroscopy, and atomistic modelling. I use these methods to connect local structure and chemical disorder to how materials behave.</p>
      <ul class="research-home__links" aria-label="Profiles and curriculum vitae">
        <li><a href="{{ site.author.uri }}">UiO profile</a></li>
        <li><a href="{{ site.author.googlescholar }}">Google Scholar</a></li>
        <li><a href="{{ '/cv/' | relative_url }}">CV</a></li>
      </ul>
    </div>
    <img class="research-home__portrait" src="{{ '/images/' | append: site.author.avatar | relative_url }}" alt="Portrait of {{ site.author.name | escape }}" width="1171" height="1436">
  </section>

  <section class="research-home__research" aria-labelledby="home-research">
    <h2 id="home-research">Research</h2>
    <div class="research-home__grid">
      {% for topic in site.data.research_topics %}
      <article class="research-card">
        <h3><a href="{{ '/research/' | relative_url }}#{{ topic.id }}">{{ topic.title | escape }}</a></h3>
        <p>{{ topic.summary | escape }}</p>
        <ul class="research-card__papers" aria-label="Representative publications">
          {% for paper in topic.papers %}
          <li><a href="{{ paper.url | relative_url }}">{{ paper.label | escape }}</a></li>
          {% endfor %}
        </ul>
      </article>
      {% endfor %}
    </div>
  </section>

  <section class="research-home__selected" aria-labelledby="home-selected-publications">
    <h2 id="home-selected-publications">Selected publications</h2>
    <ul class="research-home__selected-list">
      {% for paper in site.data.featured_publications %}
      <li>
        <a href="{{ paper.url | relative_url }}">{{ paper.title | escape }}</a>
        <span>{{ paper.venue | escape }} · {{ paper.year }}</span>
      </li>
      {% endfor %}
    </ul>
    <a class="research-home__all-publications" href="{{ '/publications/' | relative_url }}">All publications <span aria-hidden="true">→</span></a>
  </section>
<section class="research-home__updates" aria-labelledby="recent-updates">
<h2 id="recent-updates">Recent updates</h2>
<ul class="research-home__selected-list">
<li> <a href="/software/#fit2d-macro-video">Fit2D macros for diffraction data reduction</a> <span class="recent-update__meta">Workshop materials · <time datetime="2026-11-17">17 Nov 2026</time> </span>
</li>
<li> <a href="/software/#rmcprofile-video">Running RMCProfile fits</a> <span class="recent-update__meta">RMCProfile · <time datetime="2026-11-17">17 Nov 2026</time> </span>
</li>
<li> <a href="/software/#artemis-exafs-video">EXAFS fitting in Artemis</a> <span class="recent-update__meta">Athena and Artemis · <time datetime="2026-11-17">17 Nov 2026</time> </span>
</li>
</ul>
</section>
</main>
