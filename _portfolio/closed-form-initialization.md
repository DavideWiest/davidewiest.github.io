---
title: "Closed-Form Initialization"
excerpt: "An analytical approach to neural network initialization using covariance and eigendecomposition"
collection: portfolio
date: 2026-03-01
link: "https://github.com/Axym-Labs/closed-form-initialization"
link_label: "Repository"
---

This project explores whether neural networks can be initialized analytically rather than randomly. The core achievement is a closed-form parametrization of an MLP encoder: given paired training views, the model is built from covariance estimates, eigendecomposition, and ridge-style solves, without any end-to-end gradient descent. We empirically found out that our novel combination of SSL parameterization with a residual supervised (least squares) path is cricial, as nearby setups did not yield satisfactory results.

For transformers, this approach yields a spectral self-attention block plus analytically fitted feed-forward maps. The benchmark covers four scenarios: tabular classification, vision transformers on CIFAR-100, NLP on QNLI, and next-token prediction on WikiText-2. Comparing ordinary backprop from scratch against closed-form init is followed by either full fine-tuning or a frozen encoder with only the head trained.

The main practical bottleneck right now is wall-clock efficiency, especially for transformers. Still, the fact that an MLP can be parametrized in closed form at all is non-trivial, and the approach remains an interesting direction for research into initialization schemes that carry structural information from data before any gradient steps are taken.
