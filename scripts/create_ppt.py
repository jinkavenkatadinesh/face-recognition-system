"""
Generate a professional PowerPoint presentation for the Face Recognition System project.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
import os

# =============================================================================
# Theme colors
# =============================================================================
BG_DARK      = RGBColor(0x0F, 0x17, 0x2A)   # deep navy
BG_CARD      = RGBColor(0x16, 0x21, 0x3E)   # card background
ACCENT       = RGBColor(0x00, 0xD2, 0xFF)   # cyan accent
ACCENT2      = RGBColor(0x7C, 0x3A, 0xED)   # purple accent
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY   = RGBColor(0xB0, 0xBE, 0xC5)
GREEN        = RGBColor(0x00, 0xE6, 0x76)
ORANGE       = RGBColor(0xFF, 0x9F, 0x43)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height


# =============================================================================
# Helper functions
# =============================================================================
def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill_color, border_color=None):
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=18,
                 color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_frame(slide, left, top, width, height, items, font_size=16,
                     color=WHITE, bullet_color=ACCENT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(8)
        # bullet character
        run_b = p.add_run()
        run_b.text = "▸ "
        run_b.font.size = Pt(font_size)
        run_b.font.color.rgb = bullet_color
        run_b.font.name = "Calibri"
        # text
        run_t = p.add_run()
        run_t.text = item
        run_t.font.size = Pt(font_size)
        run_t.font.color.rgb = color
        run_t.font.name = "Calibri"
    return txBox


def add_accent_bar(slide, left, top, width, height, color=ACCENT):
    from pptx.enum.shapes import MSO_SHAPE
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    return bar


def add_section_header(slide, title, subtitle=None):
    add_accent_bar(slide, Inches(0.8), Inches(0.6), Inches(0.15), Inches(0.55), ACCENT)
    add_text_box(slide, Inches(1.15), Inches(0.5), Inches(10), Inches(0.7),
                 title, font_size=32, color=WHITE, bold=True)
    if subtitle:
        add_text_box(slide, Inches(1.15), Inches(1.15), Inches(10), Inches(0.4),
                     subtitle, font_size=16, color=LIGHT_GRAY)


# =============================================================================
# SLIDE 1 – Title
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
set_slide_bg(slide, BG_DARK)

# Decorative accent circles
from pptx.enum.shapes import MSO_SHAPE
circle1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.5), Inches(-1), Inches(4), Inches(4))
circle1.fill.solid()
circle1.fill.fore_color.rgb = RGBColor(0x00, 0xD2, 0xFF)
circle1.fill.fore_color.brightness = 0.85  # faded
circle1.line.fill.background()

circle2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-1.5), Inches(5), Inches(3.5), Inches(3.5))
circle2.fill.solid()
circle2.fill.fore_color.rgb = ACCENT2
circle2.line.fill.background()

add_accent_bar(slide, Inches(1.5), Inches(2.6), Inches(3), Inches(0.08), ACCENT)

add_text_box(slide, Inches(1.5), Inches(2.8), Inches(10), Inches(1.2),
             "Face Recognition System", font_size=48, color=WHITE, bold=True)
add_text_box(slide, Inches(1.5), Inches(4.0), Inches(9), Inches(0.8),
             "Intelligent Face Detection using Haar Cascade & MTCNN",
             font_size=22, color=LIGHT_GRAY)
add_text_box(slide, Inches(1.5), Inches(5.2), Inches(5), Inches(0.5),
             "Python  •  OpenCV  •  TensorFlow  •  MTCNN",
             font_size=14, color=ACCENT)

# =============================================================================
# SLIDE 2 – Project Overview
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Project Overview")

add_text_box(slide, Inches(1.15), Inches(1.8), Inches(10.5), Inches(1.0),
             "This project implements a face detection pipeline that processes images from a dataset, "
             "detects human faces using two different approaches — Haar Cascade (classical) and MTCNN "
             "(deep learning) — and saves annotated output images with bounding boxes drawn around "
             "detected faces.",
             font_size=17, color=LIGHT_GRAY)

# Key objectives cards
objectives = [
    ("🎯", "Objective", "Detect and localize faces\nin static images accurately"),
    ("⚙️", "Approach", "Compare classical (Haar)\nvs deep learning (MTCNN)"),
    ("📂", "Pipeline", "Raw images → Detection\n→ Annotated output"),
    ("🧪", "Validation", "Visual verification of\nbounding box accuracy"),
]

card_w = Inches(2.6)
card_h = Inches(2.5)
start_x = Inches(0.9)
gap = Inches(0.3)

for idx, (icon, title, desc) in enumerate(objectives):
    x = start_x + idx * (card_w + gap)
    y = Inches(3.5)
    card = add_shape(slide, x, y, card_w, card_h, BG_CARD, border_color=RGBColor(0x2A, 0x3A, 0x5C))

    add_text_box(slide, x + Inches(0.3), y + Inches(0.25), card_w - Inches(0.6), Inches(0.5),
                 icon, font_size=28, color=ACCENT, alignment=PP_ALIGN.LEFT)
    add_text_box(slide, x + Inches(0.3), y + Inches(0.75), card_w - Inches(0.6), Inches(0.4),
                 title, font_size=18, color=WHITE, bold=True)
    add_text_box(slide, x + Inches(0.3), y + Inches(1.25), card_w - Inches(0.6), Inches(1.0),
                 desc, font_size=14, color=LIGHT_GRAY)

# =============================================================================
# SLIDE 3 – Technology Stack
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Technology Stack")

techs = [
    ("Python 3.x",     "Core programming language for all scripts", ACCENT),
    ("OpenCV",         "Image processing, Haar Cascade face detection, I/O", RGBColor(0x4F, 0xC3, 0xF7)),
    ("TensorFlow",     "Backend framework powering the MTCNN model", ORANGE),
    ("MTCNN",          "Multi-task CNN for robust face detection", ACCENT2),
    ("NumPy",          "Array operations and numerical computations", GREEN),
]

for idx, (name, desc, col) in enumerate(techs):
    y = Inches(1.9) + idx * Inches(0.95)
    # color dot
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.3), y + Inches(0.15), Inches(0.22), Inches(0.22))
    dot.fill.solid()
    dot.fill.fore_color.rgb = col
    dot.line.fill.background()
    add_text_box(slide, Inches(1.75), y, Inches(3), Inches(0.5),
                 name, font_size=20, color=WHITE, bold=True)
    add_text_box(slide, Inches(4.8), y + Inches(0.05), Inches(7), Inches(0.5),
                 desc, font_size=16, color=LIGHT_GRAY)

# =============================================================================
# SLIDE 4 – Project Structure
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Project Structure", "Directory layout and file organization")

tree_lines = [
    ("FaceRecognitionProject/", 0, True),
    ("├── dataset/", 1, True),
    ("│   ├── raw/               ← input images", 2, False),
    ("│   ├── output/            ← annotated results", 2, False),
    ("│   └── test.jpg           ← setup test image", 2, False),
    ("├── models/                ← saved models (future)", 1, True),
    ("├── scripts/", 1, True),
    ("│   ├── face_detection.py  ← Haar Cascade detector", 2, False),
    ("│   ├── mtcnn_detection.py ← MTCNN detector", 2, False),
    ("│   └── test_setup.py      ← environment verifier", 2, False),
    ("└── venv/                  ← virtual environment", 1, True),
]

tree_box = add_shape(slide, Inches(1.0), Inches(1.9), Inches(11), Inches(5.0),
                     BG_CARD, border_color=RGBColor(0x2A, 0x3A, 0x5C))

for idx, (line, indent, is_dir) in enumerate(tree_lines):
    y = Inches(2.1) + idx * Inches(0.42)
    x = Inches(1.4) + indent * Inches(0.3)
    col = ACCENT if is_dir else LIGHT_GRAY
    fs = 16 if is_dir else 15
    add_text_box(slide, x, y, Inches(10), Inches(0.4),
                 line, font_size=fs, color=col, bold=is_dir, font_name="Consolas")

# =============================================================================
# SLIDE 5 – Haar Cascade Detection
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Haar Cascade Detection", "Classical machine learning approach (face_detection.py)")

# Left side – How it works
add_text_box(slide, Inches(1.15), Inches(1.8), Inches(5), Inches(0.4),
             "How It Works", font_size=20, color=ACCENT, bold=True)

add_bullet_frame(slide, Inches(1.15), Inches(2.3), Inches(5.5), Inches(3.5), [
    "Uses pre-trained Haar feature-based cascade classifier",
    "Converts image to grayscale for processing",
    "Applies histogram equalization for contrast enhancement",
    "detectMultiScale with scaleFactor=1.05, minNeighbors=2",
    "Draws green bounding boxes on detected faces",
    "Saves annotated images to output folder",
], font_size=15)

# Right side – Key parameters card
card = add_shape(slide, Inches(7.2), Inches(1.8), Inches(5.2), Inches(4.8),
                 BG_CARD, border_color=ACCENT)
add_text_box(slide, Inches(7.5), Inches(2.0), Inches(4.5), Inches(0.4),
             "⚙  Key Parameters", font_size=18, color=ACCENT, bold=True)

params = [
    ("scaleFactor", "1.05", "More sensitive multi-scale scanning"),
    ("minNeighbors", "2", "Less strict – reduces missed detections"),
    ("minSize", "(20, 20)", "Minimum face size in pixels"),
]
for idx, (param, val, desc) in enumerate(params):
    y = Inches(2.6) + idx * Inches(1.3)
    add_text_box(slide, Inches(7.5), y, Inches(4.5), Inches(0.35),
                 param, font_size=16, color=WHITE, bold=True, font_name="Consolas")
    add_text_box(slide, Inches(7.5), y + Inches(0.35), Inches(4.5), Inches(0.3),
                 f"Value: {val}", font_size=14, color=GREEN, font_name="Consolas")
    add_text_box(slide, Inches(7.5), y + Inches(0.7), Inches(4.5), Inches(0.35),
                 desc, font_size=13, color=LIGHT_GRAY)

# =============================================================================
# SLIDE 6 – MTCNN Detection
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "MTCNN Detection", "Deep learning approach (mtcnn_detection.py)")

add_text_box(slide, Inches(1.15), Inches(1.8), Inches(5), Inches(0.4),
             "How It Works", font_size=20, color=ACCENT2, bold=True)

add_bullet_frame(slide, Inches(1.15), Inches(2.3), Inches(5.5), Inches(3.5), [
    "Multi-task Cascaded Convolutional Network",
    "Three-stage cascade: P-Net → R-Net → O-Net",
    "Converts BGR to RGB (required by MTCNN)",
    "Returns bounding boxes + facial landmarks",
    "More accurate than Haar on varied poses/lighting",
    "Powered by TensorFlow backend",
], font_size=15, bullet_color=ACCENT2)

# Right side – Pipeline stages
card = add_shape(slide, Inches(7.2), Inches(1.8), Inches(5.2), Inches(4.8),
                 BG_CARD, border_color=ACCENT2)
add_text_box(slide, Inches(7.5), Inches(2.0), Inches(4.5), Inches(0.4),
             "🔗  Three-Stage Pipeline", font_size=18, color=ACCENT2, bold=True)

stages = [
    ("P-Net", "Proposal Network", "Generates candidate face\nregions at multiple scales"),
    ("R-Net", "Refine Network", "Filters false positives\nand refines bounding boxes"),
    ("O-Net", "Output Network", "Final detection with facial\nlandmark localization"),
]
for idx, (abbr, name, desc) in enumerate(stages):
    y = Inches(2.7) + idx * Inches(1.35)
    # stage badge
    badge = add_shape(slide, Inches(7.5), y, Inches(1.0), Inches(0.4), ACCENT2)
    add_text_box(slide, Inches(7.5), y, Inches(1.0), Inches(0.4),
                 abbr, font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(8.7), y - Inches(0.02), Inches(3.5), Inches(0.35),
                 name, font_size=15, color=WHITE, bold=True)
    add_text_box(slide, Inches(8.7), y + Inches(0.35), Inches(3.5), Inches(0.7),
                 desc, font_size=13, color=LIGHT_GRAY)

# =============================================================================
# SLIDE 7 – Comparison: Haar vs MTCNN
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Haar Cascade vs MTCNN", "Comparison of the two detection approaches")

# Table header
headers = ["Criteria", "Haar Cascade", "MTCNN"]
col_x = [Inches(1.2), Inches(4.8), Inches(9.0)]
col_w = [Inches(3.4), Inches(4.0), Inches(3.8)]

header_y = Inches(2.0)
for i, hdr in enumerate(headers):
    bar = add_shape(slide, col_x[i], header_y, col_w[i], Inches(0.55), ACCENT)
    add_text_box(slide, col_x[i] + Inches(0.2), header_y + Inches(0.05),
                 col_w[i] - Inches(0.4), Inches(0.45),
                 hdr, font_size=16, color=BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)

rows = [
    ("Speed",          "⚡ Very Fast",              "🐢 Slower (GPU helps)"),
    ("Accuracy",       "Moderate",                  "✅ High"),
    ("Pose Tolerance", "Frontal faces only",        "Multi-angle support"),
    ("Lighting",       "Sensitive to variations",    "Robust"),
    ("Landmarks",      "❌ Not available",           "✅ 5-point landmarks"),
    ("Dependencies",   "OpenCV only",               "TensorFlow + MTCNN"),
    ("Best For",       "Real-time / resource-limited", "High accuracy needs"),
]

for row_idx, (crit, haar, mtcnn) in enumerate(rows):
    y = Inches(2.7) + row_idx * Inches(0.6)
    bg = BG_CARD if row_idx % 2 == 0 else BG_DARK
    for i, text in enumerate([crit, haar, mtcnn]):
        cell = add_shape(slide, col_x[i], y, col_w[i], Inches(0.55), bg)
        col = WHITE if i == 0 else LIGHT_GRAY
        if i == 0:
            bld = True
        else:
            bld = False
        add_text_box(slide, col_x[i] + Inches(0.2), y + Inches(0.08),
                     col_w[i] - Inches(0.4), Inches(0.45),
                     text, font_size=14, color=col, bold=bld, alignment=PP_ALIGN.CENTER)

# =============================================================================
# SLIDE 8 – Processing Pipeline
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Processing Pipeline", "End-to-end workflow from input to output")

steps = [
    ("01", "Load Images", "Read .jpg/.png files\nfrom dataset/raw/", ACCENT),
    ("02", "Preprocess", "Grayscale conversion\n& histogram equalization", RGBColor(0x4F, 0xC3, 0xF7)),
    ("03", "Detect Faces", "Run Haar or MTCNN\ndetection algorithm", ACCENT2),
    ("04", "Annotate", "Draw bounding boxes\naround detected faces", ORANGE),
    ("05", "Save Output", "Write annotated images\nto dataset/output/", GREEN),
]

step_w = Inches(2.1)
step_h = Inches(3.2)
start_x = Inches(0.65)
gap = Inches(0.25)

for idx, (num, title, desc, col) in enumerate(steps):
    x = start_x + idx * (step_w + gap)
    y = Inches(2.2)

    # Card
    card = add_shape(slide, x, y, step_w, step_h, BG_CARD, border_color=col)

    # Number badge
    badge = add_shape(slide, x + Inches(0.65), y + Inches(0.3), Inches(0.8), Inches(0.8), col)
    add_text_box(slide, x + Inches(0.65), y + Inches(0.35), Inches(0.8), Inches(0.7),
                 num, font_size=28, color=BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)

    add_text_box(slide, x + Inches(0.15), y + Inches(1.3), step_w - Inches(0.3), Inches(0.4),
                 title, font_size=17, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.15), y + Inches(1.8), step_w - Inches(0.3), Inches(1.0),
                 desc, font_size=13, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

    # Arrow between steps
    if idx < len(steps) - 1:
        arrow_x = x + step_w + Inches(0.02)
        add_text_box(slide, arrow_x, Inches(3.5), Inches(0.25), Inches(0.4),
                     "›", font_size=28, color=col, bold=True, alignment=PP_ALIGN.CENTER)

# =============================================================================
# SLIDE 9 – Dataset Details
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Dataset Details", "Input images and processed outputs")

# Raw images card
card = add_shape(slide, Inches(1.0), Inches(1.9), Inches(5.3), Inches(5.0),
                 BG_CARD, border_color=ACCENT)
add_text_box(slide, Inches(1.3), Inches(2.1), Inches(4.5), Inches(0.4),
             "📁  Raw Input (dataset/raw/)", font_size=18, color=ACCENT, bold=True)
add_bullet_frame(slide, Inches(1.3), Inches(2.7), Inches(4.7), Inches(3.5), [
    "img1.jpg — 11.6 KB",
    "img2.jpg — 11.1 KB",
    "img3.jpg — 13.4 KB",
    "3 sample images for face detection testing",
    "Supports .jpg, .jpeg, and .png formats",
], font_size=15)

# Output images card
card = add_shape(slide, Inches(7.0), Inches(1.9), Inches(5.3), Inches(5.0),
                 BG_CARD, border_color=GREEN)
add_text_box(slide, Inches(7.3), Inches(2.1), Inches(4.5), Inches(0.4),
             "📁  Output (dataset/output/)", font_size=18, color=GREEN, bold=True)
add_bullet_frame(slide, Inches(7.3), Inches(2.7), Inches(4.7), Inches(3.5), [
    "img1.jpg — 25.0 KB (annotated)",
    "img2.jpg — 22.5 KB (annotated)",
    "img3.jpg — 27.5 KB (annotated)",
    "Output files are larger due to drawn bounding boxes",
    "Same filenames, different directory",
], font_size=15, bullet_color=GREEN)

# =============================================================================
# SLIDE 10 – Environment Setup
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Environment Setup", "test_setup.py — verifying dependencies")

card = add_shape(slide, Inches(1.0), Inches(1.9), Inches(11.2), Inches(5.0),
                 BG_CARD, border_color=RGBColor(0x2A, 0x3A, 0x5C))

code_lines = [
    ("import", " cv2, numpy, tensorflow"),
    ("", ""),
    ("# Prints library versions"),
    ("print", "(\"OpenCV Version:\", cv2.__version__)"),
    ("print", "(\"NumPy Version:\", np.__version__)"),
    ("print", "(\"TensorFlow Version:\", tf.__version__)"),
    ("", ""),
    ("# Loads & displays test image"),
    ("image", " = cv2.imread(\"../dataset/test.jpg\")"),
    ("cv2.imshow", "(\"Test Image\", image)"),
]

add_text_box(slide, Inches(1.3), Inches(2.1), Inches(4), Inches(0.4),
             "⚙  Setup Verification Script", font_size=18, color=ACCENT, bold=True)

y_start = Inches(2.7)
for idx, line_data in enumerate(code_lines):
    y = y_start + idx * Inches(0.38)
    if len(line_data) == 2:
        kw, rest = line_data
        if kw and kw.startswith("#"):
            add_text_box(slide, Inches(1.6), y, Inches(10), Inches(0.35),
                         kw, font_size=14, color=LIGHT_GRAY, font_name="Consolas")
        elif kw:
            add_text_box(slide, Inches(1.6), y, Inches(10), Inches(0.35),
                         kw + rest, font_size=14, color=GREEN, font_name="Consolas")
    else:
        add_text_box(slide, Inches(1.6), y, Inches(10), Inches(0.35),
                     line_data[0], font_size=14, color=LIGHT_GRAY, font_name="Consolas")

# Purpose callout
add_text_box(slide, Inches(1.3), Inches(5.8), Inches(10), Inches(0.8),
             "Purpose: Ensure OpenCV, NumPy, and TensorFlow are installed correctly before running detection scripts.",
             font_size=15, color=ORANGE)

# =============================================================================
# SLIDE 11 – Future Enhancements
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)
add_section_header(slide, "Future Enhancements", "Potential improvements and next steps")

enhancements = [
    ("🧠", "Face Recognition", "Identify who the person is using embeddings (FaceNet, ArcFace)", ACCENT),
    ("🎥", "Real-Time Video", "Live webcam face detection and tracking using OpenCV VideoCapture", RGBColor(0x4F, 0xC3, 0xF7)),
    ("📊", "Model Training", "Train custom models on domain-specific datasets for improved accuracy", ACCENT2),
    ("☁️", "Cloud Deployment", "Deploy as a REST API using Flask/FastAPI for remote inference", ORANGE),
    ("💾", "Database Integration", "Store detected face data with metadata in SQLite/PostgreSQL", GREEN),
    ("📱", "Web Interface", "Build a browser-based UI for uploading images and viewing results", RGBColor(0xEC, 0x40, 0x7A)),
]

card_w = Inches(3.5)
card_h = Inches(2.0)
cols = 3
gap_x = Inches(0.35)
gap_y = Inches(0.3)

for idx, (icon, title, desc, col) in enumerate(enhancements):
    row = idx // cols
    c = idx % cols
    x = Inches(0.9) + c * (card_w + gap_x)
    y = Inches(1.9) + row * (card_h + gap_y)

    card = add_shape(slide, x, y, card_w, card_h, BG_CARD, border_color=col)
    add_text_box(slide, x + Inches(0.2), y + Inches(0.15), Inches(0.5), Inches(0.4),
                 icon, font_size=24, color=col)
    add_text_box(slide, x + Inches(0.7), y + Inches(0.15), card_w - Inches(0.9), Inches(0.35),
                 title, font_size=16, color=WHITE, bold=True)
    add_text_box(slide, x + Inches(0.2), y + Inches(0.65), card_w - Inches(0.4), Inches(1.1),
                 desc, font_size=13, color=LIGHT_GRAY)

# =============================================================================
# SLIDE 12 – Thank You
# =============================================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, BG_DARK)

# Decorative
circle1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-1), Inches(-1.5), Inches(5), Inches(5))
circle1.fill.solid()
circle1.fill.fore_color.rgb = ACCENT2
circle1.line.fill.background()

circle2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10), Inches(4.5), Inches(4.5), Inches(4.5))
circle2.fill.solid()
circle2.fill.fore_color.rgb = ACCENT
circle2.line.fill.background()

add_accent_bar(slide, Inches(4.5), Inches(2.8), Inches(4.3), Inches(0.08), ACCENT)
add_text_box(slide, Inches(1.5), Inches(3.0), Inches(10.3), Inches(1.2),
             "Thank You!", font_size=56, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.5), Inches(4.3), Inches(10.3), Inches(0.6),
             "Face Recognition System — Haar Cascade & MTCNN",
             font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.5), Inches(5.2), Inches(10.3), Inches(0.5),
             "Questions?",
             font_size=22, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)


# =============================================================================
# Save
# =============================================================================
output_path = os.path.join(os.path.dirname(__file__), "..", "Face_Recognition_Project.pptx")
prs.save(output_path)
print(f"\n[+] Presentation saved to: {os.path.abspath(output_path)}")
