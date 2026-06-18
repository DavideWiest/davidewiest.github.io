---
title: "pptrain, the ready-to-use pre-pretraining library"
date: 2026-06-18
permalink: /posts/2026/06/pptrain-ready-to-use-prepretraining/
tags:
  - machine-learning
  - language-models
  - pretraining
  - software
---

Pre-pretraining is a good idea trapped in an awkward workflow. The pitch is simple: before training a language model on natural text, first train it on synthetic tasks that may teach useful structure. Cellular automata, symbolic transformations, mathematical primitives all fit this pattern. One hurdle towords shipping this in production is that most of the work lives in paper-specific code, hidden data generators, and one-off training scripts. Another one is verifying the prepretrainer was instantiated correctly and actually has a positive affect. The package [`pptrain`](https://github.com/Axym-Labs/pptrain) can help practitioners with that:

## Ready to use

Install it via:

```bash
pip install pptrain
```

and start pre-pretraining with:

```python
from pptrain import PrePreTrainer, RunConfig, create_task
from pptrain.integrations import HFCausalLMAdapter, HFModelConfig

trainer = PrePreTrainer(
    task=create_task(
        "simpler_tasks",
        {
            "preset": "paper_binary_1m",
            "sequence_count": 256,
            "eval_sequence_count": 64,
            "max_length": 128,
        },
    ),
    model_adapter=HFCausalLMAdapter(
        HFModelConfig(model_name_or_path="sshleifer/tiny-gpt2")
    ),
    run_config=RunConfig(output_dir="runs/initial", max_steps=20),
)

bundle = trainer.fit().load_transfer_bundle()
```

`pptrain` packages several task families from the literature as reusable presets:

- `nca`: cellular-automata rollouts; tests whether simple dynamical systems can provide useful upstream structure.
- `dyck`: balanced-bracket languages; isolates nested and stack-like structure.
- `procedural`: abstract programs such as reverse, sort, set, union, and delete; tests algorithmic text transformations.
- `simpler_tasks`: copy, search, set operations, and related symbolic transformations; breaks pretraining into small controlled operations.
- `lime`: induction, deduction, and abduction tasks; targets primitives of mathematical reasoning.
- `summarization`: synthetic document transformations; separates compression and selection from factual knowledge transfer.

The presets are based on suggestions from the original papers and implementation, but can be heavily customized: for example, `nca` exposes grid size, number of states, patch size, perception and hidden dimensions, rollout stride and initial rollout steps, train/eval rule counts, sequence counts, maximum length, gzip-complexity band, and per-epoch regeneration.

## Reference parity

Production-readiness also requires a correctness check: because a changed generator, tokenizer, or serialization no longer tests the mechanism from the paper, `pptrain` includes reference-parity utilities that compare local outputs against original-source fixtures for LIME, synthetic summarization, procedural pretraining, and NCA pre-pretraining.

These checks are exact where they should be exact: normalized examples or token sequences must match the reference output. 

## Empirical testing

To determine whether and how well certain tasks interact with custom environments, users can use the evaluation and replication utilities built around the same interface from training. The library supports downstream transfer evaluation, compute-matched natural warmups, simple diagnostic metrics, plots, CSVs, and markdown reports.

## Extensibility

Users can write their own pre-pretraining logic by implementing `SymbolicTaskFamily`: define how examples are sampled, executed, serialized, and tokenized. If the task needs a custom dataset or loss path, implement `Task` directly.

If you're curious about internal structure, the core abstraction is a task family. A task family samples an example, executes it if needed, serializes it into tokens, and exposes a tokenizer specification. After that, the path is ordinary model training: build a dataset, train a Hugging Face causal language model, save the checkpoint, and export a transfer bundle.
