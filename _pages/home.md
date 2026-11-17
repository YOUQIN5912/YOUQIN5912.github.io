---
layout: single
title: "Materials for functional and energy"
excerpt: "Bo Jiang studies structure, defects and reactions in functional and energy materials."
permalink: /
author_profile: true
---

<div class="academic-intro" markdown="1">
I’m Bo Jiang, a materials researcher in the [Electrochemistry group](https://www.mn.uio.no/kjemi/english/research/groups/electrochemistry/index.html) at the University of Oslo. I study how atomic structure and defects shape the behaviour of functional materials, with a current focus on oxides for electrochemical energy conversion.

<div class="academic-actions">
  <a class="btn academic-button" href="{{ '/research/' | relative_url }}">Explore my research</a>
  <a href="{{ '/publications/' | relative_url }}">Browse publications</a>
</div>
</div>

## Research interests

- [Nanoparticle exsolution in perovskites]({{ '/research/' | relative_url }}#nanoparticle-exsolution)
- [Hydration and defects in proton ceramics]({{ '/research/' | relative_url }}#proton-ceramics)
- [Local structure in functional materials]({{ '/research/' | relative_url }}#local-structure)

## Recent publications

{% assign publications = site.publications | sort: "date" | reverse %}
{% for publication in publications limit: 3 %}
  {% include publication-entry.html publication=publication show_authors=false %}
{% endfor %}

[University of Oslo profile]({{ site.author.uri }}) · [Curriculum vitae]({{ '/cv/' | relative_url }})
