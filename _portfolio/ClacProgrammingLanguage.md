---
title: "Clac"
excerpt: "A series of programming language projects exploring pattern matching, macro expansion, and interpreter design"
collection: portfolio
date: 2024-01-01
link: "https://github.com/DavideWiest/Clac3"
link_label: "Repository"
---

Clac3 is a programming language backend built around pattern matching. It takes an abstract syntax tree and a set of patterns as input, then constructs a decision tree and applies patterns until none match. This design enables powerful macros and flexible frontends: the macros that define language syntax live inside the program itself, which makes metaprogramming a first-class concern. Once pattern matching completes, the program is converted to functional form and executed by a built-in interpreter. An LLVM-based backend could be plugged in later.

There were also two predecessor versions, which I will briefly mention for the sake of context.

Clac2 was a simpler functional language built to learn interpreter construction and F#. It handled basic expressions and functions but stalled at branching.

The original Clac was a quick experiment to understand interpreter structure. It was abandoned almost immediately, but it clarified what not to do.
