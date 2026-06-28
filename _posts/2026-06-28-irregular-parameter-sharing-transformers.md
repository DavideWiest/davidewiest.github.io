---
title: "Irregular parameter sharing in Transformers"
date: 2026-06-28
permalink: /posts/2026/06/irregular-parameter-sharing-transformers/
tags:
  - machine-learning
  - language-models
  - transformers
  - parameter-sharing
---

Depth in a Transformer is a sequence of learned operators. In an ordinary depth-$L$ decoder, each layer has its own block $B_l$, and the residual stream evolves as

$$
h_{l+1}=B_l(h_l), \qquad l=1,\ldots,L.
$$

Parameter sharing changes this object. Instead of learning $L$ separate blocks, we learn a smaller bank of $K$ blocks and choose a schedule

$$
s=(s_1,\ldots,s_L), \qquad s_l \in \{1,\ldots,K\},
$$

so that

$$
h_{l+1}=B_{s_l}(h_l).
$$

Once sharing is written this way, the architecture has two degrees of freedom. The first is the number of learned blocks $K$. The second is the depth schedule $s$. Therefore, a shared Transformer is not fully specified by the amount of sharing alone. It is specified by where each reused operator acts.

The baseline schedules here are regular. One-block sharing uses the same operator at every depth. Cyclic sharing uses a small bank periodically, for example

$$
[0,1,2,0,1,2,0,1].
$$

These schedules are simple, deterministic, and easy to implement. They also impose a strong algebraic constraint on depth: positions separated by the period receive the same update. Irregular sharing keeps the same block bank and the same parameter count, then changes only the schedule. For example, with four blocks and twelve depth positions, one irregular schedule is

$$
[0,0,1,1,2,0,3,2,1,3,3,0].
$$

The central empirical question is therefore precise: at fixed shared-block count, does the schedule itself change language-model validation loss?

## method

I tested this with decoder-only causal Transformers. Each model used learned token embeddings, learned positional embeddings, pre-norm self-attention blocks, GELU MLPs, tied output embeddings, AdamW, sequence length 256, and the GPT-2 tokenizer for the token-level experiment. The practical reference model was the ordinary unshared Transformer with the same depth and width. The simple same-parameter baseline was cyclic sharing, since it uses the same number of shared blocks as the irregular models.

For the shared-block comparison, cyclic and irregular models used the same number of learned blocks and the same non-embedding parameter count. They also used matched initialization for the shared blocks. Thus the comparison changes the depth schedule, not the size of the model.

The main token-level experiment used local OpenWebText shards, 19M training tokens, 1M validation tokens, depth 12, width 384, 6 attention heads, batch size 32, and 3000 training steps. I ran it with seeds 0, 1, and 2. I also ran a short random schedule search for each seed: each candidate schedule trained for 600 steps, the best candidate schedule was selected, and then that schedule was retrained from scratch for the full 3000-step comparison.

## token-level result

The fixed schedules were:

| Model | Schedule | Learned blocks | Non-embedding parameters |
|---|---|---:|---:|
| One-block sharing | `[0,0,0,0,0,0,0,0,0,0,0,0]` | 1 | 1.772M |
| Cyclic sharing | `[0,1,2,3,0,1,2,3,0,1,2,3]` | 4 | 7.085M |
| Hand irregular sharing | `[0,0,1,1,2,0,3,2,1,3,3,0]` | 4 | 7.085M |
| Unshared Transformer | `[0,1,2,3,4,5,6,7,8,9,10,11]` | 12 | 21.253M |

The searched irregular schedule was selected separately for each seed from eight short candidate runs. The measured validation losses were:

| Seed | Regular CE | Cyclic CE | Hand irregular CE | Searched irregular CE | Unshared CE | Hand gain | Searched gain |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 6.6859 | 6.5857 | 6.5456 | 6.5667 | 6.4664 | 0.0401 | 0.0190 |
| 1 | 6.6445 | 6.5529 | 6.5192 | 6.5059 | 6.4762 | 0.0337 | 0.0470 |
| 2 | 6.6985 | 6.5994 | 6.5653 | 6.5162 | 6.4734 | 0.0341 | 0.0832 |
| Mean | 6.6763 | 6.5793 | 6.5433 | 6.5296 | 6.4720 | 0.0360 | 0.0497 |
| Sample sd | 0.0283 | 0.0239 | 0.0231 | 0.0325 | 0.0051 | 0.0036 | 0.0322 |

For seed 0, the detailed table is:

| Model | Schedule | Learned blocks | Non-embedding parameters | Validation CE |
|---|---|---:|---:|---:|
| One-block sharing | `[0,0,0,0,0,0,0,0,0,0,0,0]` | 1 | 1.772M | 6.6859 |
| Cyclic sharing | `[0,1,2,3,0,1,2,3,0,1,2,3]` | 4 | 7.085M | 6.5857 |
| Hand irregular sharing | `[0,0,1,1,2,0,3,2,1,3,3,0]` | 4 | 7.085M | 6.5456 |
| Searched irregular sharing | `[3,2,1,3,3,3,3,0,2,0,3,3]` | 4 | 7.085M | 6.5667 |
| Unshared Transformer | `[0,1,2,3,4,5,6,7,8,9,10,11]` | 12 | 21.253M | 6.4664 |

