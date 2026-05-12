---
title: "Gradient Routing for Continual Learning"
excerpt: "Evaluating sparsity and gradient-reweighted updates as a mechanism for continual learning"
collection: portfolio
link: "https://github.com/Axym-Labs/gradient-routing-continual-learning"
link_label: "Repository"
---

This project tests whether sparsity and sparse gradient routing can enable continual learning. The original hypothesis was straightforward: pretrain a model, make it somewhat sparse, and then route task gradients non-uniformly so that only a small subset of parameters adapts for each new task. The results were mostly negative.

On a PermutedMNIST benchmark with eight sequential tasks, plain all-layer sparse routing failed to improve over a dense SSL baseline. The root cause was that mild sparsity produced only 2–3% near-zero weights, and the routing rule still reused the same parameter support across tasks. Even forcing low-overlap, dormant-aware updates did not help, because most task-specific plasticity on PermutedMNIST is concentrated in the first composition layer, not distributed across the network.

The refined version that did work freezes the upper trunk after pretraining and only adapts a sparse first composition layer plus the classifier. Two variants were tested: power-law routing on the first layer, and a support-aware version that explicitly avoids previously-used weights and boosts dormant ones. Both improved over the baseline.

| Method | Final avg. accuracy | Avg. forgetting | Task-1 retention |
| --- | ---: | ---: | ---: |
| SSL baseline | 0.614 ± 0.028 | 0.363 ± 0.031 | 0.281 ± 0.083 |
| Power first-layer composer | 0.650 ± 0.012 | 0.278 ± 0.014 | 0.529 ± 0.011 |
| Support-aware first-layer composer | 0.645 ± 0.010 | 0.284 ± 0.012 | 0.496 ± 0.012 |

I also added a published SplitMNIST class-incremental benchmark to make forgetting unmistakable, and explored a task-blind online slot mechanism where sparse computation is discovered online by novelty detection. This reached 0.825 final accuracy with 0.215 forgetting, against a dense baseline of 0.199 with 0.998 forgetting.

The main lesson is that sparse gradient routing alone is too weak, but once sparse computation is localized to the right layer and discovered online, the original idea starts to work even without task identity.
