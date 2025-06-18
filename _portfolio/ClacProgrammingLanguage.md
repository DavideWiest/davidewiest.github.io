---
title: "Clac"
excerpt: "A series of programming language projects"
collection: portfolio
---
**[-> repository](https://github.com/DavideWiest/Clac3)**

## Details
- **Clac3 is a flexible backend with the advantage of powerful macro expressions**: It is a programming langauge backend that builds on patterns. It takes a program in form of an abstract syntax tree and a set of patterns as input. It then builds a decision tree of these patterns and applies them to the inputs until no pattern matches. This allows for powerful macros and flexible frontends aswell as metaprogramming, since the macros that can define language syntax are specified inside the program. When all patterns have been applied, the program is converted into functional form and can be executed by a builtin interpreter. A LLVM-based execution backend could likewise be hooked up. 
- **Clac2 is a rudimentary, functional programming language.** I used the devleopment process to learn the basics of building an interpreter with frontend and to learn the F# programming language. While it does work, I stopped at the implementation of branching (if) Statements and switched to Clac3. 
- Clac was an experiment to implement the architecture and basics of an interpreter. It was quickly discarded for a better approach.

