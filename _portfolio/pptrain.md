---
title: "pptrain"
excerpt: "A PyTorch-native library for pre-pretraining language models on synthetic tasks"
collection: portfolio
link: "https://github.com/Axym-Labs/pptrain"
link_label: "Repository"
---

pptrain is a small PyTorch- and HuggingFace-native library for pre-pretraining language models. The idea is to train on synthetic tasks before standard language pretraining, with recent work showing gains beyond what additional natural-language pretraining alone achieves.

The library ships with six built-in task families---cellular automata, balanced-bracket sequences, procedural text tasks, symbolic operations, mathematical reasoning, and synthetic summarization---each with paper-backed presets that can be overridden for local experiments. Custom task families can be added by extending a flexible abstraction and plugging in a model adapter.

I built this because I wanted a single, consistent interface for experimenting with synthetic pretraining tasks without reimplementing the boilerplate each time. The library handles training, tokenizer plumbing, transfer-bundle export, and downstream integration.
