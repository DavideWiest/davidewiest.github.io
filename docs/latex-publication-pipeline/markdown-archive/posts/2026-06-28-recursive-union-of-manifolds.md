---
title: "Recursive Union-of-Manifolds Diagnostics Beyond Images"
date: 2026-06-28
permalink: /posts/2026/06/recursive-union-of-manifolds/
tags:
  - machine-learning
  - geometry
  - intrinsic-dimension
  - natural-language-processing
  - experiments
---

## Abstract

The union-of-manifolds hypothesis states that a data distribution decomposes into several lower-dimensional geometric pieces. Brown et al. verified this hypothesis for image data by estimating intrinsic dimension inside class partitions and by testing disconnected generative structure. This note extends the intrinsic-dimension half of their procedure to hierarchical, less class-centric data. The experiment reuses the official UoMH intrinsic-dimension estimator, pins the literature code, and evaluates chess positions, finance return windows, 20 Newsgroups text in two embedding spaces, and ImageNet-R rendition styles. The central result is precise: recursive estimator-level geometry appears in natural-language topic hierarchies, chess confirms two semantic levels, finance confirms one asset-allocation level, and ImageNet-R style labels fail the node diagnostic under the screening protocol. Therefore the recursive union-of-manifolds diagnostic is a real cross-domain phenomenon in representation space, and its evidence is strongest in text and structured symbolic state spaces.

## 1. The Object

Consider a dataset represented as vectors \(x_i \in \mathbb{R}^d\). A flat union-of-manifolds model asserts that the support is organized as

$$
\mathcal{X} = \bigcup_{j=1}^{m} \mathcal{M}_j,
$$

