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

## Abstract

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

DFM changes the conditioning information. It trains a vector field of the form

$$
v_\theta(t,x_t,x_{t-\tau}),
$$

where \(x_{t-\tau}\) is an earlier point on the same constructed training trajectory. This earlier point changes the statistical meaning of the objective.

## 2. Endpoint recovery from two trajectory points

Set \(s=t-\tau\). The current point and the earlier point satisfy

$$
\begin{pmatrix}
x_t\\
x_s
\end{pmatrix}
=
\begin{pmatrix}
\alpha_t & \beta_t\\
\alpha_s & \beta_s
\end{pmatrix}
\begin{pmatrix}
x_0\\
x_1
\end{pmatrix}.
$$

This equation is a coordinatewise \(2\times2\) linear system. When

$$
\Delta_{t,s}=\alpha_t\beta_s-\alpha_s\beta_t\neq0,
$$

the endpoint pair is recovered by

$$
x_0=\frac{\beta_s x_t-\beta_t x_s}{\Delta_{t,s}},
\qquad
x_1=\frac{-\alpha_s x_t+\alpha_t x_s}{\Delta_{t,s}}.
$$

The model input \((x_t,x_{t-\tau})\) can identify the endpoint pair \((x_0,x_1)\). The calculation does not require the path to be straight as a function of time. It only uses linearity in the endpoints and the nonzero determinant condition above.

The target vector is also determined by these two points. Substituting the endpoint formulas into \(u_t=\dot{\alpha}_t x_0+\dot{\beta}_t x_1\) gives

$$
u_t(x,y)
=
\frac{(\dot{\alpha}_t\beta_s-\dot{\beta}_t\alpha_s)x
+(\alpha_t\dot{\beta}_t-\beta_t\dot{\alpha}_t)y}
{\Delta_{t,s}},
\qquad y=x_s.
$$

For the straight scheduler, this expression becomes a scalar multiple of \(x_t-x_{t-\tau}\). For cosine or VP-style schedules, it is still a simple linear expression in \(x_t\) and \(x_{t-\tau}\), but not the same chord formula. The endpoint-recovery claim is the general point.

## 3. Delay FM's objective

DFM minimizes

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}
\left[
\left\|v_\theta(t,x_t,x_{t-\tau})-u_t\right\|^2
\right].
$$

Its gradient is

$$
\nabla_\theta \mathcal{L}_{\mathrm{DFM}}
=
2\mathbb{E}
\left[
(v_\theta(t,x_t,x_{t-\tau})-u_t)^\top
\nabla_\theta v_\theta(t,x_t,x_{t-\tau})
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

The difference is the conditioning event. Ordinary FM averages over all endpoint pairs compatible with \(x_t=x\). DFM conditions on both \(x_t=x\) and \(x_{t-\tau}=y\). In the deterministic two-endpoint setting, this finer conditioning often fixes the endpoint pair. The objective is then fitting the target vector associated with the sampled coupling.

This is why source-conditioned FM and Augmented Bridge Matching are the closest conceptual relatives. When the model receives the source endpoint, the objective no longer asks for the unconditional marginal field. When the model receives enough information to recover both endpoints, the conditioning is even sharper. Both cases preserve information about the source-target coupling that ordinary FM marginalizes away.

## 4. Endpoint recovery after one model evaluation

The same endpoint logic has a sampling consequence. Suppose the target vector is determined by the endpoint pair. After an informative fitted model evaluation, the implied endpoint can often be recovered without running the neural network again.

For the linear-in-endpoints schedule, let the first informative model output be

$$
\widehat{u}_{t_*}=v_\theta(t_*,x_{t_*},x_{t_*-\tau}).
$$

The current point and target vector satisfy

$$
\begin{pmatrix}
x_{t_*}\\
u_{t_*}
\end{pmatrix}
=
\begin{pmatrix}
\alpha_{t_*} & \beta_{t_*}\\
\dot{\alpha}_{t_*} & \dot{\beta}_{t_*}
\end{pmatrix}
\begin{pmatrix}
x_0\\
x_1
\end{pmatrix}.
$$

If

$$
\Gamma_{t_*}
=
\alpha_{t_*}\dot{\beta}_{t_*}
-\dot{\alpha}_{t_*}\beta_{t_*}
\neq0,
$$

then a fitted prediction gives

$$
\widehat{x}_1
=
\frac{-\dot{\alpha}_{t_*}x_{t_*}
+\alpha_{t_*}\widehat{u}_{t_*}}
{\Gamma_{t_*}}.
$$

For common schedules at \(t_*=0\), \(x_{t_*}=x_0\), \(\alpha_0=1\), and \(\beta_0=0\). Then

$$
\widehat{x}_1
=
\frac{\widehat{u}_0-\dot{\alpha}_0x_0}{\dot{\beta}_0},
$$

provided \(\dot{\beta}_0\neq0\). The straight scheduler has \(\dot{\alpha}_0=-1\) and \(\dot{\beta}_0=1\), so this reduces to

$$
\widehat{x}_1=x_0+\widehat{u}_0.
$$

This is not a statement about straight paths only. The sufficient condition is that the endpoint can be read out from the fitted target and the known schedule. Once \(\widehat{x}_1\) is known, later target vectors along the implied trajectory are computable from the schedule. For the linear-in-endpoints class,

$$
\widehat{u}_r=\dot{\alpha}_r x_0+\dot{\beta}_r\widehat{x}_1.
$$

Further network calls may still change a finite-capacity numerical rollout. They do not add new endpoint information in the fitted endpoint-determined setting.

## 5. Coupling choice

The practical implication is that the coupling matters. If the endpoint pairs come from a product coupling, DFM is asked to preserve arbitrary noise-data pairings. Such a model may still generate plausible samples after finite-capacity smoothing and numerical approximation. The extra input is not solving a better version of the ordinary marginal FM objective in that case.

DFM is most natural when the endpoint pairing is meaningful. The pairing might come from known source-target examples, optimal transport, minibatch matching, keypoint guidance, or another domain-specific construction. In those cases, the extra input gives the model information that the task actually wants to preserve.

## 6. Delayed dynamical systems

The analysis above does not apply to genuine delayed dynamics. In a DDE,

$$
\dot{x}(t)=f(x(t),x(t-\tau)),
$$

the earlier state \(x(t-\tau)\) is part of the physical state. It is not merely a code for a sampled endpoint pair. The path is not an interpolation between two endpoints.

Snapshot-to-snapshot delayed distribution transport is therefore a different setting. DFM can be a reasonable way to give an FM-like model the variables needed by a delayed system. The remaining modeling question is whether the constructed latent paths between snapshots match the true dynamics closely enough. If those paths are built by OT, KPG-OT, splines, or geodesics, DFM learns the delayed flow induced by that construction.

## References

- Zhao et al., [Delay Flow Matching](https://openreview.net/forum?id=6lH1XblLpo), ICLR 2026.
- Lipman et al., [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747), 2022.
- Tong et al., [Improving and generalizing flow-based generative models with minibatch optimal transport](https://arxiv.org/abs/2302.00482), 2023/2024.
- Liu et al., [Flow Straight and Fast](https://arxiv.org/abs/2209.03003), 2022.
- De Bortoli et al., [Augmented Bridge Matching](https://arxiv.org/abs/2311.06978), 2023.

