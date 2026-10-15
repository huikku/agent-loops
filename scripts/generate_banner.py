#!/usr/bin/env python3
"""Generate the refined future aerospace-styled widescreen banner for AI Agent Loops.
Aesthetic: Future aerospace flight deck interface, technical HUD,
DIN typography, matte slate palette, telemetry, and hazard striping.
Clean, uncluttered, high-legibility design.
"""
import os
from PIL import Image, ImageDraw, ImageFont

font_dir = "/tmp/aerospace_fonts"
din_bold = f"{font_dir}/D-DIN-Bold.ttf"
din_regular = f"{font_dir}/D-DIN.ttf"
din_exp = f"{font_dir}/D-DINExp-Bold.ttf"
mono_bold = f"{font_dir}/JetBrainsMono-Bold.ttf"
mono_reg = f"{font_dir}/JetBrainsMono-Regular.ttf"

# Colors - Future Aerospace Palette
BG_COLOR = (13, 16, 21)          # Matte Charcoal Slate
PANEL_BG = (20, 24, 32)          # Dark Industrial Basalt
PANEL_SUB = (27, 33, 44)         # Sub-box fill
PANEL_BORDER = (46, 56, 70)      # Hairline Steel
PANEL_BORDER_LIGHT = (65, 78, 96)
TEXT_WHITE = (248, 250, 252)     # Signal White
TEXT_CREAM = (226, 232, 240)     # Off-white
TEXT_MUTED = (156, 172, 192)     # Industrial Slate (higher contrast)
TEXT_DIM = (100, 115, 135)       # Hairline Grey
AMBER_ACCENT = (245, 131, 39)    # Aviation Safety Orange / Status Amber
AMBER_BG = (45, 26, 16)          # Deep amber badge background
AMBER_BORDER = (195, 95, 25)
CYAN_ACCENT = (56, 189, 248)     # Telemetry Cyan
CYAN_BG = (14, 38, 52)
CYAN_BORDER = (25, 95, 130)
GREEN_ACCENT = (52, 211, 153)    # System Online Green
GREEN_BG = (16, 42, 32)
GREEN_BORDER = (26, 105, 75)

W, H = 1600, 900
img = Image.new("RGB", (W, H), BG_COLOR)
draw = ImageDraw.Draw(img)

# Load Fonts with larger, readable sizes
f_main_title = ImageFont.truetype(din_exp, 56)
f_sub_title = ImageFont.truetype(din_bold, 21)
f_card_title = ImageFont.truetype(din_bold, 24)
f_card_sub = ImageFont.truetype(din_bold, 17)
f_badge = ImageFont.truetype(mono_bold, 13)
f_body = ImageFont.truetype(din_regular, 16)
f_body_bold = ImageFont.truetype(din_bold, 16)
f_mono = ImageFont.truetype(mono_reg, 14)
f_mono_bold = ImageFont.truetype(mono_bold, 14)
f_micro = ImageFont.truetype(mono_reg, 11)

def draw_crosshair(draw, cx, cy, size=8, color=(65, 78, 96)):
    draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=1)
    draw.line([(cx, cy - size), (cx, cy + size)], fill=color, width=1)

def draw_hazard_stripe(draw, sx, sy, sw, sh):
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=AMBER_ACCENT)
    for s in range(sx, sx + sw + 10, 10):
        draw.polygon([(s, sy + sh), (s + 5, sy), (s + 7, sy), (s + 2, sy + sh)], fill=BG_COLOR)

def draw_tracked_text(draw, x, y, text, font, fill, spacing=2):
    cur_x = x
    for char in text:
        draw.text((cur_x, y), char, font=font, fill=fill)
        bbox = font.getbbox(char)
        cur_x += (bbox[2] - bbox[0]) + spacing
    return cur_x

def measure_tracked_text(text, font, spacing=2):
    total = 0
    for char in text:
        bbox = font.getbbox(char)
        total += (bbox[2] - bbox[0]) + spacing
    return total

# --- Outer Framing & Aerospace Grid ---
draw.rectangle([14, 14, W - 15, H - 15], outline=PANEL_BORDER, width=1)
draw.rectangle([18, 18, W - 19, H - 19], outline=(30, 36, 45), width=1)

# Corner Bracket Accents
corners = [(14, 14, 1, 1), (W - 15, 14, -1, 1), (14, H - 15, 1, -1), (W - 15, H - 15, -1, -1)]
for cx, cy, dx, dy in corners:
    draw.line([(cx, cy), (cx + 28 * dx, cy)], fill=AMBER_ACCENT, width=3)
    draw.line([(cx, cy), (cx + 28 * dy, cy)], fill=AMBER_ACCENT, width=3)

# Grid Crosshairs
draw_crosshair(draw, 45, 45)
draw_crosshair(draw, W - 45, 45)
draw_crosshair(draw, 45, H - 45)
draw_crosshair(draw, W - 45, H - 45)
draw_crosshair(draw, 545, 110)
draw_crosshair(draw, 1055, 110)

