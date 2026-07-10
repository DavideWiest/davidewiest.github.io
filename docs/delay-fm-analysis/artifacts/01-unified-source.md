---
title: "Unified source notes for delay FM article"
date: 2026-07-10
author: codex
status: temporary-working-source
---

# Unified source notes for delay FM article

This file translates the PDF report and its embedded images into one working
markdown source. It preserves the useful source material while separating it
from the reformulated article argument.

## Source summary

The source report makes three working claims:

1. In the standard FM setting, delay FM is an objective mismatch when the source
   and target distributions are merely two endpoint distributions, not
   time-indexed states of a delayed dynamical system.
2. In that setting, delay FM fits the selected source-target coupling. The first
   delayed prediction identifies the path or the implied endpoint; later
   predictions mostly follow that revealed path.
3. Delay FM can still be valid for DDE or snapshot-to-snapshot dynamical-system
   settings, where the delayed state is real state information rather than just
   a code for the endpoint pair.

The intended article should keep the first two claims as the main argument and
move the third claim into a caveat.

## DDE setting notes

The DDE notes argue that modeling DDEs inside an FM-like framework can make
sense in a specific setting: snapshot-to-snapshot distribution transport. A
recurrent model typically wants sequences or trajectory supervision. DFM instead
tries to learn a delayed probability flow from distributions observed at times
\(t_0,t_1,\ldots\), often using OT or KPG-OT to construct latent trajectories
between snapshots.

The useful part is not "individual trajectory recovery" by default. The model
learns a coupling and a constructed trajectory. If the constructed path matches
the real dynamics, for example through a good spline or geodesic construction,
then DFM may approximate intermediate distributions. That is why snapshot data
and single-cell-like cross-sectional data are plausible application domains.

For true DDE examples, the delayed state is genuinely necessary:

$$
\dot{x}(t)=f(x_t,x_{t-\tau}),
$$

and the notes mention examples such as

$$
\dot{x}(t)=\frac{\eta}{1+x^n(t-\tau)}
$$

and

$$
\dot{x}(t)=A\tanh(x(t)+x(t-\tau)).
$$

Given \(x_t\) alone, the derivative is not determined. Given
\((x_t,x_{t-\tau})\), the vector field is at least representable. This caveat is
valid, but it is not the main blog-post argument.

## Source-conditioned FM / augmented bridge matching note

The source note says:

> Source-conditioned FM is best read as Augmented Bridge Matching. It is not
> mainly motivated for ordinary unconditional generation. The paper frames the
> issue as preserving an empirical coupling / original pairing in arbitrary
> transfer tasks, especially image translation or paired bridge settings. It
> explicitly says conditioning on the initial sample preserves coupling but loses
> Markovianity.

For the article, this becomes the bridge to the second takeaway: once the model
is conditioned on enough information to identify the source-target pairing, the
training objective asks it to preserve that pairing. Delay FM with
\(\tau=t\) is source-conditioned FM, because \(x_{t-\tau}=x_0\).

## Core derivation: endpoint inversion from delayed pair

For deterministic two-endpoint paths, assume

$$
x_r=\alpha_r x_0+\beta_r x_1,\qquad s=t-\tau.
$$

Write the current and delayed states as

$$
x=x_t,\qquad y=x_s=x_{t-\tau}.
$$

Coordinatewise, the delayed pair is a \(2\times 2\) linear system in the two
unknown endpoint vectors:

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

It is invertible when

$$
\Delta_{t,s}:=\alpha_t\beta_s-\alpha_s\beta_t\neq 0.
$$

Then

$$
x_0=\frac{\beta_s x_t-\beta_t x_s}{\Delta_{t,s}},
\qquad
x_1=\frac{-\alpha_s x_t+\alpha_t x_s}{\Delta_{t,s}}.
$$

So for any deterministic linear-in-endpoints scheduler, the delayed pair
\((x_t,x_{t-\tau})\) identifies \((x_0,x_1)\) whenever the two timepoints are
nondegenerate.

The velocity target is then determined as well:

$$
\dot{x}_t=\dot{\alpha}_t x_0+\dot{\beta}_t x_1.
$$

Substituting the endpoint recovery formulas gives

$$
u_t(x,y)
=
\frac{(\dot{\alpha}_t\beta_s-\dot{\beta}_t\alpha_s)x
+(\alpha_t\dot{\beta}_t-\beta_t\dot{\alpha}_t)y}
{\Delta_{t,s}}.
$$

This is the curve-extension argument: the delayed state is not merely additional
local information. In two-endpoint interpolation, it is enough to identify the
whole endpoint pair and therefore the whole constructed path.

## Delay-FM loss from the derivation

The corresponding delay-FM objective has the form

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}
\left[
\left\|
v_\theta(t,x_t,x_{t-\tau})
-
u_t(x_t,x_{t-\tau})
\right\|^2
\right].
$$

Using the substituted target,

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}
\left[
\left\|
v_\theta(t,x_t,x_{t-\tau})
-
\frac{(\dot{\alpha}_t\beta_s-\dot{\beta}_t\alpha_s)x_t
+(\alpha_t\dot{\beta}_t-\beta_t\dot{\alpha}_t)x_{t-\tau}}
{\alpha_t\beta_s-\alpha_s\beta_t}
\right\|^2
\right].
$$

For the linear scheduler used in the simple algorithm,

$$
x_t=(1-t)x_0+t x_1,
$$

the target is explicitly

$$
x_1-x_0.
$$

For \(t\geq \tau\),

$$
x_t-x_{t-\tau}=\tau(x_1-x_0),
$$

so

