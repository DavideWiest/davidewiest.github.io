---
title: "Temporal Regularized Learning"
excerpt: "A highly local, self-supervised learning procedure that optimizes each neuron individually"
collection: portfolio
link: "https://github.com/Axym-Labs/TRL"
link_label: "Repository"
---

Temporal Regularized Learning (TRL) is a self-supervised procedure that optimizes each neuron individually, without backpropagation. It adapts the VICReg loss formulation---variance, invariance, and covariance---to input streams with sequential coherence, making it online-compatible.

The key design is that each neuron only needs three scalar memory units and an auxiliary lateral network. There is no need for biphasic updates, negative samples, or inner-loop convergence. Knowledge about downstream tasks can be injected through the sequence ordering, which means supervised training is possible without abandoning the local learning structure.

On MNIST, TRL is competitive with backpropagation, Forward-Forward, and Equilibrium Propagation. TRL-S, a simplified variant, achieves similar performance despite its reduced setup. The learned representations are interpretable: first-layer neurons develop specialized receptive fields, and deeper neurons activate selectively for specific input types.

I published a paper on this work, which is available on [Zenodo](https://doi.org/10.5281/zenodo.18673107).
