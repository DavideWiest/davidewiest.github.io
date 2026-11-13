---
permalink: /
layout: homepage
author_profile: false
hero_intro: >-
  I'm a computer science student at TU Darmstadt working on machine learning research. My work is scattered across different areas, but most connect directly to deep learning.
redirect_from: 
  - /about/
  - /about.html
---

I list my work on [axym.org](https://axym.org/work/):

<ul class="work-list">
{% for item in site.data.axym_work.items %}
  <li><a href="{{ item.url }}">{{ item.title }}</a> — {{ item.eyebrow | downcase }} [{{ item.date | slice: 0, 4 }}]</li>
{% endfor %}
</ul>

Reach me at: [davide.wiest2 [at] gmail [dot] com](mailto:davide.wiest2@gmail.com)
