#!/usr/bin/env python3
"""Generate the refined future aerospace-styled widescreen banner for AI Agent Loops.
Aesthetic: Future aerospace flight deck interface, technical HUD,
DIN typography, matte slate palette, telemetry, and hazard striping.
"""
import os
from PIL import Image, ImageDraw, ImageFont

font_dir = "/tmp/aerospace_fonts"
din_bold = f"{font_dir}/D-DIN-Bold.ttf"
din_regular = f"{font_dir}/D-DIN.ttf"
din_exp = f"{font_dir}/D-DINExp-Bold.ttf"
mono_bold = f"{font_dir}/JetBrainsMono-Bold.ttf"
mono_reg = f"{font_dir}/JetBrainsMono-Regular.ttf"

# Colors - Future Aerospace / Alienrobot Palette
BG_COLOR = (15, 18, 23)          # Matte Charcoal Slate
PANEL_BG = (22, 27, 34)          # Dark Industrial Basalt
PANEL_SUB = (28, 34, 43)         # Sub-box fill
PANEL_BORDER = (46, 56, 70)      # Hairline Steel
PANEL_BORDER_LIGHT = (65, 78, 96)
TEXT_WHITE = (248, 250, 252)     # Signal White
TEXT_CREAM = (226, 232, 240)     # Off-white
TEXT_MUTED = (148, 163, 184)     # Industrial Slate
TEXT_DIM = (100, 115, 135)       # Hairline Grey
AMBER_ACCENT = (245, 131, 39)    # Aviation Safety Orange / Status Amber
AMBER_BG = (45, 26, 16)          # Deep amber badge background
AMBER_BORDER = (195, 95, 25)
CYAN_ACCENT = (56, 189, 248)     # Telemetry Cyan
GREEN_ACCENT = (52, 211, 153)    # System Online Green

W, H = 1600, 920
img = Image.new("RGB", (W, H), BG_COLOR)
draw = ImageDraw.Draw(img)

# Load Fonts
f_main_title = ImageFont.truetype(din_exp, 52)
f_sub_title = ImageFont.truetype(din_bold, 20)
f_col_hdr = ImageFont.truetype(din_bold, 15)
f_badge = ImageFont.truetype(mono_bold, 11)
f_body_bold = ImageFont.truetype(din_bold, 13)
f_body = ImageFont.truetype(din_regular, 12)
f_mono = ImageFont.truetype(mono_reg, 11)
f_mono_bold = ImageFont.truetype(mono_bold, 11)
f_micro = ImageFont.truetype(mono_reg, 10)

def draw_crosshair(draw, cx, cy, size=8, color=(70, 82, 100)):
    draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=1)
    draw.line([(cx, cy - size), (cx, cy + size)], fill=color, width=1)

def draw_hazard_stripe(draw, sx, sy, sw, sh):
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=AMBER_ACCENT)
    for s in range(sx, sx + sw + 8, 8):
        draw.polygon([(s, sy + sh), (s + 4, sy), (s + 6, sy), (s + 2, sy + sh)], fill=BG_COLOR)

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

def draw_wrapped_text(draw, x, y, text, font, fill, max_width, line_height=18):
    words = text.split()
    cur_line = ""
    cur_y = y
    for word in words:
        test_line = (cur_line + " " + word).strip()
        bbox = font.getbbox(test_line)
        line_w = bbox[2] - bbox[0]
        if line_w <= max_width:
            cur_line = test_line
        else:
            if cur_line:
                draw.text((x, cur_y), cur_line, font=font, fill=fill)
                cur_y += line_height
            cur_line = word
    if cur_line:
        draw.text((x, cur_y), cur_line, font=font, fill=fill)
        cur_y += line_height
    return cur_y

# --- Outer Framing & Aerospace Grid ---
draw.rectangle([14, 14, W - 15, H - 15], outline=PANEL_BORDER, width=1)
draw.rectangle([18, 18, W - 19, H - 19], outline=(30, 36, 45), width=1)

# Corner Bracket Accents
corners = [(14, 14, 1, 1), (W - 15, 14, -1, 1), (14, H - 15, 1, -1), (W - 15, H - 15, -1, -1)]
for cx, cy, dx, dy in corners:
    draw.line([(cx, cy), (cx + 25 * dx, cy)], fill=AMBER_ACCENT, width=3)
    draw.line([(cx, cy), (cx + 25 * dy, cy)], fill=AMBER_ACCENT, width=3)

