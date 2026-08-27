# Blog refresh and publication

## Objective

Refresh and publish the personal website's research posts.

## Requirements

- Supersede the old chemokinesis post with a maximally short, theoretically precise account based on `chemokinetic_optimization_short.pdf` in the writable vault.
- Retain the main chain: effective dimension, oracle Ray-CK, causal information barrier, projected oracle, and operational optimizer.
- Put derivations/proofs after the main text; omit the no-hedging result.
- Report only the central MNIST evidence: endpoint NLL 2.05 versus 1.97, about 30 oracle-Ray evaluations per GD step, and about 200 for the operational optimizer.
- Remove the recursive union-of-manifolds and underrated probability-theorems posts.
- Turn `workspace/jacobian-maxent-blog/maxent-objective.md` into a short website post only if its forward-Jacobian/minimum-risk argument is valid.
- Frame the Jacobian post from gradient-based optimization; distinguish the new Jacobian interpretation from established equivariance/whitening results; connect the derivation rather than merely juxtaposing it with the literature; give SSL-plus-linear-head and greedy/layerwise learning one paragraph each; remove the recap opener and redundant limitations paragraph.
- Tighten every other existing post by deleting 25--40% where possible, removing recapitulation, hedging, empirical-diary material, and dispensable examples while preserving evidence and qualifications.
- Build and review the generated site, commit under the user's configured identity, and push the website repository.

## Acceptance checks

- The two retired posts have no publication source or archived page source.
- Every retained LaTeX source renders without errors.
- Internal/public links and site editorial checks pass.
- Changed articles preserve factual claims, citations, numerical results, figures, and necessary scope.
- The pushed `master` branch contains the complete refresh.
