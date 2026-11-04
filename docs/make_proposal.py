"""Generate a 2-page English project proposal PDF."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

doc = SimpleDocTemplate(
    "project_proposal.pdf",
    pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=15 * mm, bottomMargin=15 * mm,
)

ss = getSampleStyleSheet()

title = ParagraphStyle(
    "title", parent=ss["Title"], fontSize=15, leading=18, spaceAfter=2
)
subtitle = ParagraphStyle(
    "subtitle", parent=ss["Normal"], fontSize=9.5, leading=12,
    alignment=1, textColor=colors.HexColor("#555555"), spaceAfter=8
)
h = ParagraphStyle(
    "h", parent=ss["Heading2"], fontSize=11, leading=13,
    spaceBefore=8, spaceAfter=3, textColor=colors.HexColor("#1a3d5c")
)
body = ParagraphStyle(
    "body", parent=ss["Normal"], fontSize=9.2, leading=11.8,
    alignment=TA_JUSTIFY, spaceAfter=4
)
small = ParagraphStyle(
    "small", parent=ss["Normal"], fontSize=8.3, leading=10.5
)
cell = ParagraphStyle("cell", parent=small, fontSize=8.3, leading=10.2)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")

S = []

# ---------------------------------------------------------------- header
S.append(Paragraph(
    "Writing in the Air: Measuring and Mitigating Domain Shift "
    "in Handwritten Digit Recognition", title))
S.append(Paragraph(
    "Programming with Python, Fall 2026 &mdash; Course Project Proposal<br/>"
    "Group members: Name 1, Name 2, Name 3, Name 4", subtitle))

# ---------------------------------------------------------------- 1
S.append(Paragraph("1. Introduction and Problem Statement", h))
S.append(Paragraph(
    "Convolutional neural networks reach above 99% accuracy on the MNIST "
    "handwritten digit benchmark, which is often taken to mean the task is "
    "solved. In practice, a model deployed in the real world rarely sees the "
    "same kind of input it was trained on. This gap between training and "
    "deployment distributions is known as <i>domain shift</i>, and it is one "
    "of the most common reasons why machine learning systems that look "
    "excellent on paper fail once they are used.", body))
S.append(Paragraph(
    "This project studies domain shift on a concrete, self-collected example. "
    "We build a gesture-controlled virtual whiteboard: a webcam tracks the "
    "user's hand, an extended index finger draws, and a closed fist stops "
    "drawing. Digits written in mid-air differ systematically from MNIST "
    "digits &mdash; the stroke is thicker and of uneven width, the hand trembles, "
    "proportions are distorted, and the user cannot lift the pen, so unwanted "
    "connecting strokes appear. We quantify how much accuracy is lost on such "
    "data and determine which preprocessing and training techniques recover it.", body))
S.append(Paragraph(
    "<b>Research question.</b> How large is the accuracy drop when an "
    "MNIST-trained classifier is applied to digits written in the air, and "
    "which interventions &mdash; stroke normalisation, centre-of-mass alignment, "
    "training-time augmentation, or fine-tuning &mdash; close that gap most "
    "effectively?", body))

# ---------------------------------------------------------------- 2
S.append(Paragraph("2. Data", h))
S.append(Paragraph(
    "<b>Source domain.</b> MNIST (LeCun et al., 1998), 70,000 grayscale "
    "28&times;28 images, accessed through <font face='Courier'>torchvision</font>.", body))
S.append(Paragraph(
    "<b>Target domain (collected by us).</b> Each of the four group members "
    "writes 75&ndash;100 digits in the air using our whiteboard application, "
    "giving roughly 300&ndash;400 labelled images in total, stored together with "
    "the identity of the writer. Images are saved in raw form, without "
    "resizing, so that every preprocessing variant can be evaluated on "
    "identical source data. Members are instructed to write naturally rather "
    "than to imitate the MNIST style, since the point of the study is to "
    "capture the real difference between the two domains. This dataset is an "
    "original contribution and does not exist anywhere else.", body))

# ---------------------------------------------------------------- 3
S.append(Paragraph("3. Method", h))
S.append(Paragraph(
    "<b>Acquisition.</b> MediaPipe Hands returns 21 hand landmarks per frame. "
    "A finger counts as extended when its tip lies above its PIP joint; the "
    "resulting five-element state vector selects the drawing mode (index only "
    "&rarr; draw, fist &rarr; pause, open palm &rarr; clear). Raw fingertip positions "
    "are jittery, so the drawing point is smoothed over a short sliding "
    "window, and the camera image is mirrored horizontally to make the "
    "interaction intuitive.", body))
S.append(Paragraph(
    "<b>Classifier.</b> A compact CNN (three Conv&ndash;BatchNorm&ndash;ReLU&ndash;MaxPool "
    "blocks, dropout, one dense layer) trained on MNIST. A multinomial "
    "logistic regression on raw pixels serves as a baseline, establishing how "
    "much of the task is attributable to the convolutional architecture "
    "itself rather than to the data.", body))
S.append(Paragraph(
    "<b>Interventions.</b> Each is implemented as an independent, switchable "
    "pipeline step so that any combination can be evaluated: stroke-thickness "
    "normalisation by morphological operations; centre-of-mass alignment and "
    "aspect-preserving rescaling that reproduces the original MNIST "
    "normalisation procedure; training-time augmentation with random "
    "dilation, rotation, translation and elastic deformation; and fine-tuning "
    "on a held-out portion of our own data.", body))

# ---------------------------------------------------------------- 4
S.append(Paragraph("4. Experiments and Evaluation", h))
S.append(Paragraph(
    "The evaluation metrics are accuracy, macro-F1 and per-class F1, together "
    "with confusion matrices. Every configuration is run with three random "
    "seeds and reported as mean &plusmn; standard deviation, so that differences "
    "between variants can be distinguished from run-to-run noise.", body))

rows = [
    [Paragraph("Experiment", cellb), Paragraph("Purpose", cellb)],
    [Paragraph("Baseline vs. CNN on MNIST", cell),
     Paragraph("Establish source-domain performance and verify the training setup.", cell)],
    [Paragraph("MNIST model on our data, minimal preprocessing", cell),
     Paragraph("Measure the raw size of the domain gap &mdash; the central result.", cell)],
    [Paragraph("Ablation over preprocessing steps", cell),
     Paragraph("Isolate the contribution of stroke normalisation and of centring.", cell)],
    [Paragraph("Augmented training", cell),
     Paragraph("Test whether the gap can be closed without ever seeing target data.", cell)],
    [Paragraph("Fine-tuning on 70% of our data", cell),
     Paragraph("Upper bound: how much a small amount of in-domain data buys.", cell)],
    [Paragraph("Leave-one-writer-out", cell),
     Paragraph("Does the model generalise to a writing style it has not seen?", cell)],
]
t = Table(rows, colWidths=[62 * mm, 112 * mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#aab8c2")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
S.append(t)
S.append(Spacer(1, 4))
S.append(Paragraph(
    "<b>Visualisations.</b> Learning curves; confusion matrices for both "
    "domains; a bar chart of accuracy per ablation variant with error bars; "
    "side-by-side samples of the same digit from MNIST and from each writer; "
    "distributions of stroke thickness and image fill ratio across the two "
    "domains; and galleries of misclassified examples.", body))
S.append(Paragraph(
    "<b>Reproducibility.</b> All random seeds are fixed, library versions are "
    "pinned in <font face='Courier'>requirements.txt</font>, and every number "
    "quoted in the report is written to disk by the same script that produces "
    "the figures. No result is reported that the code does not generate.", body))

# ---------------------------------------------------------------- 5
S.append(Paragraph("5. Expected Outcome and Contribution", h))
S.append(Paragraph(
    "We expect a substantial accuracy drop on in-air digits relative to "
    "MNIST, with confusions concentrated in pairs whose distinction depends "
    "on fine stroke detail. We expect geometric normalisation to recover a "
    "noticeable part of the gap at zero training cost, augmentation to help "
    "further without requiring any target data, and fine-tuning on a small "
    "sample to perform best. The leave-one-writer-out experiment should "
    "indicate how much of the remaining error is writer-specific rather than "
    "domain-wide.", body))
S.append(Paragraph(
    "The contribution is not a new architecture but an empirical study on an "
    "original dataset: a quantified measurement of a practically relevant "
    "failure mode, and a ranking of mitigations by the accuracy each one "
    "actually recovers.", body))

# ---------------------------------------------------------------- 6
S.append(Paragraph("6. Tools, Division of Work and Schedule", h))
S.append(Paragraph(
    "<b>Libraries.</b> PyTorch and torchvision (model, data), OpenCV and "
    "MediaPipe (acquisition, image processing), NumPy, scikit-learn "
    "(baseline, metrics), Matplotlib (figures).", body))

rows2 = [
    [Paragraph("Member", cellb), Paragraph("Responsibility", cellb), Paragraph("Files", cellb)],
    [Paragraph("A", cell), Paragraph("Acquisition: hand tracking, gesture logic, smoothing, data-collection pipeline; live demo", cell),
     Paragraph("whiteboard.py, collect_data.py", cell)],
    [Paragraph("B", cell), Paragraph("Modelling: CNN architecture, training loop, baseline, fine-tuning", cell),
     Paragraph("model.py, train.py, config.py", cell)],
    [Paragraph("C", cell), Paragraph("Image processing and evaluation: normalisation, augmentation, metrics, ablation runs", cell),
     Paragraph("preprocessing.py, evaluate.py, ablation.py", cell)],
    [Paragraph("D", cell), Paragraph("Analysis, figures, cross-writer study, report and coordination", cell),
     Paragraph("analysis.py, report", cell)],
]
t2 = Table(rows2, colWidths=[20 * mm, 100 * mm, 54 * mm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#aab8c2")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
S.append(t2)
S.append(Spacer(1, 3))
S.append(Paragraph(
    "Data collection is performed jointly by all four members, which is what "
    "makes the cross-writer analysis possible. Interfaces between the modules "
    "are agreed before implementation begins, so the four parts can be "
    "developed in parallel and integrated at the end.", body))
S.append(Paragraph(
    "<b>Schedule.</b> Acquisition and MNIST training proceed in parallel on "
    "day one, followed by joint data collection; experiments and ablation on "
    "day two; report and presentation rehearsal on day three. Submission is "
    "due 13 November 2026.", body))

# ---------------------------------------------------------------- 7
S.append(Paragraph("7. References", h))
S.append(Paragraph(
    "[1] Y. LeCun, L. Bottou, Y. Bengio, P. Haffner. Gradient-based learning "
    "applied to document recognition. <i>Proceedings of the IEEE</i>, "
    "86(11):2278&ndash;2324, 1998.<br/>"
    "[2] F. Zhang et al. MediaPipe Hands: On-device Real-time Hand Tracking. "
    "arXiv:2006.10214, 2020.<br/>"
    "[3] A. Paszke et al. PyTorch: An Imperative Style, High-Performance Deep "
    "Learning Library. <i>NeurIPS</i>, 2019.<br/>"
    "[4] G. Bradski. The OpenCV Library. <i>Dr. Dobb's Journal of Software "
    "Tools</i>, 2000.<br/>"
    "[5] P. Simard, D. Steinkraus, J. Platt. Best Practices for Convolutional "
    "Neural Networks Applied to Visual Document Analysis. <i>ICDAR</i>, 2003.",
    small))

doc.build(S)
print("ok")
