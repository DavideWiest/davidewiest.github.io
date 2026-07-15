---
title: "pptrain"
excerpt: "A PyTorch-native library for pre-pretraining language models on synthetic tasks"
collection: portfolio
date: 2026-04-01
hidden: true
link: "https://github.com/Axym-Labs/pptrain"
link_label: "Repository"
---

pptrain is a small PyTorch- and HuggingFace-native library for pre-pretraining language models. The idea is to train on synthetic tasks before standard language pretraining, with recent work showing gains beyond what additional natural-language pretraining alone achieves.

The library ships with six built-in task families---cellular automata, balanced-bracket sequences, procedural text tasks, symbolic operations, mathematical reasoning, and synthetic summarization---each with paper-backed presets that can be overridden for local experiments. Custom task families can be added by extending a flexible abstraction and plugging in a model adapter. To prevent hidden issues, the codebase contains logic that compares pptrain's output to the offical codebase of the papers that introduced these mechanisms.

I built this because I wanted a single, consistent interface for experimenting with synthetic pretraining tasks without reimplementing the boilerplate each time. The library handles tokenizer plumbing, transfer-bundle export, parts of training, and downstream integration.
