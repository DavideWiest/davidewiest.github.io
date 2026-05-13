---
title: "Gradient Routing for Continual Learning"
excerpt: "Evaluating sparsity and gradient-reweighted updates as a mechanism for continual learning"
collection: portfolio
date: 2026-02-01
link: "https://github.com/Axym-Labs/gradient-routing-continual-learning"
link_label: "Repository"
---

This project tests whether sparsity and sparse gradient routing can help with continual learning. The original idea was to pretrain a model, introduce some sparsity, and route task gradients non-uniformly so that only a small subset of parameters adapts for each new task.

On a PermutedMNIST benchmark with eight sequential tasks, plain all-layer sparse routing turned out to be insufficient as a standalone mechanism. The reason was that mild sparsity produced only 2–3% near-zero weights, and routing gradients across all layers still reused the same parameter support across tasks. However, once the idea was refined and localized, it became a useful auxiliary mechanism.

The version that works freezes the upper trunk after pretraining and only adapts a sparse first composition layer plus the classifier. Two variants were tested: power-law routing on the first layer, and a support-aware version that explicitly avoids previously-used weights and boosts dormant ones. Both improved over the baseline.

| Method | Final avg. accuracy | Avg. forgetting | Task-1 retention |
| --- | ---: | ---: | ---: |
| SSL baseline | 0.614 ± 0.028 | 0.363 ± 0.031 | 0.281 ± 0.083 |
| Power first-layer composer | 0.650 ± 0.012 | 0.278 ± 0.014 | 0.529 ± 0.011 |
| Support-aware first-layer composer | 0.645 ± 0.010 | 0.284 ± 0.012 | 0.496 ± 0.012 |

I also added a published SplitMNIST class-incremental benchmark and explored a task-blind online slot mechanism where sparse computation is discovered online by novelty detection. This reached 0.825 final accuracy with 0.215 forgetting, against a dense baseline of 0.199 with 0.998 forgetting.

The takeaway is that sparse gradient routing works best as an auxiliary mechanism rather than a standalone solution. Localizing plasticity to the right layer helps, and discovering sparse computation online without task identity is possible, but in practice one still needs stronger structural mechanisms to meaningfully reduce forgetting at scale.