# Grid Crosshairs
draw_crosshair(draw, 50, 50)
draw_crosshair(draw, W - 50, 50)
draw_crosshair(draw, 50, H - 50)
draw_crosshair(draw, W - 50, H - 50)
draw_crosshair(draw, 530, 115)
draw_crosshair(draw, 1060, 115)

# --- Top Header Telemetry Bar ---
draw_hazard_stripe(draw, 35, 30, 48, 16)
draw_tracked_text(draw, 95, 31, "FUTURE AEROSPACE // AUTONOMOUS AGENT HARNESS SPECIFICATION // TAC-COM REF 180286-LP", f_micro, TEXT_MUTED, spacing=2)

# Top Right Status Pill
status_w, status_h = 240, 24
status_x = W - 35 - status_w
draw.rectangle([status_x, 26, status_x + status_w, 26 + status_h], fill=AMBER_BG, outline=AMBER_BORDER, width=1)
draw.ellipse([status_x + 10, 34, status_x + 18, 42], fill=GREEN_ACCENT)
draw.text((status_x + 26, 30), "STATUS: FULLY DEPLOYABLE", font=f_badge, fill=AMBER_ACCENT)

# Separator Line
draw.line([(35, 58), (W - 35, 58)], fill=PANEL_BORDER, width=1)

# --- Main Title Area ---
draw.text((35, 68), "AI AGENT LOOPS", font=f_main_title, fill=TEXT_WHITE)
draw_tracked_text(draw, 37, 126, "LOOP ENGINEERING: AUTOMATE THE MECHANICAL WORK // PRESERVE THE HUMAN JUDGMENT", f_sub_title, AMBER_ACCENT, spacing=2)

desc_str = "A field guide to autonomous goal loops, deterministic script plumbing, decoupled evaluators, persistent git/disk state, and anti-entropy safety harnesses."
draw.text((37, 154), desc_str, font=f_body, fill=TEXT_MUTED)

