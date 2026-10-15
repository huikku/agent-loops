#!/usr/bin/env python3
"""generate_mcp_diagram.py: Generates the future aerospace-styled widescreen diagram for
Model Context Protocol (MCP) Subsystem Connectors & API Translation Layer.
Aesthetic: Future aerospace avionics, DIN typography, matte slate palette.
"""
from PIL import Image, ImageDraw, ImageFont

font_dir = "/tmp/aerospace_fonts"
din_bold = f"{font_dir}/D-DIN-Bold.ttf"
din_regular = f"{font_dir}/D-DIN.ttf"
din_exp = f"{font_dir}/D-DINExp-Bold.ttf"
mono_bold = f"{font_dir}/JetBrainsMono-Bold.ttf"
mono_reg = f"{font_dir}/JetBrainsMono-Regular.ttf"

# Colors - Future Aerospace Palette
BG_COLOR = (15, 18, 23)          # Matte Charcoal Slate
PANEL_BG = (22, 27, 34)          # Dark Industrial Basalt
PANEL_SUB = (28, 34, 43)         # Sub-box fill
PANEL_BORDER = (46, 56, 70)      # Hairline Steel
TEXT_WHITE = (248, 250, 252)     # Signal White
TEXT_CREAM = (226, 232, 240)     # Off-white
TEXT_MUTED = (148, 163, 184)     # Industrial Slate
TEXT_DIM = (100, 115, 135)       # Hairline Grey
AMBER_ACCENT = (245, 131, 39)    # Status Amber
AMBER_BG = (45, 26, 16)          # Deep amber badge background
AMBER_BORDER = (195, 95, 25)
CYAN_ACCENT = (56, 189, 248)     # Telemetry Cyan
GREEN_ACCENT = (52, 211, 153)    # System Online Green

W, H = 1600, 920
img = Image.new("RGB", (W, H), BG_COLOR)
draw = ImageDraw.Draw(img)

# Load Fonts
f_main_title = ImageFont.truetype(din_exp, 50)
f_sub_title = ImageFont.truetype(din_bold, 19)
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

# --- Framing & Grid ---
draw.rectangle([14, 14, W - 15, H - 15], outline=PANEL_BORDER, width=1)
draw.rectangle([18, 18, W - 19, H - 19], outline=(30, 36, 45), width=1)

corners = [(14, 14, 1, 1), (W - 15, 14, -1, 1), (14, H - 15, 1, -1), (W - 15, H - 15, -1, -1)]
for cx, cy, dx, dy in corners:
    draw.line([(cx, cy), (cx + 25 * dx, cy)], fill=CYAN_ACCENT, width=3)
    draw.line([(cx, cy), (cx + 25 * dy, cy)], fill=CYAN_ACCENT, width=3)

draw_crosshair(draw, 50, 50)
draw_crosshair(draw, W - 50, 50)
draw_crosshair(draw, 50, H - 50)
draw_crosshair(draw, W - 50, H - 50)

# --- Header Telemetry ---
draw_hazard_stripe(draw, 35, 30, 48, 16)
draw_tracked_text(draw, 95, 31, "FUTURE AEROSPACE // MODEL CONTEXT PROTOCOL (MCP) // AVIONICS BUS REF 180286-MCP", f_micro, TEXT_MUTED, spacing=2)

status_w, status_h = 240, 24
status_x = W - 35 - status_w
draw.rectangle([status_x, 26, status_x + status_w, 26 + status_h], fill=AMBER_BG, outline=AMBER_BORDER, width=1)
draw.ellipse([status_x + 10, 34, status_x + 18, 42], fill=GREEN_ACCENT)
draw.text((status_x + 26, 30), "CONNECTOR BUS: ACTIVE", font=f_badge, fill=AMBER_ACCENT)

draw.line([(35, 58), (W - 35, 58)], fill=PANEL_BORDER, width=1)

# --- Title Block ---
draw.text((35, 68), "MODEL CONTEXT PROTOCOL (MCP)", font=f_main_title, fill=TEXT_WHITE)
draw_tracked_text(draw, 37, 126, "BUILDING AI CONNECTORS ON TOP OF APIS // ZERO TRIAL-AND-ERROR NOISE", f_sub_title, CYAN_ACCENT, spacing=2)

