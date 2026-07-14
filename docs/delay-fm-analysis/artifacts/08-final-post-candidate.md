---
title: "Delay Flow Matching learns the coupling"
date: 2026-07-10
permalink: /posts/2026/07/delay-flow-matching-learns-the-coupling/
tags:
  - machine-learning
  - flow-matching
  - generative-models
  - theory
---

## Summary

Delay Flow Matching (DFM) changes the conditioning variables of the learned vector field. Ordinary flow matching trains a vector field \(v_\theta(t,x_t)\) against target vectors along constructed probability paths. DFM trains \(v_\theta(t,x_t,x_{t-\tau})\), where \(x_{t-\tau}\) is an earlier point on the same constructed trajectory. In a genuine delayed dynamical system, that earlier point is part of the state needed to determine the derivative. In ordinary distribution transport, the trajectory is usually built from an endpoint pair \((x_0,x_1)\). For common deterministic interpolants, the two points \((x_t,x_{t-\tau})\) identify that endpoint pair. The DFM objective therefore conditions on the sampled coupling. It learns the target vector attached to the selected endpoint pair rather than the marginal vector field learned by ordinary FM. This note gives the endpoint-recovery calculation, compares the two squared-error objectives, and explains why one informative model evaluation can determine the implied endpoint whenever the target is endpoint-determined and the schedule gives an invertible readout.

## Introduction

The standard flow-matching setting starts with two distributions and a rule for pairing samples from them. We draw or choose an endpoint pair \((x_0,x_1)\), construct a path between the endpoints, and train a neural vector field on target vectors along that path.

In this note, the endpoint pair always means the ordered pair \((x_0,x_1)\). The first endpoint \(x_0\) comes from the source or noise distribution. The second endpoint \(x_1\) comes from the target or data distribution. The coupling is the joint distribution that tells us which \(x_0\) is paired with which \(x_1\).

The claim is narrow. In the ordinary two-endpoint setting, DFM gives the model enough information to recover the sampled endpoint pair in many common cases. Once this happens, the training objective asks the model to preserve the chosen coupling.

## 1. Flow matching setup

Ordinary flow matching constructs a conditional trajectory from each sampled endpoint pair. For a broad class of schedules,

$$
x_t=\alpha_t x_0+\beta_t x_1.
$$

The vector-field target on that constructed trajectory is

$$
u_t=\dot{\alpha}_t x_0+\dot{\beta}_t x_1.
$$

FM trains \(v_\theta(t,x_t)\) by minimizing

$$
\mathcal{L}_{\mathrm{FM}}(\theta)
=
\mathbb{E}
\left[
\left\|v_\theta(t,x_t)-u_t\right\|^2
\right].
$$

The population minimizer of this squared-error objective is

$$
v^*_{\mathrm{FM}}(t,x)=\mathbb{E}[u_t\mid x_t=x].
$$

This is the marginal vector field. If different endpoint pairs pass through the same \(x_t\), ordinary FM averages their target vectors.

## 2. Delay FM's objective

DFM changes the conditioning information. It trains a vector field of the form

$$
v_\theta(t,x_t,x_{t-\tau}),
$$

where \(x_{t-\tau}\) is an earlier point on the same constructed training trajectory. This earlier point changes the statistical meaning of the objective.

DFM minimizes

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}
\left[
\left\|v_\theta(t,x_t,x_{t-\tau})-u_t\right\|^2
\right].
$$

The corresponding population minimizer is

$$
v^*_{\mathrm{DFM}}(t,x,y)
=
\mathbb{E}[u_t\mid x_t=x,\ x_{t-\tau}=y].
$$

Compare this with ordinary FM,

$$
v^*_{\mathrm{FM}}(t,x)=\mathbb{E}[u_t\mid x_t=x].
$$

The difference is the conditioning event. Ordinary FM averages over all endpoint pairs compatible with \(x_t=x\). DFM conditions on both \(x_t=x\) and \(x_{t-\tau}=y\). In the deterministic two-endpoint setting, this finer conditioning often fixes the endpoint pair. The objective then asks the model to predict the target vector associated with the sampled coupling.

## 3. Endpoint recovery from two trajectory points

Set \(s=t-\tau\). The current point \(x_t\) and the earlier point \(x_s\) give a coordinatewise \(2\times2\) linear system for the endpoint pair. When \(\Delta_{t,s}=\alpha_t\beta_s-\alpha_s\beta_t\neq0\), the endpoint pair is recovered by

$$
x_0=\frac{\beta_s x_t-\beta_t x_s}{\Delta_{t,s}},
\qquad
x_1=\frac{-\alpha_s x_t+\alpha_t x_s}{\Delta_{t,s}}.
$$

The model input \((x_t,x_{t-\tau})\) can identify the endpoint pair \((x_0,x_1)\). The calculation does not require a straight trajectory. It only uses linearity in the endpoints and the nonzero determinant condition above.

The target vector is also determined by these two points. Substituting the endpoint formulas into \(u_t=\dot{\alpha}_t x_0+\dot{\beta}_t x_1\) gives

