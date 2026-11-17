---
layout: single
title: "Publications"
excerpt: "Selected peer-reviewed publications by Bo Jiang, with DOI and publisher links."
permalink: /publications/
author_profile: true
redirect_from:
  - /publication/2009-10-01-paper-title-number-1
  - /publication/2010-10-01-paper-title-number-2
  - /publication/2015-10-01-paper-title-number-3
---

Selected peer-reviewed articles. See [Google Scholar]({{ site.author.googlescholar }}) or [ORCID]({{ site.author.orcid }}) for more publications.

{% assign publications = site.publications | sort: "date" | reverse %}
{% assign previous_year = "" %}
{% for publication in publications %}
  {% assign year = publication.date | date: "%Y" %}
  {% if year != previous_year %}
<h2 id="year-{{ year }}">{{ year }}</h2>
    {% assign previous_year = year %}
  {% endif %}
  {% include publication-entry.html publication=publication show_authors=true %}
{% endfor %}
