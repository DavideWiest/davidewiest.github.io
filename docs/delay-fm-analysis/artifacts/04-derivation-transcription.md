---
title: "Typed derivation for delay FM rewrite"
date: 2026-07-10
author: codex
status: temporary-writing-workflow
---

# Typed derivation for rewrite

## Endpoint recovery from two trajectory points

Assume a deterministic training trajectory whose state is linear in the endpoint
pair:

$$
x_r=\alpha_r x_0+\beta_r x_1.
$$

Here the endpoint pair means the ordered pair \((x_0,x_1)\). The first endpoint
comes from the source or noise distribution. The second endpoint comes from the
target or data distribution.

Let \(s=t-\tau\). The current point \(x_t\) and the earlier point \(x_s\) on the
same constructed trajectory satisfy

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

The determinant is

$$
\Delta_{t,s}=\alpha_t\beta_s-\alpha_s\beta_t.
$$

When \(\Delta_{t,s}\neq0\),

$$
x_0=\frac{\beta_s x_t-\beta_t x_s}{\Delta_{t,s}},
\qquad
x_1=\frac{-\alpha_s x_t+\alpha_t x_s}{\Delta_{t,s}}.
$$

This step assumes linearity in endpoints, not straightness as a function of
time.

## Target vector as an endpoint function

The vector-field target attached to the constructed path is

$$
u_t=\dot{\alpha}_t x_0+\dot{\beta}_t x_1.
$$

Substituting the recovered endpoints yields

$$
u_t(x,y)
=
\frac{(\dot{\alpha}_t\beta_s-\dot{\beta}_t\alpha_s)x
+(\alpha_t\dot{\beta}_t-\beta_t\dot{\alpha}_t)y}
{\Delta_{t,s}},
\qquad y=x_s.
$$

Thus the target can be written as a function of the model input
\((x_t,x_{t-\tau})\) whenever the endpoint-recovery determinant is nonzero.

## Ordinary FM and DFM optima

Ordinary FM uses

$$
\mathcal{L}_{\mathrm{FM}}(\theta)
=
\mathbb{E}\left[\|v_\theta(t,x_t)-u_t\|^2\right].
$$

The gradient is

$$
\nabla_\theta \mathcal{L}_{\mathrm{FM}}
=
2\mathbb{E}
\left[
(v_\theta(t,x_t)-u_t)^\top\nabla_\theta v_\theta(t,x_t)
\right],
$$

and the population minimizer is

$$
v^*_{\mathrm{FM}}(t,x)=\mathbb{E}[u_t\mid x_t=x].
$$

DFM uses

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}\left[\|v_\theta(t,x_t,x_{t-\tau})-u_t\|^2\right].
$$

The gradient is

$$
\nabla_\theta \mathcal{L}_{\mathrm{DFM}}
=
2\mathbb{E}
\left[
(v_\theta(t,x_t,x_{t-\tau})-u_t)^\top
\nabla_\theta v_\theta(t,x_t,x_{t-\tau})
\right],
$$

and the population minimizer is

$$
v^*_{\mathrm{DFM}}(t,x,y)
=
\mathbb{E}[u_t\mid x_t=x,\ x_{t-\tau}=y].
$$

Endpoint recovery makes the DFM conditioning much finer than the FM
conditioning. In the deterministic two-endpoint setting, it often fixes the
sampled endpoint pair.

## Endpoint recovery after one model evaluation

Let the first informative model evaluation occur at time \(t_*\), and let the
fitted model output be

$$
\widehat{u}_{t_*}=v_\theta(t_*,x_{t_*},x_{t_*-\tau}).
$$

For a linear-in-endpoints schedule, the current point and target vector satisfy

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

When

$$
\Gamma_{t_*}
=
\alpha_{t_*}\dot{\beta}_{t_*}
-\dot{\alpha}_{t_*}\beta_{t_*}
\neq0,
$$

the endpoint can be read out as

$$
\widehat{x}_1
=
\frac{-\dot{\alpha}_{t_*}x_{t_*}
+\alpha_{t_*}\widehat{u}_{t_*}}
{\Gamma_{t_*}}.
$$

At \(t_*=0\), common schedules have \(x_{t_*}=x_0\), \(\alpha_0=1\), and
\(\beta_0=0\). Then

$$
\widehat{x}_1
=
\frac{\widehat{u}_0-\dot{\alpha}_0x_0}{\dot{\beta}_0},
$$

provided \(\dot{\beta}_0\neq0\). For the straight scheduler this reduces to
\(\widehat{x}_1=x_0+\widehat{u}_0\).

After \(\widehat{x}_1\) is known, an endpoint-determined schedule gives the
remaining target vectors by formula. For the linear-in-endpoints class,

$$
\widehat{u}_r=\dot{\alpha}_r x_0+\dot{\beta}_r\widehat{x}_1.
$$

No further neural network evaluation is needed to determine the endpoint or the
endpoint-determined target field along the implied trajectory.