desc_str = "The adapter specification: bridging autonomous loops and backend APIs via metadata, tools, enterprise SSO, and stored translation caveats."
draw.text((37, 154), desc_str, font=f_body, fill=TEXT_MUTED)

# Analogy Banner
quote_x, quote_y, quote_w, quote_h = 35, 180, W - 70, 34
draw.rectangle([quote_x, quote_y, quote_x + quote_w, quote_y + quote_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
draw.rectangle([quote_x, quote_y, quote_x + 4, quote_y + quote_h], fill=AMBER_ACCENT)
quote_text = "\"An API is like walking into a dark house where all the lights are off. An MCP turns the lights on.\" — TJ Muehleman & Jonathan Nesbitt"
draw.text((quote_x + 16, quote_y + 9), quote_text, font=f_mono_bold, fill=TEXT_CREAM)
meta_text = "STANDARD CO AI SERIES // JONATHAN NESBITT // TJ MUEHLEMAN"
draw.text((quote_x + quote_w - 380, quote_y + 10), meta_text, font=f_micro, fill=AMBER_ACCENT)

# --- Three Columns ---
col_y = 226
col_w = 496
col_h = 632
col_gap = 21

cols = [
    (35, "01 // THE ADAPTER PARADIGM", "WHY BUILD AN MCP ON TOP OF AN API?", CYAN_ACCENT),
    (35 + col_w + col_gap, "02 // INFRASTRUCTURE & AUTH", "LOCAL VS. WEB MCP & ENTERPRISE SSO", GREEN_ACCENT),
    (35 + (col_w + col_gap) * 2, "03 // ACCELERATION LAYER", "THE TRANSLATION & CAVEAT LAYER", AMBER_ACCENT),
]

for idx, (cx, badge_text, title_text, accent_color) in enumerate(cols):
    draw.rectangle([cx, col_y, cx + col_w, col_y + col_h], fill=PANEL_BG, outline=PANEL_BORDER, width=1)
    tab_h = 44
    draw.rectangle([cx, col_y, cx + col_w, col_y + tab_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.rectangle([cx, col_y, cx + 4, col_y + tab_h], fill=accent_color)
    draw.text((cx + 14, col_y + 6), badge_text, font=f_badge, fill=accent_color)
    draw.text((cx + 14, col_y + 22), title_text, font=f_col_hdr, fill=TEXT_WHITE)

# ------------------------------------------------------------------------------
# COLUMN 1: THE ADAPTER PARADIGM
# ------------------------------------------------------------------------------
c1_x = 35 + 16
c1_w = col_w - 32
c1_y = col_y + 54

c1_boxes = [
    {
        "title": "CONVERSATIONAL EXPLORATION",
        "tag": "ZERO CURL OVERHEAD",
        "color": CYAN_ACCENT,
        "bullets": [
            "• Domain experts know their data but don't know API clients",
            "• Plain English questions resolve to exact underlying endpoints",
            "• Generates production cURL/Python integration code on demand"
        ]
    },
    {
        "title": "CROSS-ENDPOINT DYNAMIC JOINS",
        "tag": "ZERO BACKEND REFACTOR",
        "color": GREEN_ACCENT,
        "bullets": [
            "• Agent correlates data across disparate, unlinked endpoints",
            "• Performs client-side table joins that do not exist in the API",
            "• Discovers rich insights without waiting for new backend resolvers"
        ]
    },
    {
        "title": "THIN ADAPTER & READ-ONLY BY DESIGN",
        "tag": "INHERITED RBAC",
        "color": AMBER_ACCENT,
        "bullets": [
            "• Separate micro-service: proxies queries directly through API",
            "• No direct database connection needed; avoids soft-delete bypass",
            "• Read-only default prevents accidental hallucinated writes"
        ]
    }
]

cur_y = c1_y
for b in c1_boxes:
    box_h = 176
    draw.rectangle([c1_x, cur_y, c1_x + c1_w, cur_y + box_h], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
    draw.rectangle([c1_x, cur_y, c1_x + 3, cur_y + box_h], fill=b["color"])
    draw.text((c1_x + 12, cur_y + 9), b["title"], font=f_body_bold, fill=TEXT_WHITE)
    draw.text((c1_x + c1_w - 140, cur_y + 10), b["tag"], font=f_micro, fill=b["color"])
    draw.line([(c1_x + 12, cur_y + 26), (c1_x + c1_w - 12, cur_y + 26)], fill=PANEL_BORDER, width=1)
    
    by = cur_y + 38
    for bullet in b["bullets"]:
        draw.text((c1_x + 14, by), bullet, font=f_body, fill=TEXT_MUTED)
        by += 34
    cur_y += box_h + 12

# ------------------------------------------------------------------------------
# COLUMN 2: INFRASTRUCTURE & AUTH
# ------------------------------------------------------------------------------
c2_x = 35 + col_w + col_gap + 16
c2_w = col_w - 32
c2_y = col_y + 54

cur_y = c2_y

# Local vs Web
draw.rectangle([c2_x, cur_y, c2_x + c2_w, cur_y + 258], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
draw.rectangle([c2_x, cur_y, c2_x + 3, cur_y + 258], fill=GREEN_ACCENT)
draw.text((c2_x + 12, cur_y + 9), "DEPLOYMENT ARCHITECTURE: LOCAL VS. WEB MCP", font=f_body_bold, fill=TEXT_WHITE)
draw.line([(c2_x + 12, cur_y + 26), (c2_x + c2_w - 12, cur_y + 26)], fill=PANEL_BORDER, width=1)

deploy_items = [
    ("LOCAL MCP (STDIO TRANSPORT):", [
        "• Runs on local CLI / Docker process; zero hosting cost",
        "• Ideal for initial authoring and single-developer workflows",
        "• Risk: process death, environment resets, local token expiry"
    ]),
    ("REMOTE / WEB MCP (SSE TRANSPORT):", [
        "• Hosted on Vercel, Fly.io, or AWS with public HTTPS endpoint",
        "• Zero-friction client setup: paste URL in Claude/ChatGPT settings",
        "• Multi-tenant & shared across entire enterprise organization"
    ])
]

dy = cur_y + 34
for dhdr, dbullets in deploy_items:
    draw.text((c2_x + 12, dy), dhdr, font=f_mono_bold, fill=CYAN_ACCENT)
    dy += 18
    for db in dbullets:
        draw.text((c2_x + 14, dy), db, font=f_body, fill=TEXT_MUTED)
        dy += 18
    dy += 6

cur_y += 258 + 12

# Enterprise Auth
draw.rectangle([c2_x, cur_y, c2_x + c2_w, cur_y + 282], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
draw.rectangle([c2_x, cur_y, c2_x + 3, cur_y + 282], fill=AMBER_ACCENT)
draw.text((c2_x + 12, cur_y + 9), "AUTHENTICATION & PERMISSION INHERITANCE", font=f_body_bold, fill=TEXT_WHITE)
draw.line([(c2_x + 12, cur_y + 26), (c2_x + c2_w - 12, cur_y + 26)], fill=PANEL_BORDER, width=1)

auth_items = [
    ("1. CORPORATE IDENTITY PROVIDERS (SSO / OAUTH2):",
     "Connectors trigger browser SSO redirect (Azure AD, Google). Users authenticate once and inherit their exact tenant, country, or department access rights."),
    ("2. SELF-HOSTED OAUTH2 (DOORKEEPER / DEVISE):",
     "For internal apps without external IdPs, run a scoped OAuth2 bearer token provider directly inside the existing codebase."),
    ("3. API RATE-LIMITING & ZERO PRIVILEGE ESCALATION:",
     "MCP proxies the authenticated user's bearer token directly. Users cannot view records outside their existing API permissions.")
]

ay = cur_y + 34
for ahdr, adesc in auth_items:
    draw.text((c2_x + 12, ay), ahdr, font=f_mono_bold, fill=AMBER_ACCENT)
    ay += 17
    ay = draw_wrapped_text(draw, c2_x + 14, ay, adesc, f_body, TEXT_MUTED, max_width=c2_w - 28, line_height=17)
    ay += 8

# ------------------------------------------------------------------------------
# COLUMN 3: THE TRANSLATION & CAVEAT LAYER
# ------------------------------------------------------------------------------
c3_x = 35 + (col_w + col_gap) * 2 + 16
c3_w = col_w - 32
c3_y = col_y + 54

cur_y = c3_y

# Caveat Concept
draw.rectangle([c3_x, cur_y, c3_x + c3_w, cur_y + 268], fill=PANEL_SUB, outline=AMBER_BORDER, width=1)
draw.rectangle([c3_x, cur_y, c3_x + 4, cur_y + 268], fill=AMBER_ACCENT)
draw.text((c3_x + 12, cur_y + 10), "CLIFF NOTES FOR THE CODEBASE: THE CAVEAT LAYER", font=f_body_bold, fill=TEXT_WHITE)
draw.text((c3_x + 12, cur_y + 30), "Every real API has unwritten quirks and edge cases:", font=f_body, fill=TEXT_MUTED)

caveat_points = [
    ("• THE SILENT TRIAL-AND-ERROR TRAP:", "Unguided agents issue 10–15 exploratory API requests trying to discover quirks (hidden row ceilings, unexpected 500s)."),
    ("• STORED CAVEAT DICTIONARY (api_caveats.json):", "Stores documented vs. safe limits, mandatory filter pairs, and date encoding quirks directly in the MCP."),
    ("• FIRST-ATTEMPT ACCURACY (>80% NOISE REDUCTION):", "The MCP server automatically applies safe clamps and required filters before hitting the API.")
]

cpy = cur_y + 54
for chdr, cdesc in caveat_points:
    draw.text((c3_x + 12, cpy), chdr, font=f_mono_bold, fill=CYAN_ACCENT)
    cpy += 17
    cpy = draw_wrapped_text(draw, c3_x + 14, cpy, cdesc, f_body, TEXT_MUTED, max_width=c3_w - 28, line_height=17)
    cpy += 6

cur_y += 268 + 12

# Maintenance & Re-probing
draw.rectangle([c3_x, cur_y, c3_x + c3_w, cur_y + 272], fill=PANEL_SUB, outline=PANEL_BORDER, width=1)
draw.rectangle([c3_x, cur_y, c3_x + 3, cur_y + 272], fill=GREEN_ACCENT)
draw.text((c3_x + 12, cur_y + 9), "MAINTENANCE & CONTINUOUS RE-PROBING", font=f_body_bold, fill=TEXT_WHITE)
draw.line([(c3_x + 12, cur_y + 26), (c3_x + c3_w - 12, cur_y + 26)], fill=PANEL_BORDER, width=1)

maint_bullets = [
    ("AUTOMATED ROUTE AUDITING:",
     "When backend APIs add endpoints or alter schemas, an autonomous agent audits routes and regenerates tool definitions."),
    ("REGRESSION CI TESTS:",
     "Automated integration suites execute every MCP tool against staging APIs to certify zero breaking changes."),
    ("METADATA SYNCHRONIZATION:",
     "Ensures parameter documentation and caveat rules remain in exact 1:1 sync with production serializers.")
]

my = cur_y + 34
for mhdr, mdesc in maint_bullets:
    draw.text((c3_x + 12, my), mhdr, font=f_mono_bold, fill=GREEN_ACCENT)
    my += 17
    my = draw_wrapped_text(draw, c3_x + 14, my, mdesc, f_body, TEXT_MUTED, max_width=c3_w - 28, line_height=17)
    my += 8

# --- Bottom Telemetry Bar ---
foot_y = H - 38
draw.line([(35, foot_y), (W - 35, foot_y)], fill=PANEL_BORDER, width=1)
draw_tracked_text(draw, 35, foot_y + 10, "DESIGN SYSTEM: FUTURE AEROSPACE HUD // DIN TECHNICAL TYPOGRAPHY", f_micro, TEXT_DIM, spacing=2)
draw.text((640, foot_y + 10), "ALIENROBOT.COM // MCP CONNECTOR SPECIFICATION", font=f_micro, fill=CYAN_ACCENT)

repo_str = "PUBLIC REPOSITORY: GITHUB.COM/HUIKKU/AGENT-LOOPS"
repo_w = measure_tracked_text(repo_str, f_micro, spacing=1)
draw_tracked_text(draw, W - 35 - repo_w, foot_y + 10, repo_str, f_micro, AMBER_ACCENT, spacing=1)

out_png = "/home/john/code/agent-loops/assets/mcp-architecture.png"
out_jpg = "/home/john/code/agent-loops/assets/mcp-architecture.jpg"
out_webp = "/home/john/code/agent-loops/assets/mcp-architecture.webp"

img.save(out_png, "PNG")
img.save(out_jpg, "JPEG", quality=95)
img.save(out_webp, "WEBP", quality=95)
print(f"Generated MCP diagrams: {out_png}, {out_jpg}, {out_webp}")

