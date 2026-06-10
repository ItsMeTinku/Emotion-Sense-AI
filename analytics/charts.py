"""
analytics/charts.py
====================
Generates matplotlib charts embedded directly into the Tkinter GUI.
All functions return a Figure object ready to be rendered via FigureCanvasTkAgg.
"""

import io
from typing import Any
import matplotlib
matplotlib.use("Agg")          # headless backend — avoids Tcl/Tk conflicts
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.figure import Figure


# ── Color palette ────────────────────────────────────────────────────────────
EMOTION_COLORS = {
    "Happy":    "#FFD700",
    "Sad":      "#4A90D9",
    "Angry":    "#E74C3C",
    "Anxious":  "#F39C12",
    "Stressed": "#E67E22",
    "Excited":  "#2ECC71",
    "Fearful":  "#9B59B6",
    "Neutral":  "#95A5A6",
}
BG  = "#1a1a2e"
FG  = "#e0e0e0"
ACC = "#7c6aff"


def _style_fig(fig: Figure, ax_list: list):
    """Apply dark theme to a figure and its axes."""
    fig.patch.set_facecolor(BG)
    for ax in ax_list:
        ax.set_facecolor("#16213e")
        ax.tick_params(colors=FG, labelsize=8)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        ax.title.set_color(FG)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a4a")


# ── Public chart builders ─────────────────────────────────────────────────────

def emotion_bar_chart(scores: dict[str, float]) -> Figure:
    """Horizontal bar chart of emotion confidence scores."""
    labels = list(scores.keys())
    values = list(scores.values())
    colors = [EMOTION_COLORS.get(l, ACC) for l in labels]

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    bars = ax.barh(labels, values, color=colors, edgecolor="none", height=0.6)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Confidence (%)")
    ax.set_title("Emotion Scores", fontsize=11, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", color=FG, fontsize=8)

    _style_fig(fig, [ax])
    fig.tight_layout()
    return fig


def emotion_pie_chart(frequency: list[dict]) -> Figure:
    """Pie chart of emotion frequency from history."""
    if not frequency:
        fig, ax = plt.subplots(figsize=(4.5, 3.2))
        ax.text(0.5, 0.5, "No data yet", ha="center", va="center",
                color=FG, fontsize=12)
        ax.axis("off")
        _style_fig(fig, [ax])
        return fig

    labels = [r["primary_emotion"] for r in frequency]
    sizes  = [r["cnt"] for r in frequency]
    colors = [EMOTION_COLORS.get(l, ACC) for l in labels]

    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors,
        autopct="%1.0f%%", startangle=140,
        wedgeprops={"edgecolor": BG, "linewidth": 1.5},
    )
    for t in texts + autotexts:
        t.set_color(FG)
        t.set_fontsize(8)
    ax.set_title("Emotion Distribution", fontsize=11, fontweight="bold")
    _style_fig(fig, [ax])
    fig.tight_layout()
    return fig


def stress_trend_chart(history: list[dict]) -> Figure:
    """Line chart of stress_level over time (last 30 entries)."""
    recent = history[:30][::-1]      # chronological order
    if not recent:
        fig, ax = plt.subplots(figsize=(5.5, 3.0))
        ax.text(0.5, 0.5, "No data yet", ha="center", va="center",
                color=FG, fontsize=12)
        ax.axis("off")
        _style_fig(fig, [ax])
        return fig

    x     = list(range(len(recent)))
    y     = [r["stress_level"] for r in recent]
    dates = [r["timestamp"][:10] for r in recent]

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.fill_between(x, y, alpha=0.25, color="#E74C3C")
    ax.plot(x, y, color="#E74C3C", linewidth=2, marker="o", markersize=4)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Stress Level")
    ax.set_title("Stress Trend (Last 30 Sessions)", fontsize=11, fontweight="bold")

    # Show every 5th date label to avoid clutter
    step = max(1, len(dates) // 6)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(dates[::step], rotation=30, ha="right", fontsize=7)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))

    _style_fig(fig, [ax])
    fig.tight_layout()
    return fig


def weekly_bar_chart(weekly: list[dict]) -> Figure:
    """Stacked bar chart — emotions per day over the last 7 days."""
    if not weekly:
        fig, ax = plt.subplots(figsize=(5.5, 3.2))
        ax.text(0.5, 0.5, "No data this week", ha="center", va="center",
                color=FG, fontsize=12)
        ax.axis("off")
        _style_fig(fig, [ax])
        return fig

    from collections import defaultdict
    day_emotion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in weekly:
        day_emotion[row["day"]][row["primary_emotion"]] += row["cnt"]

    days     = sorted(day_emotion.keys())
    emotions = list(EMOTION_COLORS.keys())
    x        = list(range(len(days)))
    bottom   = [0] * len(days)

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    for em in emotions:
        vals = [day_emotion[d].get(em, 0) for d in days]
        if any(vals):
            ax.bar(x, vals, bottom=bottom,
                   color=EMOTION_COLORS[em], label=em,
                   edgecolor=BG, linewidth=0.5)
            bottom = [b + v for b, v in zip(bottom, vals)]

    ax.set_xticks(x)
    ax.set_xticklabels([d[-5:] for d in days], rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Sessions")
    ax.set_title("This Week's Emotions", fontsize=11, fontweight="bold")
    ax.legend(fontsize=7, loc="upper left",
              facecolor="#16213e", edgecolor="#2a2a4a",
              labelcolor=FG)
    _style_fig(fig, [ax])
    fig.tight_layout()
    return fig
