---
layout: default
title: "Software"
excerpt: "Research software for diffraction, X-ray absorption spectroscopy, atomistic modelling, and data analysis."
permalink: /software/
author_profile: false
---

<main id="main-content" class="research-home site-inner">
  <h1>Software</h1>
  <p class="site-inner__intro">Tools and resources for structural characterisation, atomistic modelling, and data analysis. I share practical SOPs, tutorials and workshop notes below, covering workflows from laboratory diffraction to synchrotron PDF and XAS.</p>
<p class="software-channel">
<a href="https://www.youtube.com/@qinyou7272">Visit my YouTube channel · @qinyou7272</a>
</p>
<section class="software-workshops" aria-labelledby="workshop-materials">
<h2 id="workshop-materials">Tutorials &amp; workshop materials</h2>
<div class="software-tutorials">
<ul>
<li class="software-tutorial" id="fit2d-macro-video">
<div class="software-tutorial__summary">
<p>
<strong>Fit2D macros for diffraction data reduction</strong>
</p>
<p>A short demonstration of using a Fit2D macro for diffraction data reduction.</p>
<p class="software-tutorial__meta"> Shared <time datetime="2026-11-17">17 Nov 2026</time>
</p>
<ul class="software-entry__links" aria-label="Resources for Fit2D macros for diffraction data reduction">
<li>
<a href="https://www.youtube.com/watch?v=rCrD9djcPpM">Watch on YouTube</a>
</li>
</ul>
</div>
</li>
<li class="software-tutorial" id="xrd-pdf-xas-workshop">
<div class="software-tutorial__summary">
<p>
<strong>Mastering materials characterization — from lab XRD to synchrotron XAS/PDF</strong>
</p>
<p>Workshop slides introducing Rietveld refinement, TOPAS, pair distribution functions and X-ray absorption spectroscopy, with BM01/BM31 data-processing examples and a hands-on TOPAS Launch Mode exercise.</p>
<p class="software-tutorial__meta"> Shared <time datetime="2026-11-17">17 Nov 2026</time>
</p>
<ul class="software-entry__links" aria-label="Resources for Mastering materials characterization — from lab XRD to synchrotron XAS/PDF">
<li>
<a href="/files/sops/XRD_PDF_XAS_workshop_Bo_final.pdf" download="">Download slides (PDF)</a>
</li>
</ul>
</div>
</li>
</ul>
</div>
</section>

  {% for group in site.data.software %}
  <section class="software-group" aria-labelledby="{{ group.id }}">
    <h2 id="{{ group.id }}">{{ group.title | escape }}</h2>
    <ul class="software-list">
      {% for item in group.items %}
      <li class="software-entry" id="{{ item.name | slugify }}">
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
        {{ site.data.software_tutorials[item.name] }}
      </li>
      {% endfor %}
    </ul>
  </section>
  {% endfor %}
</main>
