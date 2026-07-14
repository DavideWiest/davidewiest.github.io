---
title: "Sentence audit for final revised sections"
date: 2026-07-10
author: codex
status: temporary-writing-workflow
---

# Sentence audit for final revised sections

This audit covers the second pass on the newly revised sections. Earlier
sections were left intact except for citation consistency.

## 4. Gradients and trajectory continuation

- "Flow-matching models are trained..." gives the high-level training procedure
  before any gradient formula.
- "This simulation-free regression view..." anchors the training description in
  FM, CFM, and stochastic interpolants with citations.
- "For DFM, the per-sample gradient..." introduces the mathematical object for a
  single sampled training tuple.
- "For the straight schedule..." names the schedule class and cites the
  straight-path / OT-style literature.
- "When \(t>\tau\)..." states the delayed displacement identity before
  substituting it into the gradient.
- "In the initial-history window..." handles \(0<t<\tau\) without expanding the
  section into a second derivation.
- "For a cosine or VP-style schedule..." cites diffusion and score-SDE sources
  before introducing \(\alpha_r=\cos\phi_r\), \(\beta_r=\sin\phi_r\).
- "With \(s=t-\tau\)..." gives the scheduler-specific target produced by the
  endpoint-recovery formula.
- "Both substitutions have the same structure." introduces the interpretation
  without anthropomorphic "the model is asked" phrasing.
- "Conditional on..." defines the schedule-determined continuation target
  \(F_t(x_t,x_{t-\tau})\).
- "The parameter update..." states the objective-level distinction from the
  marginal conditional mean.
- "At the beginning..." links the gradient argument to sampling.
- "In ordinary distribution transport..." states why the endpoint coupling is
  the learned choice.
- "This is why DFM..." introduces source-conditioned FM and ABM as relatives,
  not as unexplained labels.
- "Here source-conditioned FM..." defines the term.
- "Augmented Bridge Matching..." cites the coupling-preservation claim.
- "DFM has a similar effect..." states the mechanism.
- "In this setting..." separates the schedule-supplied formula from the learned
  coupling.
- "The next two sections..." gives the reader the transition to consequences.

## 5. Sampling efficiently from DFM models

- "The endpoint-recovery formula..." references the previous derivation instead
  of repeating it.
- "For sampling..." sets \(t=0\) and identifies the target endpoint as the
  time-\(1\) endpoint \(x_1\).
- "In practice..." introduces the linear-in-endpoints scheduler condition.
- "\(\widehat{u}_0=v_\theta(0,x_0,x_0)\)" states the first informative
  prediction.
- "The target equation..." gives the only needed algebraic relation.
- "If \(\dot{\beta}_0\neq0\)..." states the endpoint readout condition.
- "For the straight scheduler..." derives \(\widehat{x}_1=x_0+\widehat{u}_0\).
- "For the cosine..." derives \(\widehat{x}_1=\widehat{u}_0/\dot{\phi}_0\).
- "After this readout..." states why later target vectors are analytic.
- "Additional network calls..." scopes the claim to fitted endpoint-determined
  behavior.
- "This endpoint readout..." distinguishes the argument from distillation and
  flow-map matching.

## 6. Coupling choice

- "The practical implication..." states the section claim directly.
- "If the endpoint pairs..." avoids anthropomorphic phrasing and says the DFM
  objective ties the model to product-coupled pairs.
- "Such a model..." avoids claiming product-coupled DFM cannot sample well.
- "The extra input..." distinguishes DFM from an improved marginal FM objective.
- "DFM is most natural..." gives the recommendation.
- "The pairing might..." cites OT, minibatch coupling, bridge matching, and ABM.
- "In those cases..." states why the extra input is useful.

## 7. Delayed dynamical systems

- "The analysis above..." states the scope boundary.
- "In a DDE..." gives the governing form.
- "the earlier state..." explains why the DDE setting differs from endpoint
  interpolation.
- "This is the setting..." cites NODE, NDDE, trajectory FM, and DFM.
- "Snapshot-to-snapshot..." gives the valid application class.
- "DFM can..." states the positive but bounded claim.
- "The remaining modeling question..." keeps constructed paths separate from
  true dynamics.
- "If those paths..." states what DFM learns under OT/KPG-OT/spline/geodesic
  construction.

## Checks Applied

- Replaced "These examples show..." with a more precise statement about the
  DFM gradient residual and a schedule-determined continuation target.
- Replaced "DFM does not ask..." with objective-level wording.
- Replaced "closest conceptual relatives" with "DFM is best interpreted as a
  close relative of..." and introduced source-conditioned FM before using it.
- Added citations at the claims they support.
- Removed "chord" and retained "trajectory" / "continuation" language.