# Quote Banner Block
quote_x, quote_y, quote_w, quote_h = 35, 180, W - 70, 34
draw.rectangle([quote_x, quote_y, quote_x + quote_w, quote_y + quote_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
draw.rectangle([quote_x, quote_y, quote_x + 4, quote_y + quote_h], fill=CYAN_ACCENT)
quote_text = "\"I don't prompt Claude anymore. I have loops running that prompt Claude. My job is to write loops.\"  — Boris Cherny (Creator of Claude Code)"
draw.text((quote_x + 16, quote_y + 9), quote_text, font=f_mono_bold, fill=TEXT_CREAM)
author_meta = "ADDY OSMANI // PETER STEINBERGER // JASON ELGIN (STANDARD CO)"
draw.text((quote_x + quote_w - 430, quote_y + 10), author_meta, font=f_micro, fill=CYAN_ACCENT)

# --- Three Architectural Display Panels ---
col_y = 226
col_w = 496
col_h = 632
col_gap = 21

cols = [
    (35, "01 // SYSTEM ARCHITECTURE", "THREE JOBS, THREE OWNERS (3-LAYER STACK)", AMBER_ACCENT),
    (35 + col_w + col_gap, "02 // EXECUTION TAXONOMY", "THE 5 OPERATIONAL LOOP ARCHETYPES", CYAN_ACCENT),
    (35 + (col_w + col_gap) * 2, "03 // PERSISTENCE & SAFETY", "STATE LEDGERS & ANTI-SILENT-FAILURE", GREEN_ACCENT),
]

for idx, (cx, badge_text, title_text, accent_color) in enumerate(cols):
    # Main panel bounding box
    draw.rectangle([cx, col_y, cx + col_w, col_y + col_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
    
    # Header tab (Stacked layout: badge on top, title below)
    tab_h = 44
    draw.rectangle([cx, col_y, cx + col_w, col_y + tab_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.rectangle([cx, col_y, cx + 4, col_y + tab_h], fill=accent_color)
    draw.text((cx + 14, col_y + 6), badge_text, font=f_badge, fill=accent_color)
    draw.text((cx + 14, col_y + 22), title_text, font=f_col_hdr, fill=TEXT_WHITE)

# ------------------------------------------------------------------------------
# COLUMN 1: THE 3-LAYER ARCHITECTURE
# ------------------------------------------------------------------------------
c1_x = 35 + 16
c1_w = col_w - 32
c1_y = col_y + 54

c1_layers = [
    {
        "num": "LAYER 01",
        "name": "DETERMINISTIC SCRIPTS",
        "owner": "OWNER: CRON / SHELL",
        "color": CYAN_ACCENT,
        "role": "The Mechanical Plumbing (Zero AI Needed)",
        "bullets": [
            "• Land-grab scrapers, RSS aggregators, REST API clients",
            "• Candidate ingestion, filesystem polling, git hooks",
            "• Pure deterministic Python/Bash: fast, predictable, $0 token cost"
        ]
    },
    {
        "num": "LAYER 02",
        "name": "AGENT REASONING",
        "owner": "OWNER: AUTONOMOUS AGENT",
        "color": GREEN_ACCENT,
        "role": "The Cognitive Worker & Triage Engine",
        "bullets": [
            "• Reads full text, extracts commitments, triages candidates",
            "• Evaluates content against human criteria and quality thresholds",
            "• Generates synthesis, drafts emails/PRs, packages actionables"
        ]
    },
    {
        "num": "LAYER 03",
        "name": "HUMAN JUDGMENT / POLICY",
        "owner": "OWNER: HUMAN OPERATOR",
        "color": AMBER_ACCENT,
        "role": "The Taste Owner & Safety Gatekeeper",
        "bullets": [
            "• Plain-English policy files: taste.md, rules.md, criteria.md",
            "• Agent can propose candidate promotions/retirements",
            "• NEVER allows agent to modify policies unilaterally"
        ]
    }
]

cur_y = c1_y
for lay in c1_layers:
    box_h = 176
    draw.rectangle([c1_x, cur_y, c1_x + c1_w, cur_y + box_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.rectangle([c1_x, cur_y, c1_x + 3, cur_y + box_h], fill=lay["color"])
    
    # header row
    draw.text((c1_x + 12, cur_y + 9), lay["num"], font=f_badge, fill=lay["color"])
    draw.text((c1_x + 75, cur_y + 7), lay["name"], font=f_body_bold, fill=TEXT_WHITE)
    draw.text((c1_x + c1_w - 150, cur_y + 9), lay["owner"], font=f_micro, fill=TEXT_DIM)
    
    draw.line([(c1_x + 12, cur_y + 26), (c1_x + c1_w - 12, cur_y + 26)], fill=PANEL_BORDER, width=1)
    
    # role
    draw.text((c1_x + 14, cur_y + 33), lay["role"], font=f_mono_bold, fill=TEXT_CREAM)
    
    # bullets
    by = cur_y + 56
    for b in lay["bullets"]:
        draw.text((c1_x + 14, by), b, font=f_body, fill=TEXT_MUTED)
        by += 32
    
    cur_y += box_h + 12

# ------------------------------------------------------------------------------
# COLUMN 2: THE 5 LOOP ARCHETYPES
# ------------------------------------------------------------------------------
c2_x = 35 + col_w + col_gap + 16
c2_w = col_w - 32
c2_y = col_y + 54

c2_loops = [
    ("01 // MESSAGE LOOP", "Interactive chat turn (human is half the loop; prompt & reply)"),
    ("02 // HEARTBEAT LOOP", "Metronome pulse: 30s site health checks or 30m urgent email triage"),
    ("03 // SCHEDULE / CRON", "Calendar cadence: bi-weekly meeting summarizer or 6am research digest"),
    ("04 // EVENT HOOK", "Trigger-on-event: git PR checks, UI component duplication detectors"),
]

cur_y = c2_y
for title, desc in c2_loops:
    box_h = 64
    draw.rectangle([c2_x, cur_y, c2_x + c2_w, cur_y + box_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.text((c2_x + 12, cur_y + 8), title, font=f_badge, fill=CYAN_ACCENT)
    draw.text((c2_x + 12, cur_y + 28), desc, font=f_body, fill=TEXT_MUTED)
    cur_y += box_h + 8

# Deep Dive into Goal Loop Box
goal_h = 268
draw.rectangle([c2_x, cur_y, c2_x + c2_w, cur_y + goal_h], fill=PANEL_SUB, outline=AMBER_BORDER, width=1)
draw.rectangle([c2_x, cur_y, c2_x + 4, cur_y + goal_h], fill=AMBER_ACCENT)
draw.text((c2_x + 12, cur_y + 10), "GOAL LOOP DEEP DIVE: THE /goal SPECIFICATION", font=f_body_bold, fill=TEXT_WHITE)
draw.text((c2_x + 12, cur_y + 30), "Runs recursively until state condition is verified true:", font=f_body, fill=TEXT_MUTED)

goal_rules = [
    ("1. TESTABLE OBJECTIVE:", "Must have a binary, measurable contract (\"reconcile all 30 invoices\"), NOT subjective (\"make it look good\")."),
    ("2. INDEPENDENT GRADER:", "\"An agent cannot grade its own paper.\" Verification is performed by a decoupled checker agent."),
    ("3. HARD STOP BOUNDS:", "Mandatory iteration ceiling (e.g. max 10 passes or 2hr runtime) to prevent runaway infinite token burn."),
    ("4. AUDIT TRAIL:", "Emits structured decision diffs per cycle.")
]

gy = cur_y + 54
for ghdr, gdesc in goal_rules:
    draw.text((c2_x + 12, gy), ghdr, font=f_mono_bold, fill=AMBER_ACCENT)
    gy += 17
    gy = draw_wrapped_text(draw, c2_x + 14, gy, gdesc, f_body, TEXT_MUTED, max_width=c2_w - 24, line_height=17)
    gy += 6

# ------------------------------------------------------------------------------
# COLUMN 3: STATE & ANTI-SILENT-FAILURE
# ------------------------------------------------------------------------------
c3_x = 35 + (col_w + col_gap) * 2 + 16
c3_w = col_w - 32
c3_y = col_y + 54

cur_y = c3_y

# Section: Ephemeral State Box
draw.rectangle([c3_x, cur_y, c3_x + c3_w, cur_y + 154], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
draw.rectangle([c3_x, cur_y, c3_x + 3, cur_y + 154], fill=GREEN_ACCENT)
draw.text((c3_x + 12, cur_y + 9), "THE STATE AXIOM: ZERO IN-MEMORY RETENTION", font=f_body_bold, fill=TEXT_WHITE)
draw.text((c3_x + 12, cur_y + 30), "Every loop run spawns a brand new agent with zero memory.", font=f_body, fill=TEXT_MUTED)
draw.text((c3_x + 12, cur_y + 50), "System state is strictly defined by what is committed to disk/git:", font=f_body, fill=TEXT_CREAM)

state_bullets = [
    "• Deduplication Ledger: seen_ids.json / processed_urls.txt",
    "• Decision Log: appended record of picked vs. skipped + rationale",
    "• Proposal File: agent writes suggestions; human ratchets them"
]
sy = cur_y + 74
for sb in state_bullets:
    draw.text((c3_x + 12, sy), sb, font=f_mono, fill=CYAN_ACCENT)
    sy += 22

cur_y += 154 + 12

# Section: The Three Defensive Laws against Silent Failures
laws_h = 386
draw.rectangle([c3_x, cur_y, c3_x + c3_w, cur_y + laws_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
draw.rectangle([c3_x, cur_y, c3_x + 3, cur_y + laws_h], fill=AMBER_ACCENT)
draw.text((c3_x + 12, cur_y + 9), "ANTI-ENTROPY: THE 3 DEFENSIVE LAWS", font=f_body_bold, fill=TEXT_WHITE)
draw.text((c3_x + 12, cur_y + 29), "Loops fail silently: silent death, zero output, and token waste.", font=f_body, fill=TEXT_MUTED)

laws = [
    {
        "num": "LAW I // PRE-FLIGHT CHECK",
        "color": CYAN_ACCENT,
        "desc": "Before running the loop, verify the health of the previous run. If the last state was corrupted, uncommitted, or empty, abort immediately and alert."
    },
    {
        "num": "LAW II // ATOMIC ROLLBACK",
        "color": AMBER_ACCENT,
        "desc": "Never ship half-broken state. If an agent crashes midway through a batch, roll back all disk writes to the last known good commit."
    },
    {
        "num": "LAW III // BE LOUD ON FAILURE",
        "color": GREEN_ACCENT,
        "desc": "Silent loops breed systemic debt. Any unhandled exception or failed verification MUST trigger an immediate webhook, Slack, or email alert."
    }
]

ly = cur_y + 54
for law in laws:
    draw.text((c3_x + 12, ly), law["num"], font=f_mono_bold, fill=law["color"])
    draw.line([(c3_x + 12, ly + 16), (c3_x + c3_w - 12, ly + 16)], fill=PANEL_BORDER, width=1)
    ly += 22
    ly = draw_wrapped_text(draw, c3_x + 14, ly, law["desc"], f_body, TEXT_MUTED, max_width=c3_w - 28, line_height=18)
    ly += 16

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
print(f"Refined banners saved: {out_png}, {out_jpg}, {out_webp}")
