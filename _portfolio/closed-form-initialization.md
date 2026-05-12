---
title: "Closed-Form Initialization"
excerpt: "An analytical approach to neural network initialization using covariance and eigendecomposition"
collection: portfolio
link: "https://github.com/Axym-Labs/closed-form-initialization"
link_label: "Repository"
---

This project studies whether neural networks can be initialized analytically rather than randomly. The core idea is to build the encoder from paired training views using covariance, eigendecomposition, and ridge-style solves, then evaluate whether that analytic initialization helps downstream training.

The benchmark covers four scenarios: tabular classification, vision transformers on CIFAR-100, NLP on QNLI, and next-token prediction on WikiText-2. For each, we compare ordinary backprop from scratch against closed-form init followed by either full fine-tuning or a frozen encoder with only the classification head trained.

The main result is that closed-form init with compute-matched fine-tuning does not beat backprop at full budget on any scenario. The narrower positive signal is that freezing the encoder and training only the head is competitive on QNLI and in some low-data regimes. The practical bottleneck remains wall-clock efficiency, especially for transformers.

This was a useful negative result. It taught me that an elegant theoretical construction does not automatically translate into a practical win, and that systems efficiency---not just statistical properties---often determines whether a method is worth adopting.
