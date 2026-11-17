---
layout: default
title: "Software"
excerpt: "Research software for diffraction, X-ray absorption spectroscopy, atomistic modelling, and data analysis."
permalink: /software/
author_profile: false
---

<main id="main-content" class="research-home site-inner">
  <h1>Software</h1>
  <p class="site-inner__intro">Tools I use for structural characterisation, atomistic modelling, and data analysis.</p>

  {% for group in site.data.software %}
  <section class="software-group" aria-labelledby="{{ group.id }}">
    <h2 id="{{ group.id }}">{{ group.title | escape }}</h2>
    <ul class="software-list">
      {% for item in group.items %}
      <li class="software-entry">
        <div class="software-entry__summary">
          <h3>{{ item.name | escape }}</h3>
          <p>{{ item.description | escape }}</p>
        </div>
        {% if item.links and item.links.size > 0 %}
        <ul class="software-entry__links" aria-label="Links for {{ item.name | escape }}">
          {% for link in item.links %}
          <li><a href="{{ link.url | escape }}" aria-label="{{ link.label | escape }} for {{ item.name | escape }}">{{ link.label | escape }}</a></li>
          {% endfor %}
        </ul>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
  </section>
  {% endfor %}
</main>
