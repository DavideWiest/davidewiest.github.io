---
title: "Content bullets for delay FM rewrite"
date: 2026-07-10
author: codex
status: temporary-writing-workflow
---

# Content bullets for rewrite

## Terms that must be defined before use

- Delay Flow Matching uses a vector field of the form
  \(v_\theta(t,x_t,x_{t-\tau})\).
- \(x_t\) is the current point on the constructed training trajectory.
- \(x_{t-\tau}\) is an earlier point on that same constructed trajectory.
- The endpoint pair means the ordered pair \((x_0,x_1)\), where \(x_0\)
  comes from the source or noise distribution and \(x_1\) comes from the target
  or data distribution under the chosen coupling.
- The ordinary FM marginal vector field means
  \(v^*(t,x)=\mathbb{E}[u_t\mid x_t=x]\).

## Correct main claim

- In the standard two-endpoint distribution-transport setting, DFM gives the
  model enough information to identify the endpoint pair for many deterministic
  interpolants.
- Once \((x_t,x_{t-\tau})\) identifies \((x_0,x_1)\), the DFM objective asks the
  model to predict the target vector for the selected endpoint pair.
- This is not the same statistical object as ordinary FM, which averages over
  all endpoint pairs compatible with \(x_t\).
- The closest conceptual relatives are source-conditioned FM and Augmented
  Bridge Matching, because all three preserve endpoint-pair information.

## Mathematical route

- Start from \(x_r=\alpha_r x_0+\beta_r x_1\).
- Set \(s=t-\tau\).
- Write the current and earlier trajectory points as a \(2\times2\) system.
- Invert it when
  \(\Delta_{t,s}=\alpha_t\beta_s-\alpha_s\beta_t\neq0\).
- State explicitly that this step does not assume a straight path in time.
- Compare FM and DFM gradients.
- Derive the population minimizers from squared loss.

## Correct endpoint consequence

- The consequence is not restricted to straight paths.
- Sufficient condition: the target vector is determined by the endpoint pair,
  and the first informative model output gives an invertible readout of
  \(x_1\) given \(x_0\) or \(x_t\).
- For linear-in-endpoints schedules, one can recover \(x_1\) from one fitted
  model output and the current point:

$$
\widehat{x}_1
=
\frac{-\dot{\alpha}_{t_*}x_{t_*}+\alpha_{t_*}\widehat{u}_{t_*}}
{\alpha_{t_*}\dot{\beta}_{t_*}-\dot{\alpha}_{t_*}\beta_{t_*}}.
$$

- For the straight scheduler at \(t_*=0\), this reduces to
  \(\widehat{x}_1=x_0+\widehat{u}_0\).
- After \(\widehat{x}_1\) is known, later endpoint-determined target vectors can
  be computed from the schedule without more neural network evaluations.

## Style constraints from the correction

- Avoid undefined phrases such as "delayed state."
- Avoid vague terms such as "velocity regression."
- Avoid labels such as "curve-extension loss" unless they are defined and useful.
- Avoid paper-inappropriate headings.
- Avoid colon-pivot prose sentences in the post body.
- Make the mathematical sufficient conditions explicit before giving special
  cases.

