#!/usr/bin/env python3
"""Generate article figures for the parameter-sharing topology post."""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path("/home/davwis/main")
RESULT_PATH = (
    ROOT
    / "workspace/irregular-parameter-sharing/docs/hard-block-sharing/artifacts/combined_result.json"
)
IMAGE_DIR = ROOT / "harness/workspace/website/images/parameter-sharing-topology"
DOC_IMAGE_DIR = ROOT / "harness/workspace/website/docs/parameter-sharing-topology/artifacts/figures"


LABELS = {
    "unshared": "unshared\ndense",
    "sequence_depth": "sequence\ndepth",
    "cycle_depth": "cycle\ndepth",
    "sequence_width": "sequence\nwidth",
    "cycle_width": "cycle\nwidth",
    "diagonal": "diagonal\ndepth-width",
    "random": "balanced\nrandom",
    "max_distance": "max\ndistance",
    "best_random": "best-of-12\nrandom",
}

NAMES = {
    "unshared": "unshared dense MLP",
    "sequence_depth": "sequence cross-layer sharing",
    "cycle_depth": "cycle cross-layer sharing",
    "sequence_width": "sequence width sharing",
    "cycle_width": "cycle width sharing",
    "diagonal": "regular diagonal depth-width sharing",
    "random": "balanced random hard sharing",
    "max_distance": "maximum-depth-distance hard sharing",
    "best_random": "best-of-12 random hard sharing",
}


def load_rows() -> dict[str, dict[str, float]]:
    data = json.loads(RESULT_PATH.read_text())
    rows = {}
    for row in data["summary"]:
        name = row["name"]
        for key, expected in NAMES.items():
            if name == expected:
                rows[key] = row
                break
    missing = sorted(set(NAMES) - set(rows))
    if missing:
        raise RuntimeError(f"missing rows: {missing}")
    return rows


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.8, alpha=0.65)
    ax.set_axisbelow(True)


def save(fig: plt.Figure, stem: str) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DOC_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for directory in (IMAGE_DIR, DOC_IMAGE_DIR):
        fig.savefig(directory / f"{stem}.png", dpi=220, bbox_inches="tight")


def validation_ce_plot(rows: dict[str, dict[str, float]]) -> None:
    order = [
        "unshared",
        "sequence_depth",
        "cycle_depth",
        "sequence_width",
        "cycle_width",
        "diagonal",
        "random",
        "max_distance",
        "best_random",
    ]
    means = np.array([rows[k]["val_loss_mean"] for k in order])
    sds = np.array([rows[k]["val_loss_sd"] for k in order])
    colors = []
    for key in order:
        if key == "cycle_width":
            colors.append("#0072B2")
        elif key == "max_distance":
            colors.append("#009E73")
        elif key == "unshared":
            colors.append("#6B7280")
        else:
            colors.append("#B8B8B8")

    fig, ax = plt.subplots(figsize=(8.2, 4.3), constrained_layout=True)
    x = np.arange(len(order))
    bars = ax.bar(
        x,
        means,
        yerr=sds,
        capsize=3,
        color=colors,
        edgecolor="#222222",
        linewidth=0.7,
        error_kw={"elinewidth": 1.1, "ecolor": "#111111"},
    )
    ax.set_title("Validation loss by hard-sharing topology", fontsize=12, pad=8)
    ax.set_ylabel("validation cross-entropy, mean +/- sd")
    ax.set_xticks(x, [LABELS[k] for k in order], rotation=35, ha="right")
    ax.set_ylim(4.44, 4.685)
    style_axes(ax)
    for bar, mean in zip(bars, means):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            mean + 0.006,
            f"{mean:.4f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    save(fig, "validation_ce_by_topology")
    plt.close(fig)


def delta_plot(rows: dict[str, dict[str, float]]) -> None:
    order = [
        "sequence_depth",
        "cycle_depth",
        "sequence_width",
        "cycle_width",
        "diagonal",
        "random",
        "max_distance",
        "best_random",
    ]
    deltas = np.array([rows[k]["delta_vs_random"] for k in order])
    colors = []
    for key in order:
        if key == "cycle_width":
            colors.append("#0072B2")
        elif key == "max_distance":
            colors.append("#009E73")
        else:
            colors.append("#B8B8B8")

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    x = np.arange(len(order))
    bars = ax.bar(
        x,
        deltas,
        color=colors,
        edgecolor="#222222",
        linewidth=0.7,
    )
    ax.axhline(0, color="#222222", linewidth=0.9)
    ax.set_title("Matched topologies relative to balanced random", fontsize=12, pad=8)
    ax.set_ylabel("CE delta; lower is better")
    ax.set_xticks(x, [LABELS[k] for k in order], rotation=35, ha="right")
    ax.set_ylim(-0.072, 0.052)
    style_axes(ax)
    for bar, delta in zip(bars, deltas):
        y = delta - 0.005 if delta < 0 else delta + 0.004
        va = "top" if delta < 0 else "bottom"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y,
            f"{delta:+.4f}",
            ha="center",
            va=va,
            fontsize=8,
        )
    save(fig, "delta_vs_random")
    plt.close(fig)


