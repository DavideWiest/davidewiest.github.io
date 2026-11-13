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

{% assign work = site.data.axym_work.items %}
{% assign shown = 4 %}
I list my work on [axym.org](https://axym.org/work/):

<ul class="work-list">
{% for item in work %}
  <li{% if forloop.index > shown %} class="work-list__more" hidden{% endif %}><a href="{{ item.url }}">{{ item.title }}</a> — {{ item.eyebrow | downcase }} [{{ item.date | slice: 0, 4 }}]</li>
{% endfor %}
</ul>
{% if work.size > shown %}
<p class="work-list__toggle">(<a href="https://axym.org/work/" id="work-list-more">show {{ work.size | minus: shown }} more items</a>)</p>
<script>
  document.getElementById("work-list-more").addEventListener("click", function (event) {
    event.preventDefault();
    document.querySelectorAll(".work-list__more").forEach(function (item) { item.hidden = false; });
    this.parentElement.remove();
  });
</script>
{% endif %}

Reach me at: [davide.wiest2 [at] gmail [dot] com](mailto:davide.wiest2@gmail.com)
