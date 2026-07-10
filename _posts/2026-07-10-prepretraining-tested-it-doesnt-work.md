---
title: "Prepretraining tested: it doesn't work"
date: 2026-07-10
permalink: /posts/2026/07/prepretraining-tested-it-doesnt-work/
tags:
  - machine-learning
  - language-models
  - pretraining
  - experiments
---

Prepretraining denotes a two-stage training regime: a language-model architecture is first trained on synthetic or abstract data, and only then trained on natural language. This setting is relevant because language-model training is increasingly constrained by data quality, compute allocation, and the finite supply of public human-written text. In that context, scaling-law work established the empirical role of model, data, and compute scale, compute-optimal training sharpened the importance of token budgets, and data-supply analyses motivate methods that improve sample efficiency ([Kaplan et al. 2020](https://arxiv.org/abs/2001.08361), [Hoffmann et al. 2022](https://arxiv.org/abs/2203.15556), [Villalobos et al. 2022](https://arxiv.org/abs/2211.04325)).

The central empirical question is whether synthetic upstream training gives the later natural-text phase a better initialization. The tested mechanisms were NCA-generated sequences, LIME-style induction, deduction, and abduction tasks, simpler copy/set/query tasks, procedural programs, Dyck programs, and synthetic summarization transformations. These correspond to the mechanisms proposed or used by [Lee et al. 2026](https://arxiv.org/abs/2603.10055), [Wu et al. 2021](https://proceedings.mlr.press/v139/wu21c.html), [Wu et al. 2022](https://arxiv.org/abs/2206.10139), [Jiang et al. 2026](https://arxiv.org/abs/2601.21725), and [Krishna et al. 2021](https://aclanthology.org/2021.findings-emnlp.273/), with neural cellular automata also grounded in the construction of [Mordvintsev et al. 2020](https://distill.pub/2020/growing-ca). Across these variants, the transfer claim is stronger than cheap data generation: synthetic data must induce structure that remains useful after the transition to natural text.

This evaluation tests that claim with [`pptrain`](https://github.com/Axym-Labs/pptrain), using the Pythia-410M architecture and tokenizer, a 12,288-token context length, three seeds, public Hugging Face text datasets, and six synthetic task families. To keep the comparison explicit, the baseline is random initialization followed by downstream text training, while the natural-text warmup is treated as a separate method, called NLP prepretraining, rather than as the baseline.

Under this protocol, the results do not support a general synthetic-prepretraining benefit. Synthetic prepretraining improves over random initialization in only one of six task families, and that case is small: Simpler tasks improves final downstream eval loss by 0.16%. At the same time, NLP prepretraining outperforms every synthetic method, and the reasoning and algorithmic probes show no transfer gain.

## Experimental setup

The benchmark was executed with `pptrain replicate`; the completed run corresponds to:

```bash
pptrain replicate \
  --profile paper_proxy_2048 \
  --model-name-or-path EleutherAI/pythia-410m-deduped \
  --context-length 12288 \
  --output-dir internal/runs/paper_proxy_pythia410m_12k_20260703_1552 \
  --resume
```

Although the profile is named `paper_proxy_2048`, the run analyzed here overrides the context length to 12,288 tokens. Because the model is initialized from the Pythia config and tokenizer rather than from the released Pythia weights, the Pythia suite supplies the architectural and tokenizer reference, while the training baseline remains random initialization ([Biderman et al. 2023](https://arxiv.org/abs/2304.01373)).

Each task used three conditions per seed:

1. Random-init baseline: train only on the downstream text slice.
2. Synthetic transfer: train on a synthetic task, transfer the learned weights into the downstream model, then train on the downstream text slice.
3. NLP prepretraining: spend the upstream budget on natural text from the same text family, then continue on the downstream text slice.

The public text data were loaded through Hugging Face Datasets ([Lhoest et al. 2021](https://arxiv.org/abs/2109.02846)). General-text tasks used `HuggingFaceFW/fineweb-edu`, `sample-10BT`, which is part of FineWeb-Edu ([Penedo et al. 2024](https://arxiv.org/abs/2406.17557), [dataset card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)); the math task used `HuggingFaceTB/finemath`, `finemath-4plus` ([dataset card](https://huggingface.co/datasets/HuggingFaceTB/finemath)); and the summarization task used `vblagoje/cc_news` ([dataset card](https://huggingface.co/datasets/vblagoje/cc_news)). In all three cases, the datasets were streamed with separate skip offsets for warmup, train, and eval slices.

The six synthetic task families were NCA, LIME, Simpler tasks, Procedural, Dyck, and Summarization. NCA used the `paper_web_text` preset from the NCA language-modeling mechanism; LIME used the `paper_benchmark_100k` symbolic-reasoning preset; Simpler tasks used the `paper_unary_core_100k` copy/set/query mix; Procedural used the `paper_set_len64` program preset; Dyck used the `paper_k64` bracket-language preset; and Summarization used the `paper_ourtasks_subset_100k` synthetic-document preset. Since the protocol uses public datasets and a shared bounded setup, it is a proxy study rather than an exact reproduction of every original corpus, schedule, or training budget. The scope is therefore to test whether the same synthetic methods improve later NLP training under one shared, public, multi-seed protocol.

<figure>
  <img src="/images/pptrain-replication/claim_matrix.png" alt="Claim matrix for the pptrain proxy run" style="width:100%;">
  <figcaption><strong>Figure 1.</strong> Claim matrix for the six task families. Green cells denote claims supported by the three-seed rule, red cells denote contradicted claims, and grey cells denote inconclusive or unevaluated claims. The matrix shows broad failure against both the random-init baseline and NLP prepretraining.</figcaption>
</figure>

## Results

Taken together, Figure 1 and Table 1 summarize the final outcomes. NCA, LIME, Procedural, Dyck, and Summarization did not beat random initialization, while all six synthetic methods underperformed NLP prepretraining. The auxiliary probes agree with the loss results: reasoning accuracy for NCA and LIME was zero for both scratch and transferred models, and the algorithmic probes for Procedural and Dyck showed no gain.

<figure>
  <img src="/images/pptrain-replication/transfer_gap_vs_scratch.png" alt="Synthetic transfer gap versus random-init baseline" style="width:100%;">
  <figcaption><strong>Figure 2.</strong> Mean downstream eval-loss improvement of synthetic transfer over the random-init baseline. Positive values indicate lower loss than scratch. Only Simpler tasks is positive, and the effect is small.</figcaption>
</figure>

<figure>
  <img src="/images/pptrain-replication/compute_matched_nlp_prepretraining_gap.png" alt="Synthetic transfer gap versus NLP prepretraining" style="width:100%;">
  <figcaption><strong>Figure 3.</strong> Mean downstream eval-loss improvement of synthetic transfer over NLP prepretraining. Positive values indicate that synthetic transfer beat the natural-text warmup. All six values are negative.</figcaption>
</figure>

<p><strong>Table 1.</strong> Main downstream losses and relative gaps. Lower loss and lower perplexity are better. Positive gap values mean synthetic transfer improved over the comparator.</p>

| Task | Synthetic preset | Scratch loss | Synthetic loss | NLP loss | Synthetic vs scratch | Synthetic vs NLP | Scratch ppl | Synthetic ppl | NLP ppl |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NCA | `paper_web_text` | 6.232 | 6.779 | 6.044 | -8.78% | -12.17% | 508.9 | 891.7 | 421.5 |
| LIME | `paper_benchmark_100k` | 5.134 | 6.032 | 4.713 | -17.60% | -27.99% | 170.8 | 419.3 | 111.4 |
| Simpler tasks | `paper_unary_core_100k` | 6.237 | 6.227 | 6.040 | +0.16% | -3.08% | 511.1 | 506.1 | 420.1 |
| Procedural | `paper_set_len64` | 6.236 | 6.540 | 6.042 | -4.87% | -8.24% | 510.8 | 692.4 | 420.8 |
| Dyck | `paper_k64` | 6.242 | 6.583 | 6.050 | -5.46% | -8.79% | 513.8 | 726.5 | 424.3 |
| Summarization | `paper_ourtasks_subset_100k` | 5.828 | 6.623 | 5.559 | -13.66% | -19.14% | 339.6 | 766.1 | 259.7 |

The loss curves show the same ordering over training rather than only at the final step. In most panels, NLP prepretraining ends with the lowest loss, the random-init baseline remains between NLP prepretraining and synthetic transfer, and synthetic transfer starts at higher loss and remains higher.

<figure>
  <img src="/images/pptrain-replication/loss_overlays.png" alt="Downstream loss overlays for scratch, synthetic transfer, and NLP prepretraining" style="width:100%;">
  <figcaption><strong>Figure 4.</strong> Downstream eval-loss curves for random initialization, synthetic transfer, and NLP prepretraining. Solid lines are seed means and bands show one standard deviation. The ordering is visible across training, not only at the final step.</figcaption>
</figure>

<figure>
  <img src="/images/pptrain-replication/effect_summary.png" alt="Effect summary heatmap" style="width:100%;">
  <figcaption><strong>Figure 5.</strong> Summary heatmap of the main effect sizes. Each column is scaled separately for readability; comparisons across columns should use the printed values rather than the color intensity.</figcaption>
</figure>

The NCA condition is the clearest mechanistic failure. Figure 6 shows the diagnostic in one place: held-out synthetic next-patch token accuracy was 0.0024%, the transferred model finished at 6.779 downstream CE versus 6.232 for scratch and 6.044 for NLP prepretraining, and its midlayer CKA to the NLP-prepretrained model was 0.151. The transferred NCA model also had an effective rank of 4.6, compared with 48.4 for scratch. Because the implementation had reference-parity checks against paper code fixtures, this result is informative about the training mechanism rather than just the generator implementation. In this run, a validated task generator did not produce a useful upstream learning problem for the model, so the failure cannot be reduced to a downstream evaluation artifact.

<figure>
  <img src="/images/pptrain-replication/nca_showcase.png" alt="NCA upstream accuracy, downstream loss, and representation diagnostics" style="width:100%;">
  <figcaption><strong>Figure 6.</strong> NCA failed before useful transfer. The synthetic task was barely learned, downstream eval loss was worse than both scratch and NLP prepretraining, and the transferred representation was far from the NLP-prepretrained geometry.</figcaption>
</figure>

## Diagnostics

Although the representation diagnostics are descriptive rather than primary success criteria, they match the outcome metrics. Relative to scratch, synthetic transfer has lower CKA to the NLP-prepretrained model. Simpler tasks is the mildest case, combining high activation CKA to NLP prepretraining with the only positive scratch gap, whereas NCA shows the opposite pattern: low CKA, low effective rank, high divergence, and the worst direct upstream synthetic accuracy.

<figure>
  <img src="/images/pptrain-replication/activation_cka_to_baseline.png" alt="Activation CKA to NLP prepretraining" style="width:80%;">
  <figcaption><strong>Figure 7.</strong> Midlayer activation CKA to the corresponding NLP-prepretrained model. Higher values indicate more similar hidden-state geometry on held-out downstream tokens. Simpler tasks is closest to the NLP method; NCA is farthest away.</figcaption>
</figure>

<figure>
  <img src="/images/pptrain-replication/logit_divergence_to_baseline.png" alt="Logit divergence to NLP prepretraining" style="width:80%;">
  <figcaption><strong>Figure 8.</strong> Reference KL divergence from synthetic transfer to the NLP-prepretrained model, shown in scaled units for readability. Lower values indicate closer predictive distributions.</figcaption>
</figure>

<figure>
  <img src="/images/pptrain-replication/activation_effective_rank.png" alt="Activation effective rank" style="width:100%;">
  <figcaption><strong>Figure 9.</strong> Effective rank of midpoint hidden states on held-out downstream tokens. Low rank indicates narrow internal activity; NCA is the lowest-rank transferred condition.</figcaption>
</figure>

## Interpretation

The measured result is bounded but consistent. Under this setup, synthetic prepretraining worsens downstream NLP training in five of six task families. The two controls locate the failure: random initialization tests whether synthetic transfer helps at all, while NLP prepretraining tests whether the same upstream budget is better spent on natural text. Synthetic transfer fails the first comparison in five of six tasks and the second comparison in all six.

A possible mechanism is stiffening plus covariate shift. If synthetic prepretraining moves the network into a less plastic state before the transition to natural text, and if the synthetic and downstream distributions are far apart, then the second stage becomes a difficult warm-start problem rather than a useful initialization. This interpretation is consistent with evidence that warm-starting a trained network can generalize worse than retraining from scratch, that deep networks can lose plasticity across task sequences, and that fine-tuning under distribution shift can underperform even when the pretrained representation is good ([Ash and Adams 2020](https://arxiv.org/abs/1910.08475), [Dohare et al. 2023](https://arxiv.org/abs/2306.13812), [Kumar et al. 2022](https://arxiv.org/abs/2202.10054)). In this run, five of the six synthetic tasks produced a worse starting point than random initialization.

The NCA condition illustrates this failure mode because its intended mechanism is that rich non-linguistic dynamics provide useful structure before natural text. Here, however, the NCA-prepretrained model did not learn the held-out synthetic prediction task and then transferred poorly to natural text. For this condition, the upstream curriculum failed before the downstream transfer question became relevant.

## Conclusion

Under the tested Pythia-410M, 12k-context, public-dataset protocol, synthetic prepretraining does not provide a useful initialization for downstream NLP training: NLP prepretraining achieves lower final evaluation loss than every synthetic method, and random initialization achieves lower final evaluation loss than five of the six synthetic methods.

The evaluation also identifies the necessary controls for future prepretraining claims. A synthetic upstream method should beat random initialization, beat a natural-text upstream budget, and show that the synthetic task was learned; without those checks, a synthetic curriculum can move the model into a less useful region of parameter space while still appearing plausible as a pretraining method.

## Appendix

<figure>
  <img src="/images/pptrain-replication/convergence_step_delta.png" alt="Convergence step delta" style="width:100%;">
  <figcaption><strong>Figure A1.</strong> Steps by which synthetic transfer reaches the random-init baseline's final loss. Positive values indicate faster convergence. The profile did not produce a meaningful convergence advantage.</figcaption>
</figure>

<figure>
  <img src="/images/pptrain-replication/pairwise_logit_divergence.png" alt="Pairwise logit divergence matrix" style="width:85%;">
  <figcaption><strong>Figure A2.</strong> Pairwise Jensen-Shannon divergence between predictive distributions on a shared diagnostic text bundle. Lower values indicate more similar model predictions.</figcaption>
</figure>

<figure>
  <img src="/images/pptrain-replication/pairwise_activation_cka.png" alt="Pairwise activation CKA matrix" style="width:85%;">
  <figcaption><strong>Figure A3.</strong> Pairwise midpoint activation CKA on a shared diagnostic text bundle. Higher values indicate more similar internal representation structure.</figcaption>
</figure>

## References

1. Jordan T. Ash and Ryan P. Adams. [On Warm-Starting Neural Network Training](https://arxiv.org/abs/1910.08475). NeurIPS 2020.
2. Stella Biderman et al. [Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling](https://arxiv.org/abs/2304.01373). ICML 2023.
3. Shibhansh Dohare et al. [Maintaining Plasticity in Deep Continual Learning](https://arxiv.org/abs/2306.13812). 2023.
4. Jordan Hoffmann et al. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). NeurIPS 2022.
5. Liangze Jiang et al. [Procedural Pretraining: Warming Up Language Models with Abstract Data](https://arxiv.org/abs/2601.21725). ICML 2026.
6. Jared Kaplan et al. [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361). 2020.
7. Kalpesh Krishna et al. [Does Pretraining for Summarization Require Knowledge Transfer?](https://aclanthology.org/2021.findings-emnlp.273/). Findings of EMNLP 2021.
8. Ananya Kumar et al. [Fine-Tuning can Distort Pretrained Features and Underperform Out-of-Distribution](https://arxiv.org/abs/2202.10054). ICLR 2022.
9. Dan Lee et al. [Training Language Models via Neural Cellular Automata](https://arxiv.org/abs/2603.10055). 2026.
10. Quentin Lhoest et al. [Datasets: A Community Library for Natural Language Processing](https://arxiv.org/abs/2109.02846). EMNLP Demo 2021.
11. Alexander Mordvintsev et al. [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca). Distill 2020.
12. Guilherme Penedo et al. [The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale](https://arxiv.org/abs/2406.17557). 2024.
13. Pablo Villalobos et al. [Will we run out of data? Limits of LLM scaling based on human-generated data](https://arxiv.org/abs/2211.04325). 2022.
14. Yuhuai Wu et al. [LIME: Learning Inductive Bias for Primitives of Mathematical Reasoning](https://proceedings.mlr.press/v139/wu21c.html). ICML 2021.
15. Yuhuai Wu, Felix Li, and Percy Liang. [Insights into Pre-training via Simpler Synthetic Tasks](https://arxiv.org/abs/2206.10139). 2022.
16. Hugging Face. [HuggingFaceFW/fineweb-edu dataset card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu).
17. Hugging Face. [HuggingFaceTB/finemath dataset card](https://huggingface.co/datasets/HuggingFaceTB/finemath).
18. Vladimir Blagojevic. [vblagoje/cc_news dataset card](https://huggingface.co/datasets/vblagoje/cc_news).
