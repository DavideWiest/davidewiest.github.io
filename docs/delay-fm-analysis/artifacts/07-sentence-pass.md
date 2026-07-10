---
title: "Sentence audit for delay FM rewrite"
date: 2026-07-10
author: codex
status: temporary-writing-workflow
---

# Sentence audit for final rewrite

This audit records the purpose of each accepted prose sentence in the final
post. Equations are checked in the derivation artifact.

## Abstract

1. "Delay Flow Matching..." defines DFM by its conditioning variables rather
   than by the unexplained phrase "delayed state."
2. "Ordinary flow matching..." states the comparator before the modification.
3. "DFM trains..." introduces \(x_{t-\tau}\) as an earlier point on the same
   constructed trajectory.
4. "In a genuine..." separates the DDE reading from the ordinary FM setting.
5. "In ordinary..." defines the setting analyzed in the post.
6. "For common..." states the endpoint-identification claim.
7. "The DFM objective..." states the consequence for the objective.
8. "It learns..." contrasts selected-coupling target vectors with the marginal
   vector field.
9. "This note gives..." previews the proof obligations.

## Introduction

10. "The standard..." gives the reader the setup before notation.
11. "We draw..." explains how endpoint pairs enter training.
12. "In this note..." defines "endpoint pair" explicitly.
13. "The first endpoint..." defines \(x_0\).
14. "The second endpoint..." defines \(x_1\).
15. "The coupling..." defines the article's central object.
16. "The claim is narrow." prevents overreading.
17. "In the ordinary..." states the scoped claim.
18. "Once this happens..." states why the coupling becomes central.

## Flow matching setup

19. "Ordinary flow matching..." motivates the path equation.
20. "The vector-field..." defines the target \(u_t\).
21. "FM trains..." introduces the objective.
22. "The population..." gives the squared-loss minimizer.
23. "This is..." names the marginal vector field only after the formula.
24. "If different..." explains the conditional mean behavior.
25. "DFM changes..." introduces the modification.
26. "It trains..." gives the DFM input form.
27. "Here..." defines \(x_{t-\tau}\) again locally.
28. "This earlier point..." states why the modification matters.

## Endpoint recovery

29. "Set \(s=t-\tau\)." fixes notation.
30. "The current..." introduces the matrix equation.
31. "This equation..." explains coordinatewise inversion.
32. "When..." states the determinant condition.
33. "the endpoint..." introduces the recovered endpoints.
34. "The model..." states the main algebraic consequence.
35. "The calculation..." prevents the straight-path underclaim.
36. "It only..." states the actual assumptions.
37. "The target..." explains why endpoint recovery affects the objective.
38. "Substituting..." introduces the target formula.
39. "For the straight..." marks the straight case as only a special case.
40. "For cosine..." marks nonlinear schedules as covered by the general claim.
41. "The endpoint-recovery..." restates the general point.

## Delay FM's objective

42. "DFM minimizes..." introduces the DFM objective.
43. "Its gradient..." gives the gradient object.
44. "The corresponding..." gives the population minimizer.
45. "Compare..." places the FM minimizer beside it.
46. "The difference..." identifies the conditioning change.
47. "Ordinary FM..." explains the averaging object.
48. "DFM conditions..." explains the finer conditioning object.
49. "In the deterministic..." connects endpoint recovery to the objective.
50. "The objective..." states that the sampled coupling is what is preserved.
51. "This is why..." connects to source-conditioned FM and ABM.
52. "When the model..." states the source-conditioned version precisely.
53. "When the model..." states the endpoint-recovered version precisely.
54. "Both cases..." gives the conceptual comparison without overclaiming.

## Endpoint after one model evaluation

55. "The same endpoint..." motivates the sampling consequence.
56. "Suppose..." states the endpoint-determined condition.
57. "After..." states the one-evaluation consequence with the fitted-model
   condition.
58. "For the..." introduces the concrete readout.
59. "The current..." introduces the state-target system.
60. "If..." states the readout determinant condition.
61. "then..." gives the endpoint readout.
62. "For common..." states the \(t=0\) simplification.
63. "Then..." gives the simplified formula.
64. "The straight..." gives the familiar special case.
65. "This is..." explicitly rejects the straight-path-only reading.
66. "The sufficient..." states the general condition.
67. "Once..." states why later target vectors are analytic.
68. "For the..." gives the linear-in-endpoints formula.
69. "Further..." scopes finite-capacity and numerical exceptions.
70. "They do..." states the endpoint-information claim.

## Coupling choice

71. "The practical..." states the implication.
72. "If the..." describes product coupling.
73. "Such a..." avoids claiming that product-coupled DFM cannot work.
74. "The extra..." states the interpretation.
75. "DFM is..." gives the recommendation.
76. "The pairing..." gives examples.
77. "In those..." states why the extra input helps.

## Delayed dynamical systems

78. "The analysis..." sets the boundary.
79. "In a DDE..." introduces the true DDE equation.
80. "the earlier..." explains the role of \(x(t-\tau)\).
81. "It is..." distinguishes this from endpoint coding.
82. "The path..." states why endpoint-interpolation analysis does not apply.
83. "Snapshot-to-snapshot..." names the valid separate setting.
84. "DFM can..." states the positive scoped use case.
85. "The remaining..." states the modeling caveat.
86. "If those..." explains what DFM learns under constructed paths.

## Final style checks

- Removed the heading "What the loss is fitting."
- Replaced it with "Delay FM's objective."
- Removed "Where the argument stops."
- Removed "curve-extension loss" and the standalone "This is the
  curve-extension argument."
- Replaced the straight-path endpoint statement with the scheduler-general
  endpoint-readout condition.
- Avoided body prose sentences that use a colon as the main pivot.

