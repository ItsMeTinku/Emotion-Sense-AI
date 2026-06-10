"""
reports/report_generator.py
============================
Generates PDF reports and CSV / Excel exports of emotion history.

Dependencies (optional — graceful degradation):
    pip install reportlab pandas openpyxl
"""

import os
import csv
import json
from datetime import datetime
from typing import Optional


REPORTS_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(REPORTS_DIR, exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _emotion_emoji(emotion: str) -> str:
    MAP = {
        "Happy": "😊", "Sad": "😢", "Angry": "😠",
        "Anxious": "😰", "Stressed": "😖", "Excited": "🤩",
        "Fearful": "😱", "Neutral": "😐",
    }
    return MAP.get(emotion, "🔵")


# ── CSV Export ────────────────────────────────────────────────────────────────

def export_csv(history: list[dict], username: str) -> str:
    """Write history to CSV and return the file path."""
    path = os.path.join(REPORTS_DIR, f"{username}_history_{_timestamp()}.csv")
    fields = ["id", "timestamp", "primary_emotion", "confidence",
              "stress_level", "source", "input_text"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(history)
    return path


# ── Excel Export ──────────────────────────────────────────────────────────────

def export_excel(history: list[dict], username: str) -> str:
    """Write history to Excel (.xlsx) and return path."""
    try:
        import pandas as pd
        path = os.path.join(REPORTS_DIR, f"{username}_history_{_timestamp()}.xlsx")
        df = pd.DataFrame(history)[
            ["timestamp", "primary_emotion", "confidence", "stress_level",
             "source", "input_text"]
        ]
        df.columns = ["Timestamp", "Emotion", "Confidence (%)",
                      "Stress Level", "Source", "Input Text"]
        df.to_excel(path, index=False, engine="openpyxl")
        return path
    except ImportError:
        return export_csv(history, username)    # graceful fallback


# ── PDF Report ────────────────────────────────────────────────────────────────

def export_pdf(history: list[dict], stats: dict, username: str) -> str:
    """Generate a styled PDF wellness report using ReportLab."""
    path = os.path.join(REPORTS_DIR, f"{username}_report_{_timestamp()}.pdf")

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        Table, TableStyle, HRFlowable)
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        doc = SimpleDocTemplate(path, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story  = []

        # ── Header ──────────────────────────────────────────────────
        title_style = ParagraphStyle(
            "Title", parent=styles["Title"],
            fontSize=22, textColor=colors.HexColor("#4A00E0"),
            spaceAfter=4
        )
        story.append(Paragraph("EmotionSense AI", title_style))
        story.append(Paragraph("Mental Wellness Report", styles["Heading2"]))
        story.append(HRFlowable(width="100%", thickness=1,
                                color=colors.HexColor("#4A00E0")))
        story.append(Spacer(1, 0.3*cm))

        meta_style = ParagraphStyle("Meta", parent=styles["Normal"],
                                    fontSize=9, textColor=colors.grey)
        story.append(Paragraph(
            f"User: <b>{username}</b> &nbsp;&nbsp; "
            f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}",
            meta_style))
        story.append(Spacer(1, 0.5*cm))

        # ── Summary stats ────────────────────────────────────────────
        story.append(Paragraph("📊 Summary", styles["Heading3"]))
        top_em = stats["frequency"][0]["primary_emotion"] if stats["frequency"] else "N/A"
        summary_data = [
            ["Total Sessions", str(stats["total"])],
            ["Most Frequent Emotion", top_em],
            ["Average Stress Level", f"{stats['avg_stress']}%"],
        ]
        tbl = Table(summary_data, colWidths=[8*cm, 8*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f4f4ff")),
            ("TEXTCOLOR",  (0,0), (0,-1), colors.HexColor("#4A00E0")),
            ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,-1), 10),
            ("ROWBACKGROUNDS", (0,0), (-1,-1),
             [colors.HexColor("#eeeeff"), colors.white]),
            ("BOX",        (0,0), (-1,-1), 0.5, colors.HexColor("#4A00E0")),
            ("INNERGRID",  (0,0), (-1,-1), 0.25, colors.grey),
            ("PADDING",    (0,0), (-1,-1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.5*cm))

        # ── Emotion frequency table ──────────────────────────────────
        if stats["frequency"]:
            story.append(Paragraph("📈 Emotion Frequency", styles["Heading3"]))
            freq_data = [["Emotion", "Sessions"]] + [
                [f"{_emotion_emoji(r['primary_emotion'])} {r['primary_emotion']}",
                 str(r["cnt"])]
                for r in stats["frequency"]
            ]
            ftbl = Table(freq_data, colWidths=[10*cm, 6*cm])
            ftbl.setStyle(TableStyle([
                ("BACKGROUND",     (0,0), (-1,0), colors.HexColor("#4A00E0")),
                ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
                ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0,1), (-1,-1),
                 [colors.HexColor("#f4f4ff"), colors.white]),
                ("BOX",            (0,0), (-1,-1), 0.5, colors.grey),
                ("INNERGRID",      (0,0), (-1,-1), 0.25, colors.lightgrey),
                ("PADDING",        (0,0), (-1,-1), 5),
            ]))
            story.append(ftbl)
            story.append(Spacer(1, 0.5*cm))

        # ── Recent sessions ──────────────────────────────────────────
        story.append(Paragraph("📋 Recent Sessions (last 10)", styles["Heading3"]))
        recent = history[:10]
        if recent:
            log_data = [["#", "Timestamp", "Emotion", "Conf%", "Stress%"]]
            for i, row in enumerate(recent, 1):
                log_data.append([
                    str(i),
                    row.get("timestamp", "")[:16],
                    f"{_emotion_emoji(row['primary_emotion'])} {row['primary_emotion']}",
                    f"{row['confidence']}%",
                    f"{row['stress_level']}%",
                ])
            ltbl = Table(log_data, colWidths=[1.2*cm, 4.5*cm, 4.5*cm, 2.4*cm, 2.4*cm])
            ltbl.setStyle(TableStyle([
                ("BACKGROUND",     (0,0), (-1,0), colors.HexColor("#2c2c54")),
                ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
                ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE",       (0,0), (-1,-1), 8),
                ("ROWBACKGROUNDS", (0,1), (-1,-1),
                 [colors.HexColor("#f9f9ff"), colors.white]),
                ("BOX",            (0,0), (-1,-1), 0.5, colors.grey),
                ("INNERGRID",      (0,0), (-1,-1), 0.25, colors.lightgrey),
                ("PADDING",        (0,0), (-1,-1), 4),
            ]))
            story.append(ltbl)

        story.append(Spacer(1, 0.8*cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Paragraph(
            "Generated by EmotionSense AI — "
            "Your Mental Wellness Companion 💙",
            ParagraphStyle("Footer", parent=styles["Normal"],
                           fontSize=8, textColor=colors.grey,
                           alignment=TA_CENTER)
        ))

        doc.build(story)
        return path

    except ImportError:
        # ReportLab not installed — fall back to CSV
        return export_csv(history, username)
