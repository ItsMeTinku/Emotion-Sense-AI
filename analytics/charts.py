"""
analytics/charts.py — Dark-themed Matplotlib charts for EmotionSense AI.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from collections import defaultdict

EMOTION_COLORS = {
    "Happy":"#FFD700","Sad":"#4A90D9","Angry":"#E74C3C",
    "Anxious":"#F39C12","Stressed":"#E67E22","Excited":"#2ECC71",
    "Fearful":"#9B59B6","Neutral":"#95A5A6",
}
BG, FG, ACC = "#1a1a2e", "#e0e0e0", "#7c6aff"

def _style(fig, axes):
    fig.patch.set_facecolor(BG)
    for ax in axes:
        ax.set_facecolor("#16213e")
        ax.tick_params(colors=FG, labelsize=8)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        ax.title.set_color(FG)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a4a")

def emotion_bar_chart(scores: dict) -> Figure:
    labels = list(scores.keys())
    values = list(scores.values())
    colors = [EMOTION_COLORS.get(l, ACC) for l in labels]
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    bars = ax.barh(labels, values, color=colors, edgecolor="none", height=0.6)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Confidence (%)")
    ax.set_title("Emotion Confidence Scores", fontsize=11, fontweight="bold")
    for bar, val in zip(bars, values):
        ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
                f"{val:.1f}%", va="center", color=FG, fontsize=8)
    _style(fig, [ax])
    fig.tight_layout()
    return fig

def emotion_pie_chart(frequency: list) -> Figure:
    if not frequency:
        fig, ax = plt.subplots(figsize=(4.4, 3.2))
        ax.text(0.5, 0.5, "No data yet", ha="center", va="center", color=FG, fontsize=12)
        ax.axis("off"); _style(fig, [ax]); return fig
    labels = [r["primary_emotion"] for r in frequency]
    sizes  = [r["cnt"] for r in frequency]
    colors = [EMOTION_COLORS.get(l, ACC) for l in labels]
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    wedges, texts, autos = ax.pie(sizes, labels=labels, colors=colors,
        autopct="%1.0f%%", startangle=140,
        wedgeprops={"edgecolor": BG, "linewidth": 1.5})
    for t in texts + autos:
        t.set_color(FG); t.set_fontsize(8)
    ax.set_title("Emotion Distribution", fontsize=11, fontweight="bold")
    _style(fig, [ax]); fig.tight_layout(); return fig

def stress_trend_chart(history: list) -> Figure:
    recent = history[:30][::-1]
    if not recent:
        fig, ax = plt.subplots(figsize=(5.4, 3.0))
        ax.text(0.5, 0.5, "No data yet", ha="center", va="center", color=FG, fontsize=12)
        ax.axis("off"); _style(fig, [ax]); return fig
    x     = list(range(len(recent)))
    y     = [r["stress_level"] for r in recent]
    dates = [r["timestamp"][:10] for r in recent]
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.fill_between(x, y, alpha=0.25, color="#E74C3C")
    ax.plot(x, y, color="#E74C3C", linewidth=2, marker="o", markersize=4)
    ax.set_ylim(0, 100); ax.set_ylabel("Stress Level")
    ax.set_title("Stress Trend", fontsize=11, fontweight="bold")
    step = max(1, len(dates)//6)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(dates[::step], rotation=30, ha="right", fontsize=7)
    _style(fig, [ax]); fig.tight_layout(); return fig

def weekly_bar_chart(weekly: list) -> Figure:
    if not weekly:
        fig, ax = plt.subplots(figsize=(5.4, 3.2))
        ax.text(0.5, 0.5, "No data this week", ha="center", va="center", color=FG, fontsize=12)
        ax.axis("off"); _style(fig, [ax]); return fig
    day_em = defaultdict(lambda: defaultdict(int))
    for row in weekly:
        day_em[row["day"]][row["primary_emotion"]] += row["cnt"]
    days   = sorted(day_em.keys())
    x      = list(range(len(days)))
    bottom = [0]*len(days)
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    for em, color in EMOTION_COLORS.items():
        vals = [day_em[d].get(em,0) for d in days]
        if any(vals):
            ax.bar(x, vals, bottom=bottom, color=color, label=em,
                   edgecolor=BG, linewidth=0.5)
            bottom = [b+v for b,v in zip(bottom,vals)]
    ax.set_xticks(x)
    ax.set_xticklabels([d[-5:] for d in days], rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Sessions")
    ax.set_title("This Week\'s Emotions", fontsize=11, fontweight="bold")
    ax.legend(fontsize=7, loc="upper left",
              facecolor="#16213e", edgecolor="#2a2a4a", labelcolor=FG)
    _style(fig, [ax]); fig.tight_layout(); return fig