$$
u_t(x,y)
=
\frac{(\dot{\alpha}_t\beta_s-\dot{\beta}_t\alpha_s)x
+(\alpha_t\dot{\beta}_t-\beta_t\dot{\alpha}_t)y}
{\Delta_{t,s}},
\qquad y=x_s.
$$

For a straight, linear-in-time schedule, this expression becomes a scalar multiple of the displacement from the earlier trajectory point to the current one. For cosine or VP-style schedules, it is a different deterministic continuation map from the same two trajectory points. The schedule changes the continuation map, not the fact that the two trajectory points identify the endpoints.

## 4. Gradients and trajectory continuation

Flow-matching models are trained by sampling endpoint pairs, sampling times, constructing the corresponding trajectory points, and minimizing mean squared error to the target vector \(u_t\). This simulation-free regression view is the common backbone of flow matching, conditional flow matching, and stochastic interpolants ([Lipman et al. 2022](https://arxiv.org/abs/2210.02747), [Tong et al. 2023](https://arxiv.org/abs/2302.00482), [Albergo et al. 2023](https://arxiv.org/abs/2303.08797)). For DFM, the per-sample gradient at \(t>0\) has the form

$$
\nabla_\theta \ell_{\mathrm{DFM}}
=
2
\left(
v_\theta(t,x_t,x_{t-\tau})-u_t
\right)^\top
\nabla_\theta v_\theta(t,x_t,x_{t-\tau}).
$$

For the straight schedule used by rectified-flow and OT-style FM constructions ([Liu et al. 2022](https://arxiv.org/abs/2209.03003), [Tong et al. 2023](https://arxiv.org/abs/2302.00482), [Pooladian et al. 2023](https://arxiv.org/abs/2304.14772)),

$$
x_r=(1-r)x_0+r x_1,\qquad u_t=x_1-x_0.
$$

When \(t>\tau\),

$$
x_t-x_{t-\tau}=\tau(x_1-x_0),
$$

so the DFM gradient becomes

$$
\nabla_\theta \ell_{\mathrm{DFM}}
=
2
\left(
v_\theta(t,x_t,x_{t-\tau})
-
\frac{x_t-x_{t-\tau}}{\tau}
\right)^\top
\nabla_\theta v_\theta(t,x_t,x_{t-\tau}).
$$

In the initial-history window \(0<t<\tau\), the same substitution gives \(x_{t-\tau}=x_0\) and replaces \(\tau\) by \(t\).

For a cosine or VP-style schedule, as used in diffusion and score-SDE parameterizations ([Ho et al. 2020](https://arxiv.org/abs/2006.11239), [Song et al. 2020](https://arxiv.org/abs/2011.13456), [Lipman et al. 2022](https://arxiv.org/abs/2210.02747)),

$$
\alpha_r=\cos \phi_r,\qquad \beta_r=\sin \phi_r.
$$

With \(s=t-\tau\), endpoint recovery gives

$$
u_t(x_t,x_s)
=
\dot{\phi}_t
\frac{\cos(\phi_t-\phi_s)x_t-x_s}{\sin(\phi_t-\phi_s)}.
$$

The corresponding gradient is

$$
\nabla_\theta \ell_{\mathrm{DFM}}
=
2
\left(
v_\theta(t,x_t,x_s)
-
\dot{\phi}_t
\frac{\cos(\phi_t-\phi_s)x_t-x_s}{\sin(\phi_t-\phi_s)}
\right)^\top
\nabla_\theta v_\theta(t,x_t,x_s).
$$

Both substitutions have the same structure. Conditional on \((x_t,x_{t-\tau})\), the residual in the DFM gradient is measured against a schedule-determined continuation target \(F_t(x_t,x_{t-\tau})\). The parameter update is therefore organized around trajectory continuation rather than the marginal conditional mean \(\mathbb{E}[u_t\mid x_t]\). At the beginning of a rollout, the first informative model prediction selects an implied endpoint. In ordinary distribution transport, that selection depends on the endpoint coupling used during training.

This is why DFM is best interpreted as a close relative of source-conditioned FM and Augmented Bridge Matching. Here source-conditioned FM means the variant in which the vector field also receives the source endpoint \(x_0\). Augmented Bridge Matching studies the same kind of augmentation in bridge matching and shows how it preserves empirical pairings ([De Bortoli et al. 2023](https://arxiv.org/abs/2311.06978)). DFM has a similar effect because the earlier trajectory point can identify the endpoint pair. In this setting, the schedule supplies the continuation formula, and the learned part is the coupling. The next two sections spell out two consequences.

## 5. Sampling efficiently from DFM models

The endpoint-recovery formula from Section 3 already gives \(x_1\) once two trajectory points are known. For sampling, the analogous first-step calculation uses the starting point at time \(0\) and the target vector predicted by the model. The endpoint we want is the time-\(1\) endpoint \(x_1\).

In practice, the DFM and FM schedules considered above are linear in the endpoint pair. For these schedulers, the first informative model output can be written as

$$
\widehat{u}_0=v_\theta(0,x_0,x_0).
$$

The target equation at \(t=0\) is

$$
\widehat{u}_0
\approx
\dot{\alpha}_0 x_0+\dot{\beta}_0 x_1.
$$

If \(\dot{\beta}_0\neq0\), the endpoint readout is

$$
\widehat{x}_1
=
\frac{\widehat{u}_0-\dot{\alpha}_0x_0}{\dot{\beta}_0}.
$$

For the straight scheduler, \(\dot{\alpha}_0=-1\) and \(\dot{\beta}_0=1\), so

$$
\widehat{x}_1=x_0+\widehat{u}_0.
$$

For the cosine or VP-style scheduler with \(\alpha_t=\cos\phi_t\), \(\beta_t=\sin\phi_t\), and \(\phi_0=0\),

$$
\dot{\alpha}_0=0,\qquad \dot{\beta}_0=\dot{\phi}_0,
$$

and therefore

$$
\widehat{x}_1=\frac{\widehat{u}_0}{\dot{\phi}_0}.
$$

After this readout, later target vectors along the implied trajectory are available from the scheduler. For the linear-in-endpoints class,

$$
\widehat{u}_r=\dot{\alpha}_r x_0+\dot{\beta}_r\widehat{x}_1.
$$

Additional network calls may still change a finite-capacity numerical rollout. They do not add endpoint information in the fitted endpoint-determined setting. This endpoint readout is also different from distillation or learned flow-map methods, which train an additional map to reduce the number of integration steps ([Boffi et al. 2024](https://arxiv.org/abs/2406.07507)).

## 6. Coupling choice

The practical implication is that the coupling matters. If the endpoint pairs come from a product coupling, the DFM objective ties the model to arbitrary noise-data pairings. Such a model may still generate plausible samples after finite-capacity smoothing and numerical approximation. The extra input is not solving a better version of the ordinary marginal FM objective in that case.

DFM is most natural when the endpoint pairing is meaningful. The pairing might come from known source-target examples, optimal transport, minibatch matching, bridge matching, or another domain-specific construction ([Tong et al. 2023](https://arxiv.org/abs/2302.00482), [Pooladian et al. 2023](https://arxiv.org/abs/2304.14772), [Shi et al. 2023](https://arxiv.org/abs/2303.16852), [Tong et al. 2023b](https://arxiv.org/abs/2307.03672), [De Bortoli et al. 2023](https://arxiv.org/abs/2311.06978)). In those cases, the extra input gives the model information that the task actually wants to preserve.

## 7. Delayed dynamical systems

The analysis above does not apply to genuine delayed dynamics. In a DDE,

$$
\dot{x}(t)=f(x(t),x(t-\tau)),
$$

the earlier state \(x(t-\tau)\) is part of the physical state. It is not merely a code for a sampled endpoint pair. The path is not an interpolation between two endpoints. This is the setting where neural DDE models and trajectory-oriented flow-matching methods are relevant rather than just endpoint-pair interpolation ([Chen et al. 2018](https://arxiv.org/abs/1806.07366), [Zhu et al. 2021](https://arxiv.org/abs/2102.10801), [Zhang et al. 2024](https://arxiv.org/abs/2410.21154), [Zhao et al. 2026](https://openreview.net/forum?id=6lH1XblLpo)).

Snapshot-to-snapshot delayed distribution transport is therefore a different setting. DFM can be a reasonable way to give an FM-like model the variables needed by a delayed system. The remaining modeling question is whether the constructed latent paths between snapshots match the true dynamics closely enough. If those paths are built by OT, KPG-OT, splines, or geodesics, DFM learns the delayed flow induced by that construction.

## References

- Zhao et al., [Delay Flow Matching](https://openreview.net/forum?id=6lH1XblLpo), ICLR 2026.
- Lipman et al., [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747), 2022.
- Tong et al., [Improving and generalizing flow-based generative models with minibatch optimal transport](https://arxiv.org/abs/2302.00482), 2023.
- Albergo et al., [Stochastic Interpolants: A Unifying Framework for Flows and Diffusions](https://arxiv.org/abs/2303.08797), 2023.
- Liu et al., [Flow Straight and Fast](https://arxiv.org/abs/2209.03003), 2022.
- Pooladian et al., [Multisample Flow Matching](https://arxiv.org/abs/2304.14772), 2023.
- Ho et al., [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239), 2020.
- Song et al., [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456), 2020.
- De Bortoli et al., [Augmented Bridge Matching](https://arxiv.org/abs/2311.06978), 2023.
- Shi et al., [Diffusion Schrödinger Bridge Matching](https://arxiv.org/abs/2303.16852), 2023.
- Tong et al., [Simulation-free Schrödinger bridges via score and flow matching](https://arxiv.org/abs/2307.03672), 2023.
- Boffi et al., [Flow Map Matching](https://arxiv.org/abs/2406.07507), 2024.
- Chen et al., [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366), 2018.
- Zhu et al., [Neural Delay Differential Equations](https://arxiv.org/abs/2102.10801), 2021.
- Zhang et al., [Trajectory Flow Matching with Applications to Clinical Time Series Modeling](https://arxiv.org/abs/2410.21154), 2024.