# --- Top Header Telemetry Bar ---
draw_hazard_stripe(draw, 35, 28, 48, 16)
draw_tracked_text(draw, 95, 29, "FUTURE AEROSPACE // AUTONOMOUS AGENT HARNESS SPECIFICATION // TAC-COM REF 180286-LP", f_micro, TEXT_MUTED, spacing=2)

# Top Right Status Pill
status_w, status_h = 240, 24
status_x = W - 35 - status_w
draw.rectangle([status_x, 24, status_x + status_w, 24 + status_h], fill=AMBER_BG, outline=AMBER_BORDER, width=1)
draw.ellipse([status_x + 10, 32, status_x + 18, 40], fill=GREEN_ACCENT)
draw.text((status_x + 26, 28), "STATUS: FULLY DEPLOYABLE", font=f_badge, fill=AMBER_ACCENT)

# Separator Line
draw.line([(35, 56), (W - 35, 56)], fill=PANEL_BORDER, width=1)

# --- Main Title Area ---
draw.text((35, 68), "AI AGENT LOOPS", font=f_main_title, fill=TEXT_WHITE)
draw_tracked_text(draw, 37, 130, "LOOP ENGINEERING: AUTOMATE THE MECHANICAL WORK // PRESERVE THE HUMAN JUDGMENT", f_sub_title, AMBER_ACCENT, spacing=2)