def make_schedules() -> dict[str, np.ndarray]:
    depth = 16
    chunks = 16
    shared_blocks = 128
    depth_templates = shared_blocks // chunks
    width_templates = shared_blocks // depth

    cycle_depth = np.empty((depth, chunks), dtype=int)
    for layer in range(depth):
        template = layer % depth_templates
        for chunk in range(chunks):
            cycle_depth[layer, chunk] = template * chunks + chunk

    cycle_width = np.empty((depth, chunks), dtype=int)
    for layer in range(depth):
        for chunk in range(chunks):
            template = chunk % width_templates
            cycle_width[layer, chunk] = layer * width_templates + template

    diagonal = np.empty((depth, chunks), dtype=int)
    block_id = 0
    depth_shift = depth // 2
    chunk_shift = chunks // 2
    for layer in range(depth_shift):
        for chunk in range(chunks):
            diagonal[layer, chunk] = block_id
            diagonal[layer + depth_shift, (chunk + chunk_shift) % chunks] = block_id
            block_id += 1

    def bit_reverse(value: int, bits: int) -> int:
        out = 0
        for _ in range(bits):
            out = (out << 1) | (value & 1)
            value >>= 1
        return out

    layer_order = []
    for i in range((depth + 1) // 2):
        layer_order.append(i)
        if depth - 1 - i != i:
            layer_order.append(depth - 1 - i)
    chunk_bits = max(1, math.ceil(math.log2(chunks)))
    chunk_order = sorted(range(chunks), key=lambda x: bit_reverse(x, chunk_bits))
    ordered_positions = [(layer, chunk) for layer in layer_order for chunk in chunk_order]
    assigned: list[list[tuple[int, int]]] = [[] for _ in range(shared_blocks)]
    counts = [0 for _ in range(shared_blocks)]
    mapping: dict[tuple[int, int], int] = {}
    for layer, chunk in ordered_positions:
        best_id = 0
        best_score = (-1.0, 0.0, 0.0)
        for candidate_id in range(shared_blocks):
            if not assigned[candidate_id]:
                min_depth_gap = depth
                min_chunk_gap = chunks
            else:
                min_depth_gap = min(abs(layer - prev_layer) for prev_layer, _ in assigned[candidate_id])
                min_chunk_gap = min(abs(chunk - prev_chunk) for _, prev_chunk in assigned[candidate_id])
            score = (float(min_depth_gap), float(min_chunk_gap) / chunks, -float(counts[candidate_id]))
            if score > best_score:
                best_score = score
                best_id = candidate_id
        assigned[best_id].append((layer, chunk))
        counts[best_id] += 1
        mapping[(layer, chunk)] = best_id
    max_distance = np.array(
        [[mapping[(layer, chunk)] for chunk in range(chunks)] for layer in range(depth)],
        dtype=int,
    )

    return {
        "cycle across depth": cycle_depth,
        "cycle across width": cycle_width,
        "diagonal depth-width": diagonal,
        "maximum depth distance": max_distance,
    }


def schedule_plot() -> None:
    schedules = make_schedules()
    cmap = plt.get_cmap("tab20", 20)
    fig, axes = plt.subplots(1, 4, figsize=(10.4, 2.9), constrained_layout=True)
    for ax, (title, schedule) in zip(axes, schedules.items()):
        ax.imshow(schedule % 20, cmap=cmap, aspect="auto", interpolation="nearest")
        ax.set_title(title, fontsize=10, pad=5)
        ax.set_xticks([0, 7, 15])
        ax.set_yticks([0, 7, 15])
        ax.set_xlabel("MLP chunk")
        if ax is axes[0]:
            ax.set_ylabel("layer")
        else:
            ax.set_yticklabels([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.suptitle("Four 128-block schedules over 16 layers and 16 chunks", fontsize=12)
    save(fig, "sharing_topology_schedules")
    plt.close(fig)


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 12,
            "axes.labelsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    rows = load_rows()
    validation_ce_plot(rows)
    delta_plot(rows)
    schedule_plot()


if __name__ == "__main__":
    main()
