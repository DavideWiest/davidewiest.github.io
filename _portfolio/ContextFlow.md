---
title: "ContextFlow"
hidden: true
sitemap: false
excerpt: "A .NET library for building structured LLM interactions through dependency injection and fluent interfaces"
collection: portfolio
link: "https://github.com/DavideWiest/ContextFlow"
link_label: "Repository"
---

ContextFlow is a .NET library for interacting with large language models at a higher level of abstraction than raw API calls. It provides modular components that work together through dependency injection, making it possible to build complex prompt chains and pipelines without losing track of state. The library includes a fluent interface for prompt templating and chaining, asynchronous counterparts for all operations, and 55 NUnit tests covering the core functionality.

During development, maintainability metrics were kept within strict bounds: cyclomatic complexity below 6 per method, class coupling below 10, and a Maintainability Index of 82. The [documentation](https://github.com/DavideWiest/ContextFlow/wiki) covers usage patterns and architecture decisions.
