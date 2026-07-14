#!/usr/bin/env python3
"""Generate a compact NCA diagnostic figure for the prepretraining article."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path("/home/davwis/main")
WEBSITE_DIR = Path(__file__).resolve().parents[3]
RESULTS = (
    ROOT
    / "workspace/pptrain/internal/runs/paper_proxy_pythia410m_12k_20260703_1552/replication_results.json"
)
OUT_DIR = WEBSITE_DIR / "images/pptrain-replication"
ARTIFACT_DIR = WEBSITE_DIR / "docs/pptrain-replication/artifacts/figures"


def mean_std(metric: dict) -> tuple[float, float, list[float]]:
    return float(metric["mean"]), float(metric["std"]), [float(v) for v in metric["values"]]


def style(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.8, alpha=0.65)
    ax.set_axisbelow(True)


def save(fig: plt.Figure) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    for directory in (OUT_DIR, ARTIFACT_DIR):
        fig.savefig(directory / "nca_showcase.png", dpi=220, bbox_inches="tight", transparent=True)


def main() -> None:
    data = json.loads(RESULTS.read_text())
    nca = data["tasks"]["nca"]
    metrics = nca["metrics"]
    diagnostics = nca["diagnostics"]

    nca_acc_mean, nca_acc_sd, nca_acc_values = mean_std(metrics["nca_synthetic_token_accuracy"])
    loss_claim = nca["claims"]["transfer_signal"]
    scratch_loss = loss_claim["scratch_loss"]
    transferred_loss = loss_claim["transferred_loss"]
    nlp_loss = nca["claims"]["compute_matched_gain"]["baseline_loss"]

    cka = diagnostics["activation_cka_to_baseline"]
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "figure.facecolor": "none",
            "axes.facecolor": "none",
        }
    )

    fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.2), constrained_layout=True)

    ax = axes[0]
    ax.bar([0], [nca_acc_mean], yerr=[nca_acc_sd], color="#CC6677", edgecolor="#222222", capsize=3)
    jitter = np.linspace(-0.04, 0.04, len(nca_acc_values))
    ax.scatter(np.zeros(len(nca_acc_values)) + jitter, nca_acc_values, color="#222222", s=18, zorder=3)
    ax.set_title("NCA upstream task")
    ax.set_ylabel("held-out token accuracy (%)")
    ax.set_xticks([0], ["NCA"])
    ax.set_ylim(0.0, 0.006)
    ax.text(0, nca_acc_mean + nca_acc_sd + 0.00035, f"{nca_acc_mean:.4f}%", ha="center", va="bottom")
    style(ax)

    ax = axes[1]
    labels = ["scratch", "NCA\ntransfer", "NLP\nwarmup"]
    values = [scratch_loss["mean"], transferred_loss["mean"], nlp_loss["mean"]]
    errors = [scratch_loss["std"], transferred_loss["std"], nlp_loss["std"]]
    colors = ["#999999", "#CC6677", "#0072B2"]
    bars = ax.bar(range(3), values, yerr=errors, color=colors, edgecolor="#222222", capsize=3)
    ax.set_title("Downstream text loss")
    ax.set_ylabel("eval cross-entropy")
    ax.set_xticks(range(3), labels)
    ax.set_ylim(5.95, 7.08)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.045, f"{value:.3f}", ha="center", va="bottom")
    style(ax)

    ax = axes[2]
    labels = ["scratch", "NCA\ntransfer", "NLP\nwarmup"]
    cka_values = [
        cka["scratch"]["mean"],
        cka["transferred"]["mean"],
        cka["nlp_prepretraining"]["mean"],
    ]
    cka_errors = [
        cka["scratch"]["std"],
        cka["transferred"]["std"],
        cka["nlp_prepretraining"]["std"],
    ]
    bars = ax.bar(range(3), cka_values, yerr=cka_errors, color=colors, edgecolor="#222222", capsize=3)
    ax.set_title("Representation geometry")
    ax.set_ylabel("midlayer CKA to NLP warmup")
    ax.set_xticks(range(3), labels)
    ax.set_ylim(0.0, 1.12)
    for bar, value in zip(bars, cka_values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.035, f"{value:.3f}", ha="center", va="bottom")
    style(ax)

    fig.suptitle("NCA pretraining failed before useful transfer", fontsize=12)
    save(fig)


if __name__ == "__main__":
    main()