The equal-parameter comparison is cyclic sharing, hand irregular sharing, and searched irregular sharing. All three use four learned blocks and 7.085M non-embedding parameters. The fixed hand irregular schedule improves validation cross-entropy over cyclic sharing in all three seeds, with mean gain 0.0360. The searched irregular schedule also improves over cyclic sharing in all three seeds, with mean gain 0.0497. Since the shared models have the same non-embedding parameter count and matched shared-block initialization, this improvement is produced by the schedule.

The unshared Transformer has the lowest mean validation loss. It is the practical reference: when the model is allowed to spend 21.253M non-embedding parameters instead of 7.085M, it learns a better language model. The relevant comparison for the sharing mechanism is therefore the fixed-$K$ comparison between cyclic and irregular schedules.

## smaller OpenWebText check

A second token-level run used the same GPT-2 tokenizer and local OpenWebText source at smaller scale: 4.5M training tokens, 0.5M validation tokens, depth 8, width 256, 8 attention heads, and 1200 training steps.

| Model | Schedule | Learned blocks | Non-embedding parameters | Validation CE |
|---|---|---:|---:|---:|
| One-block sharing | `[0,0,0,0,0,0,0,0]` | 1 | 0.788M | 7.3475 |
| Cyclic sharing | `[0,1,2,0,1,2,0,1]` | 3 | 2.363M | 7.2871 |
| Hand irregular sharing | `[0,0,1,1,2,0,0,2]` | 3 | 2.363M | 7.2723 |
| Searched irregular sharing | `[0,0,0,2,1,0,1,2]` | 3 | 2.363M | 7.2700 |
| Unshared Transformer | `[0,1,2,3,4,5,6,7]` | 8 | 6.300M | 7.2011 |

This run has the same structure as the main run. At equal shared-block count, hand irregular sharing improves over cyclic sharing by 0.0148 CE, and searched irregular sharing improves over cyclic sharing by 0.0171 CE.

## replication on character language modeling

The same schedule question was tested on a character-level Transformer language model trained on local Lichess PGN data. This experiment is smaller than OpenWebText and gives a seed-level check because it holds the same schedule comparison fixed.

| Seed | Cyclic CE | Hand irregular CE | Searched irregular CE | Unshared CE |
|---:|---:|---:|---:|---:|
| 0 | 0.6211 | 0.6200 | 0.6047 | not run |
| 1 | 0.6283 | 0.6257 | 0.6064 | not run |
| 2 | 0.5788 | 0.5813 | 0.5666 | 0.5612 |

The searched irregular schedule beats cyclic sharing in all three seeds. The hand schedule beats cyclic sharing in two seeds and loses in one seed. Therefore, irregularity itself is not enough; the schedule has to be selected. This is exactly what the schedule formulation predicts. Once $s$ is an architectural object, choosing $s$ is part of model design.

## interpretation

A cyclic schedule assumes that depth is periodic. This assumption is convenient because it converts depth into repeated applications of a small operator bank. It also makes the first, fourth, and seventh transformations share weights in an eight-layer three-block model. Nothing in the residual stream requires this periodic equivalence.

An irregular schedule removes that equivalence while keeping the same learned blocks. In the hand schedule above, block 0 appears twice at the start, block 3 enters only after six transformations, and the final positions reuse blocks 1, 3, 3, and 0. In this view, a shared Transformer resembles an unrolled dynamical system with a small set of operators and a discrete control sequence. The number of operators controls parameter count. The control sequence controls how those operators are composed.

This matters for language models because non-embedding Transformer blocks are the expensive part that grows with depth and width. At LLM scale, sharing a block bank is a direct parameter-compression axis. A regular schedule spends that axis in the most constrained way. An irregular schedule keeps the compression and gives the depth computation more compositions.

The experiment establishes the concrete schedule effect: with the same learned blocks, the non-periodic schedules achieve lower validation loss than the cyclic schedule. The unshared model remains the practical reference point for maximum quality at this width and depth. Accordingly, schedule learning belongs inside the parameter-sharing problem: choose the block bank, choose the depth schedule, and then scale the comparison to larger shared-block banks, deeper Transformers, and longer training.

## artifact

The run writes exact metrics, schedules, and raw histories under:

`/home/davwis/main/exploration/irregular_token_lm/openwebtext_large_seed0/`

`/home/davwis/main/exploration/irregular_token_lm/openwebtext_large_seed1/`

`/home/davwis/main/exploration/irregular_token_lm/openwebtext_large_seed2/`

The corrected experiment report, including failed model-idea tests and the character-LM replication table, is under:

`/home/davwis/main/exploration/docs/corrected_model_ideas/artifacts/corrected_experiment_report.md`