$$
x_1-x_0=\frac{x_t-x_{t-\tau}}{\tau}.
$$

The loss becomes

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}
\left[
\left\|
v_\theta(t,x_t,x_{t-\tau})
-
\frac{x_t-x_{t-\tau}}{\tau}
\right\|^2
\right].
$$

For \(t<\tau\), the constant initial function gives

$$
x_{t-\tau}=x_0,
$$

so

$$
x_1-x_0=\frac{x_t-x_0}{t}=\frac{x_t-x_{t-\tau}}{t}.
$$

Thus in the linear case, the model target is a finite-difference direction from
the delayed point to the current point. This supports the interpretation that
delay FM gives the network enough information to recover the path direction
algebraically.

## Useful scheduler simplifications

For time-dilated straight paths,

$$
\alpha_t=1-\rho_t,\qquad \beta_t=\rho_t,
$$

we get

$$
u_t(x,y)=\frac{\dot{\rho}_t}{\rho_t-\rho_s}(x-y).
$$

For the special case \(\rho_t=t\),

$$
u_t(x,y)=\frac{x_t-x_{t-\tau}}{\tau}.
$$

For early times \(t<\tau\), with constant history \(x_{t-\tau}=x_0\),

$$
u_t(x,y)=\frac{\dot{\rho}_t}{\rho_t}(x-y),
$$

and for \(\rho_t=t\),

$$
u_t(x,y)=\frac{x_t-x_0}{t}.
$$

For cosine or VP-style paths,

$$
\alpha_t=\cos\phi_t,\qquad \beta_t=\sin\phi_t,
$$

the target becomes a simple linear combination of \(x_t\) and \(x_{t-\tau}\),
but not pure chord following. The broader claim is therefore not that every
scheduler reduces to the same chord. The weaker and more robust claim is that
the delayed pair identifies the endpoints for deterministic two-endpoint paths.

For VE-style additive-noise paths,

$$
x_t=\sigma_t x_0+x_1,
$$

we get

$$
u_t(x,y)=\frac{\dot{\sigma}_t}{\sigma_t-\sigma_s}(x-y).
$$

If \(\sigma_t=e^{-\lambda t}\), then

$$
u_t(x,y)=\frac{\lambda}{e^{\lambda\tau}-1}(x-y).
$$

For many straight/noise schedules, the target collapses to a scalar multiple of
the delayed chord. For cosine/VP rotation-like schedules, it remains a simple
linear expression in \(x_t\) and \(x_{t-\tau}\).

## Loss-gradient interpretation

Standard FM trains a model \(v_\theta(t,x_t)\) with

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
(v_\theta(t,x_t)-u_t)^\top
\nabla_\theta v_\theta(t,x_t)
\right].
$$

The optimal predictor at a point is the conditional mean:

$$
v^*(t,x)=\mathbb{E}[u_t\mid x_t=x].
$$

At a crossing or high-overlap region, FM averages over all pair velocities that
pass through the same \(x\) at the same \(t\). This is the standard marginal
field.

Delay FM trains

$$
\mathcal{L}_{\mathrm{DFM}}(\theta)
=
\mathbb{E}\left[\|v_\theta(t,x_t,x_{t-\tau})-u_t\|^2\right],
$$

with gradient

$$
\nabla_\theta \mathcal{L}_{\mathrm{DFM}}
=
2\mathbb{E}
\left[
(v_\theta(t,x_t,x_{t-\tau})-u_t)^\top
\nabla_\theta v_\theta(t,x_t,x_{t-\tau})
\right].
$$

Its optimal predictor is

$$
v^*(t,x,y)=\mathbb{E}[u_t\mid x_t=x,\ x_{t-\tau}=y].
$$

For deterministic two-endpoint interpolants, the conditioning event identifies
the endpoints, so the conditional variance is zero except for degeneracies.
Therefore delay FM does not average over all velocities crossing at \(x_t\). It
regresses to the velocity of the selected endpoint pair.

## Endpoint from the first prediction

In the linear scheduler with unit interval and constant initial history,

$$
v^*(t,x_t,x_{t-\tau})=x_1-x_0.
$$

At the first useful model call from the initial state, write

$$
\widehat{w}=v_\theta(0,x_0,x_0).
$$

For a fitted model,

$$
\widehat{w}\approx x_1-x_0,
$$

so the endpoint estimate is simply

$$
\widehat{x}_1=x_0+\widehat{w}.
$$

If one starts with a small step \(h\),

$$
x_h=x_0+h\widehat{w}.
$$

The fitted delay target then keeps returning the same velocity along the implied
straight path:

$$
v_\theta(t,x_0+t\widehat{w},x_0+(t-\tau)\widehat{w})
\approx \widehat{w}
\qquad (t\geq\tau),
$$

and, during the initial-history window,

$$
v_\theta(t,x_0+t\widehat{w},x_0)
\approx \widehat{w}
\qquad (0<t<\tau).
$$

Therefore, in the ideal fitted straight-path setting, all later forward passes
are redundant for the endpoint. They only re-integrate the path implied by the
first predicted displacement.

## Deprecated initial thoughts, retained only as intuition

The older note described standard FM as learning a velocity field and delay FM
as learning "lines." The reformulated argument should avoid relying on the word
"line" too literally, because non-straight schedulers can still be
linear-in-endpoints while having rotation/scaling terms. The useful intuition is
that delay FM learns curve extension from a delayed pair.

The older note also speculated that delay FM may perform poorly when translating
a ball-shaped distribution into a donut-shaped distribution, because small
changes in the revealed path direction may need to encode large changes in the
target's radial component. This is a useful research intuition, but it is not
needed for the main article unless a later empirical section is added.