where each \(\mathcal{M}_j\) has its own intrinsic dimension. Consequently, if a proposed partition tracks the actual pieces, then the estimated intrinsic dimensions of the parts vary more than equally sized random parts. Brown et al. used this principle for image classes in [Verifying the Union of Manifolds Hypothesis for Image Data](https://arxiv.org/abs/2207.02862), and their public code exposes the estimator needed for the test through [`layer6ai-labs/UoMH`](https://github.com/layer6ai-labs/UoMH).

The recursive version applies the same statement inside each piece. Formally, for a parent node \(P\), the hypothesis is

$$
P = \bigcup_{k=1}^{r(P)} P_k,
$$

and the children \(P_k\) exhibit the same two signatures as the root pieces. First, their intrinsic-dimension estimates have excess dispersion relative to matched random children inside \(P\). Second, nearest neighbors inside \(P\) preserve child identity more often than a random-label baseline. Hence recursion is not a metaphor in this experiment. It is a repeated node-level test.

This formulation also fixes the scope of the claim. The experiment establishes recursive estimator-level geometry. A disconnected-support theorem requires the generative disconnectedness test from the original paper or an equivalent topological test. Therefore every conclusion below concerns intrinsic dimension and local neighbor structure in the chosen representation spaces.

## 2. Protocol

Each dataset is converted into a feature matrix and a hierarchy. The hierarchy gives root-to-child partitions, child-to-grandchild partitions, and, when sample size permits, grandchild-to-great-grandchild partitions. At every internal node, the experiment estimates intrinsic dimension for each observed child by using the pinned UoMH Levina-Bickel / MacKay-Ghahramani estimator. It then constructs random child partitions with the same child sizes inside the same parent node and repeats the same estimator.

The main effect statistic is

$$
\rho(P) =
\frac{\operatorname{std}(\widehat{\mathrm{ID}}(P_1),\ldots,\widehat{\mathrm{ID}}(P_r))}
{\operatorname{median}_{b}\operatorname{std}(\widehat{\mathrm{ID}}(R_{b,1}),\ldots,\widehat{\mathrm{ID}}(R_{b,r}))}.
$$

Here \(R_{b,k}\) are matched random children. In addition, the parent node is tested for nearest-neighbor child purity, and this gives the locality lift

$$
\lambda(P) =
\frac{\Pr[\text{nearest neighbor has same child label}]}
{\sum_k \Pr[P_k]^2}.
$$

Accordingly, a node has a geometric effect when \(\rho(P) > 1\) and \(\lambda(P) > 1\). Moreover, in the confirmatory run, a node is marked as confirmed when this effect also has finite randomization \(p \leq 0.05\) under 19 matched random controls. Because the p-value is computed as \((1 + \#\{\rho_{\mathrm{random}} \geq \rho_{\mathrm{observed}}\})/(1 + 19)\), the value \(0.05\) means that no random control exceeded the observed node.

The primary hierarchies are:

| Dataset | Hierarchy |
| --- | --- |
| Chess positions | game phase by ply, then material bucket, then local feature clusters |
| Finance ETF windows | asset group, then ticker, then calendar regime |
| 20 Newsgroups TF-IDF/SVD | coarse topic family, then fine newsgroup, then local feature clusters |
| 20 Newsgroups SBERT | the same topic hierarchy in Sentence-BERT embedding space |
| ImageNet-R screening | rendition style, then object synset when sample size permits |

Thus the protocol tests labels, metadata, and induced local clusters with the same estimator and the same randomization logic.

## 3. Results

The confirmatory run used 6,000 samples per dataset where available, child caps of 384, parent caps of 3,000, \(k = 2,\ldots,15\), target \(k = 10\), and 19 matched random controls per node. All dataset-level runs completed. All target-k node and child estimates were finite. All stored estimator curves were strict JSON after non-finite intermediate curve values were serialized as null.

The summary table is:

| Dataset | Valid nodes | Max depth | Effect nodes | Confirmed nodes | Main fact |
| --- | ---: | ---: | ---: | ---: | --- |
| 20 Newsgroups SBERT | 13 | 3 | 12 | 3 | recursive effect through depth 3; confirmed root, one fine-topic node, and one local depth-3 node |
| 20 Newsgroups TF-IDF/SVD | 10 | 3 | 8 | 4 | confirmed fine-topic recursion and one confirmed depth-3 local node |
| Chess positions | 7 | 3 | 3 | 3 | confirmed game-phase and material levels; depth-3 local clusters fail |
| Finance ETF windows | 5 | 2 | 1 | 1 | confirmed asset-group split; ticker recursion fails locality |

For chess, the root game-phase split has \(\rho = 4.17\), locality lift \(2.46\), and \(p = 0.05\). Then, within the middle-game and end-game phase nodes, material buckets have median \(\rho = 5.42\), median locality lift \(1.39\), and median \(p = 0.05\). Consequently, chess has a confirmed two-level recursive structure. Then, at depth 3, local KMeans clusters have median \(\rho = 0.52\) and median locality lift \(1.83\). Therefore the local clusters are spatially coherent without producing excess intrinsic-dimension dispersion.

For finance, the asset-group split has \(\rho = 4.81\), locality lift \(1.07\), and \(p = 0.05\). Then ticker partitions inside asset groups have median \(\rho = 1.04\) and median locality lift \(0.91\). Consequently, the finance representation contains a top-level asset-group geometry, and ticker identity is not a recursive manifold diagnostic under this protocol.

For TF-IDF/SVD text, the root topic-family split has locality lift \(3.26\) and \(\rho = 0.88\), so the root is local without excess ID dispersion. Then fine newsgroups inside topic families have effect fraction \(1.00\), confirmed fraction \(0.75\), median \(\rho = 1.67\), and median locality lift \(2.57\). Finally, local depth-3 clusters have effect fraction \(0.80\), confirmed fraction \(0.20\), median \(\rho = 1.36\), and median locality lift \(1.52\). Hence TF-IDF/SVD text carries the recursive diagnostic most clearly below the coarse family level.

For SBERT text, the root topic-family split has \(\rho = 2.20\), locality lift \(4.07\), and \(p = 0.05\). Then fine-topic nodes have effect fraction \(1.00\), confirmed fraction \(0.25\), median \(\rho = 1.34\), and median locality lift \(3.10\). Finally, depth-3 local clusters have effect fraction \(0.875\), confirmed fraction \(0.125\), median \(\rho = 1.26\), and median locality lift \(1.60\). Therefore the transformer representation preserves topic hierarchy at the root, at the fine-topic level, and inside at least one local subtopic node.

The ImageNet-R screening run starts from rendition style. The root style node has \(\rho = 0.94\), locality lift \(1.18\), and \(p = 0.83\) under five controls. Therefore ImageNet-R style labels do not pass the two-part node diagnostic in this raw-pixel, style-first setup.

## 4. Interpretation

The recursive result is strongest when the hierarchy is aligned with functional structure. In chess, game phase and material describe the legal state space directly. Accordingly, the first two levels have large ID heterogeneity and strong locality. In text, topic family and fine topic organize documents by semantic and lexical mechanisms. Accordingly, both TF-IDF/SVD and SBERT expose recursive geometry, and the agreement across representations makes the language result the cleanest extension beyond images.

The result also separates mixture structure from recursive manifold structure. Finance has a real asset-group split, because broad asset classes have distinct return-window geometry. Then ticker identity does not preserve nearest-neighbor structure inside those groups. Consequently, finance behaves as a shallow mixture in this representation.

The result also separates locality from intrinsic-dimension heterogeneity. Chess depth-3 clusters have strong locality and low heterogeneity ratio. Therefore local clustering alone is insufficient. A recursive manifold diagnostic requires both local child identity and excess dispersion of child intrinsic dimensions.

## 5. Consequences

The experiment gives a practical recipe for testing recursive manifold structure in representation spaces. First, define a hierarchy before estimation. Next, run the same intrinsic-dimension estimator on observed and matched random child partitions. Then require both excess ID dispersion and local neighbor purity. Finally, separate effect-size nodes from finite-randomization-confirmed nodes.

This recipe turns the union-of-manifolds idea into a reusable diagnostic for domains that are not naturally image-class datasets. It also identifies where the hypothesis stops under a given representation. The method confirms chess phase/material recursion, confirms multiple natural-language recursive nodes across two text embeddings, confirms only the top finance split, and rejects ImageNet-R style labels under the screening setup.

Accordingly, the recursive union-of-manifolds hypothesis is not a universal label story. It is a geometric claim about how a representation decomposes under a specified hierarchy. Under that definition, the evidence is decisive: natural language and symbolic game states contain recursive union-of-manifolds diagnostics; finance contains a shallow version; ImageNet-R style labels do not pass this version of the test.

## References And Artifacts

- Brown et al., [Verifying the Union of Manifolds Hypothesis for Image Data](https://arxiv.org/abs/2207.02862)
- Official UoMH code, [`layer6ai-labs/UoMH`](https://github.com/layer6ai-labs/UoMH)
- Wang and Wang, [CW Complex Hypothesis for Image Data](https://proceedings.mlr.press/v235/wang24bs.html)
- Schulte and Ruegamer, [Rethinking Intrinsic Dimension Estimation in Neural Representations](https://arxiv.org/abs/2604.20276)
- Reimers and Gurevych, [Sentence-BERT](https://arxiv.org/abs/1908.10084)
- Project repository, [`Axym-Labs/uomh-beyond-classification`](https://github.com/Axym-Labs/uomh-beyond-classification)
- Confirmatory artifacts, [`confirmatory-r19-20260628`](https://github.com/Axym-Labs/uomh-beyond-classification/tree/main/docs/recursive-uomh-protocol/artifacts/confirmatory-r19-20260628)
- Screening artifacts, [`final-run-20260628-recursive`](https://github.com/Axym-Labs/uomh-beyond-classification/tree/main/docs/recursive-uomh-protocol/artifacts/final-run-20260628-recursive)