# Quote Banner Block (Cleaner & higher contrast)
quote_x, quote_y, quote_w, quote_h = 35, 172, W - 70, 38
draw.rectangle([quote_x, quote_y, quote_x + quote_w, quote_y + quote_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
draw.rectangle([quote_x, quote_y, quote_x + 5, quote_y + quote_h], fill=CYAN_ACCENT)
quote_text = "\"I don't prompt Claude anymore. I have loops running that prompt Claude. My job is to write loops.\"  — Boris Cherny"
draw.text((quote_x + 18, quote_y + 10), quote_text, font=f_mono_bold, fill=TEXT_CREAM)
meta_str = "STANDARD CO AI SERIES // FIELD ARCHITECTURE"
meta_w = measure_tracked_text(meta_str, f_micro, spacing=1)
draw_tracked_text(draw, quote_x + quote_w - meta_w - 18, quote_y + 12, meta_str, f_micro, CYAN_ACCENT, spacing=1)

# --- Three Architectural Display Panels ---
col_y = 226
col_w = 496
col_h = 490
col_gap = 21

cards = [
    {
        "x": 35,
        "badge": "LAYER 01 // ZERO AI",
        "title": "DETERMINISTIC SCRIPTS",
        "subtitle": "The Mechanical Plumbing",
        "owner": "OWNER: CRON / SHELL / CI",
        "callout": "$0 TOKEN COST // 100% PREDICTABLE",
        "accent": CYAN_ACCENT,
        "bg_accent": CYAN_BG,
        "border_accent": CYAN_BORDER,
        "bullets": [
            "• Scrapes candidates, parses RSS, queries REST APIs",
            "• Polls filesystems, handles Git operations & JSON",
            "• Fast, reproducible, and zero hallucination risk",
            "• Eliminates mechanical conversational bottleneck"
        ]
    },
    {
        "x": 35 + col_w + col_gap,
        "badge": "LAYER 02 // COGNITIVE ENGINE",
        "title": "AGENT REASONING",
        "subtitle": "The Autonomous Worker",
        "owner": "OWNER: AUTONOMOUS AI AGENT",
        "callout": "SEMANTIC TRIAGE & CREATIVE DRAFTS",
        "accent": GREEN_ACCENT,
        "bg_accent": GREEN_BG,
        "border_accent": GREEN_BORDER,
        "bullets": [
            "• Reads full text, extracts commitments, triages items",
            "• Evaluates content against human criteria files",
            "• Synthesizes digests, drafts PRs, formats reports",
            "• Spawns brand new instance per run (ephemeral state)"
        ]
    },
    {
        "x": 35 + (col_w + col_gap) * 2,
        "badge": "LAYER 03 // HUMAN POLICY",
        "title": "HUMAN JUDGMENT",
        "subtitle": "The Taste & Safety Gatekeeper",
        "owner": "OWNER: HUMAN OPERATOR",
        "callout": "IMMUTABLE EDITORIAL AUTHORITY",
        "accent": AMBER_ACCENT,
        "bg_accent": AMBER_BG,
        "border_accent": AMBER_BORDER,
        "bullets": [
            "• Plain-English policy files: taste.md & rules.md",
            "• Defines quality bar, subjective tone & boundaries",
            "• Agent proposes rule edits; human ratchets them",
            "• Sole authority: agent never alters policies directly"
        ]
    }
]

for card in cards:
    cx = card["x"]
    accent = card["accent"]
    
    # Outer Card Frame
    draw.rectangle([cx, col_y, cx + col_w, col_y + col_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
    
    # Top Card Tab Header
    tab_h = 76
    draw.rectangle([cx, col_y, cx + col_w, col_y + tab_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.rectangle([cx, col_y, cx + 5, col_y + tab_h], fill=accent)
    
    # Badge and Title
    draw.text((cx + 18, col_y + 12), card["badge"], font=f_badge, fill=accent)
    draw.text((cx + 18, col_y + 36), card["title"], font=f_card_title, fill=TEXT_WHITE)
    
    # Subtitle / Role
    draw.text((cx + 18, col_y + tab_h + 16), card["subtitle"], font=f_card_sub, fill=TEXT_CREAM)
    
    # Highlight Callout Banner Pill
    call_y = col_y + tab_h + 46
    call_h = 36
    draw.rectangle([cx + 18, call_y, cx + col_w - 18, call_y + call_h], fill=card["bg_accent"], outline=card["border_accent"], width=1)
    draw.text((cx + 30, call_y + 9), card["callout"], font=f_mono_bold, fill=accent)
    
    # Bullet points with generous spacing
    by = call_y + call_h + 24
    for bullet in card["bullets"]:
        draw.text((cx + 20, by), bullet, font=f_body, fill=TEXT_MUTED)
        by += 40
        
    # Bottom Owner Pill inside Card
    own_h = 32
    own_y = col_y + col_h - own_h - 16
    draw.rectangle([cx + 18, own_y, cx + col_w - 18, own_y + own_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.text((cx + 28, own_y + 8), card["owner"], font=f_mono, fill=TEXT_DIM)

# --- Bottom Ribbon: Two Wide Telemetry Bands ---
bot_y = 730
bot_w = (W - 70 - 21) // 2
bot_h = 92

# Ribbon 1: Execution Taxonomy
rx1 = 35
draw.rectangle([rx1, bot_y, rx1 + bot_w, bot_y + bot_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
draw.rectangle([rx1, bot_y, rx1 + 4, bot_y + bot_h], fill=CYAN_ACCENT)
draw.text((rx1 + 18, bot_y + 12), "02 // EXECUTION TAXONOMY", font=f_badge, fill=CYAN_ACCENT)
draw.text((rx1 + 18, bot_y + 32), "THE 5 OPERATIONAL LOOP ARCHETYPES", font=f_card_sub, fill=TEXT_WHITE)
f_ribbon_items = ImageFont.truetype(din_bold, 15)
draw.text((rx1 + 18, bot_y + 58), "01 MESSAGE   ·   02 HEARTBEAT   ·   03 SCHEDULE   ·   04 EVENT HOOK   ·   05 GOAL LOOP (/goal)", font=f_ribbon_items, fill=TEXT_MUTED)

# Ribbon 2: Defensive Engineering
rx2 = 35 + bot_w + 21
draw.rectangle([rx2, bot_y, rx2 + bot_w, bot_y + bot_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
draw.rectangle([rx2, bot_y, rx2 + 4, bot_y + bot_h], fill=AMBER_ACCENT)
draw.text((rx2 + 18, bot_y + 12), "03 // PERSISTENCE & DEFENSE", font=f_badge, fill=AMBER_ACCENT)
draw.text((rx2 + 18, bot_y + 32), "ANTI-ENTROPY: THE 3 DEFENSIVE LAWS", font=f_card_sub, fill=TEXT_WHITE)
draw.text((rx2 + 18, bot_y + 58), "LAW I: PRE-FLIGHT CHECK   ·   LAW II: ATOMIC ROLLBACK   ·   LAW III: BE LOUD ON FAILURE", font=f_ribbon_items, fill=TEXT_MUTED)

# --- Bottom Telemetry / Footer Bar ---
foot_y = H - 38
draw.line([(35, foot_y), (W - 35, foot_y)], fill=PANEL_BORDER, width=1)
draw_tracked_text(draw, 35, foot_y + 10, "DESIGN SYSTEM: FUTURE AEROSPACE HUD // DIN TECHNICAL TYPOGRAPHY", f_micro, TEXT_DIM, spacing=2)
draw.text((640, foot_y + 10), "ALIENROBOT.COM // SPECIFICATION RUNBOOK", font=f_micro, fill=CYAN_ACCENT)

repo_str = "PUBLIC REPOSITORY: GITHUB.COM/HUIKKU/AGENT-LOOPS"
repo_w = measure_tracked_text(repo_str, f_micro, spacing=1)
draw_tracked_text(draw, W - 35 - repo_w, foot_y + 10, repo_str, f_micro, AMBER_ACCENT, spacing=1)

out_png = "/home/john/code/agent-loops/assets/banner.png"
out_jpg = "/home/john/code/agent-loops/assets/banner.jpg"
out_webp = "/home/john/code/agent-loops/assets/banner.webp"

img.save(out_png, "PNG")
img.save(out_jpg, "JPEG", quality=95)
img.save(out_webp, "WEBP", quality=95)
print(f"Refined clean banners saved: {out_png}, {out_jpg}, {out_webp}")
