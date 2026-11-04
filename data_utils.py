"""
Loading the two datasets used in the study.

Owner: person B (MNIST) and person D (our own data, labels.csv).

    load_mnist()          source domain, via torchvision
    load_airwrite()       target domain, our own digits from data/raw/
    make_synthetic_airwrite()
                          a clearly-labelled STAND-IN for the target domain,
                          built by distorting MNIST test digits. It exists
                          only so that the whole pipeline can be developed
                          and tested before real data has been collected.
                          Numbers obtained on it must never appear in the
                          report as results on our data.
"""

import csv

import cv2
import numpy as np

import config
from preprocessing import elastic_deform, skeletonize


# --------------------------------------------------------------------------
# Source domain: MNIST
# --------------------------------------------------------------------------

def load_mnist(train: bool):
    """
    Return MNIST as numpy arrays.

    Returns:
        images: uint8 array (N, 28, 28), white digits on black.
        labels: int64 array (N,).

    torchvision downloads the files on first use into data/mnist/ (ignored by
    git). It tries several mirrors, which helps when the original host is
    slow.
    """
    from torchvision.datasets import MNIST    # imported lazily: heavy

    ds = MNIST(root=str(config.DATA_MNIST), train=train, download=True)
    return ds.data.numpy(), ds.targets.numpy().astype(np.int64)


# --------------------------------------------------------------------------
# Target domain: digits written in the air by the group
# --------------------------------------------------------------------------

def scan_raw_folder():
    """
    Find every collected sample under data/raw/<writer>/<digit>/*.png.

    Returns:
        list of (path, label, writer) tuples, sorted so that the order - and
        therefore every random split made from it - is reproducible.
    """
    rows = []
    for path in sorted(config.DATA_RAW.glob("*/*/*.png")):
        digit_dir = path.parent.name
        if not digit_dir.isdigit():
            continue
        rows.append((path, int(digit_dir), path.parent.parent.name))
    return rows


def write_labels_csv(rows):
    """Write data/labels.csv with columns path, label, writer."""
    out = config.PROJECT_ROOT / "data" / "labels.csv"
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "label", "writer"])
        for path, label, who in rows:
            writer.writerow([path.relative_to(config.PROJECT_ROOT).as_posix(),
                             label, who])
    return out


def load_airwrite():
    """
    Load our own collected digits, raw and uncropped to 28x28.

    Returns:
        images:  list of uint8 arrays of varying size.
        labels:  int64 array (N,).
        writers: array of writer names (N,).

    Also refreshes data/labels.csv so that the file always matches the
    folder contents.
    """
    rows = scan_raw_folder()
    if not rows:
        raise FileNotFoundError(
            "No collected digits found in data/raw/. Run collect_data.py "
            "first, or pass --synthetic to test the pipeline on stand-in "
            "data.")
    write_labels_csv(rows)

    images = [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE) for p, _, _ in rows]
    labels = np.array([r[1] for r in rows], dtype=np.int64)
    writers = np.array([r[2] for r in rows])
    return images, labels, writers


# --------------------------------------------------------------------------
# Synthetic stand-in for the target domain (development only)
# --------------------------------------------------------------------------

# Four imaginary "writers" with different habits, so that the
# leave-one-writer-out code has something meaningful to work on.
_SYNTHETIC_WRITERS = {
    "synth_a": dict(thickness=(10, 14), slant=-0.10, tremor=3.0, joins=0.3),
    "synth_b": dict(thickness=(14, 20), slant=0.15, tremor=5.0, joins=0.5),
    "synth_c": dict(thickness=(8, 12), slant=0.00, tremor=2.0, joins=0.2),
    "synth_d": dict(thickness=(16, 22), slant=0.25, tremor=6.0, joins=0.6),
}


def _air_stroke(digit28, rng, style):
    """
    Turn one MNIST digit into something that looks drawn with a finger.

    The digit is enlarged to webcam scale, reduced to its centre line, then
    redrawn with a thick stroke, slanted, made to tremble, and - like a pen
    that cannot be lifted - sometimes joined back to its start by an extra
    stroke.
    """
    size = int(rng.integers(160, 260))
    big = cv2.resize(digit28, (size, size), interpolation=cv2.INTER_CUBIC)
    big = (big > 100).astype(np.uint8) * 255
    skel = skeletonize(big)

    # Slant (shear) and a random aspect change: hands distort proportions.
    stretch = rng.uniform(0.8, 1.25)
    shear = np.float32([[stretch, style["slant"], 0], [0, 1, 0]])
    width = int(size * (stretch + abs(style["slant"]))) + 1
    skel = cv2.warpAffine(skel, shear, (width, size), borderValue=0)
    skel = (skel > 0).astype(np.uint8) * 255

    # Thick stroke with a random width, like an index finger at arm's length.
    lo, hi = style["thickness"]
    t = int(rng.integers(lo, hi + 1))
    out = cv2.dilate(skel, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (t, t)))

    # Unwanted connecting stroke between two random points of the digit.
    if rng.random() < style["joins"]:
        ys, xs = np.nonzero(skel)
        i, j = rng.integers(0, len(ys), size=2)
        cv2.line(out, (int(xs[i]), int(ys[i])), (int(xs[j]), int(ys[j])),
                 255, max(2, t // 2), cv2.LINE_AA)

    # Tremor: a coarse elastic deformation at webcam scale.
    out = elastic_deform(out, rng, alpha=style["tremor"] * 8, sigma=12.0)

    # Crop with the same margin the whiteboard uses.
    ys, xs = np.nonzero(out)
    m = config.CROP_MARGIN
    out = np.pad(out, m)
    return out[ys.min():ys.max() + 2 * m + 1, xs.min():xs.max() + 2 * m + 1]


def make_synthetic_airwrite(per_writer=100, seed=config.SEED):
    """
    Build a stand-in dataset with the same format as load_airwrite().

    Uses MNIST TEST digits, which the model never trains on.
    """
    rng = np.random.default_rng(seed)
    mnist_x, mnist_y = load_mnist(train=False)
    images, labels, writers = [], [], []
    for name, style in _SYNTHETIC_WRITERS.items():
        for k in range(per_writer):
            digit = k % 10                       # balanced classes
            pool = np.flatnonzero(mnist_y == digit)
            idx = int(rng.choice(pool))
            images.append(_air_stroke(mnist_x[idx], rng, style))
            labels.append(digit)
            writers.append(name)
    return images, np.array(labels, dtype=np.int64), np.array(writers)


def load_target(synthetic: bool):
    """Our data, or the synthetic stand-in when synthetic=True."""
    return make_synthetic_airwrite() if synthetic else load_airwrite()
