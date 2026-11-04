"""
Shared configuration for the whole project.

Every module imports its constants from here so that all four parts of the
project (acquisition, model, preprocessing, analysis) agree on paths, image
sizes and the random seed.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Reproducibility
# --------------------------------------------------------------------------
# A single seed used by every script that involves randomness. The course
# requires reproducible results, so this value must never be changed casually.
SEED = 42

# Every experiment is repeated with these three seeds and reported as
# mean +/- std, so that differences between variants can be told apart from
# run-to-run noise. SEED is the first one and is used for single-run figures.
SEEDS = (42, 43, 44)

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"          # our own, unprocessed digits
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_MNIST = PROJECT_ROOT / "data" / "mnist"      # downloaded by torchvision
MODELS_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "figures"
RESULTS_DIR = PROJECT_ROOT / "results"

for _d in (DATA_RAW, DATA_PROCESSED, DATA_MNIST, MODELS_DIR, FIGURES_DIR,
           RESULTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# Image format
# --------------------------------------------------------------------------
# MNIST images are 28x28 grayscale, white strokes on a black background.
# Our canvas uses the same convention so that no colour inversion is needed.
IMG_SIZE = 28

# The original MNIST procedure scales each digit so that its bounding box
# fits into 20x20 pixels, then pastes it into a 28x28 frame. Our
# preprocessing reproduces that, so the same constant is used there.
DIGIT_BOX = 20

# Mean and standard deviation of MNIST pixel values (after scaling to [0, 1]).
# Both the training data and our own images are standardised with these.
MNIST_MEAN = 0.1307
MNIST_STD = 0.3081

# --------------------------------------------------------------------------
# Training settings
# --------------------------------------------------------------------------
EPOCHS = 8                # MNIST converges well within 8-10 epochs
BATCH_SIZE = 128
LEARNING_RATE = 1e-3
VAL_SIZE = 6000           # MNIST train split: 54k train / 6k validation

FINETUNE_FRACTION = 0.7   # share of our own data used for fine-tuning
FINETUNE_EPOCHS = 15
FINETUNE_LR = 1e-4        # small: we adapt the model, not retrain it

# --------------------------------------------------------------------------
# Acquisition settings
# --------------------------------------------------------------------------
CAMERA_INDEX = 0          # change if the wrong webcam opens
FRAME_WIDTH = 960
FRAME_HEIGHT = 540

STROKE_THICKNESS = 12     # pixels, at full camera resolution
SMOOTHING_WINDOW = 5      # number of past fingertip positions averaged
CROP_MARGIN = 20          # pixels kept around the digit when cropping

# MediaPipe landmark indices (see the MediaPipe Hands documentation).
WRIST = 0
THUMB_TIP, THUMB_IP = 4, 3
INDEX_TIP, INDEX_PIP, INDEX_MCP = 8, 6, 5
MIDDLE_TIP, MIDDLE_PIP = 12, 10
RING_TIP, RING_PIP = 16, 14
PINKY_TIP, PINKY_PIP, PINKY_MCP = 20, 18, 17


# --------------------------------------------------------------------------
# Separate output folders for test runs
# --------------------------------------------------------------------------
def redirect_outputs(subdir: str, models: bool = True):
    """
    Send results (and optionally models and figures) to a sub-folder.

    Used by --quick smoke tests and by --synthetic runs on stand-in data, so
    that their numbers can never be mistaken for, or overwrite, the real
    results that go into the report. Modules read these paths at call time
    (config.RESULTS_DIR, not `from config import RESULTS_DIR`), so rebinding
    them here takes effect everywhere.
    """
    global MODELS_DIR, FIGURES_DIR, RESULTS_DIR
    FIGURES_DIR = PROJECT_ROOT / "figures" / subdir
    RESULTS_DIR = PROJECT_ROOT / "results" / subdir
    if models:
        MODELS_DIR = PROJECT_ROOT / "models" / subdir
    for d in (MODELS_DIR, FIGURES_DIR, RESULTS_DIR):
        d.mkdir(parents=True, exist_ok=True)
