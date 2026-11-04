# Division of work

Split by pipeline layer, so file boundaries are clean and git conflicts are
unlikely. Fill in the real names before submitting — the course requires
responsibilities and contributions to be stated per person.

| | Name | Student ID | Class |
|---|---|---|---|
| A | | | |
| B | | | |
| C | | | |
| D | | | |

---

## A — Acquisition

**Files:** `gestures.py`, `whiteboard.py`, `collect_data.py`

Hand tracking with MediaPipe, gesture recognition, trajectory smoothing,
canvas and digit extraction, the data collection tool. Presents the live demo.

This is the **critical path** — nobody has real data until it works, so this
role should go to the strongest member of the group.

**Hands off:** `data/raw/` images, once collected.

---

## B — Modelling

**Files:** `model.py`, `train.py`, `config.py`

CNN architecture, training loop, logistic-regression baseline, learning
curves, checkpoints. Later: fine-tuning on our own data.

Starts immediately — MNIST needs no input from anyone else.

**Provides:** `models/cnn_mnist.pt` and `predict(img) -> (digit, confidence)`.

---

## C — Preprocessing and evaluation

**Files:** `preprocessing.py`, `evaluate.py`, `ablation.py`

Stroke-thickness normalisation, centre-of-mass alignment, resizing,
augmentation. Metrics, confusion matrices, and running every ablation variant.

Does not need to wait for A: builds and tests the pipeline on artificially
distorted MNIST digits first, then swaps in the real images.

**Provides:** `preprocess(img, steps)` and the results table in `results/`.

---

## D — Analysis, report, submission

**Files:** `analysis.py`, report, slides

Summary figures, distribution comparisons, cross-writer study. Writes the
report to the course template, packages and submits.

Starts with Introduction and Method, which need no results.

---

## Joint

**Data collection — all four members.** Roughly 75-100 digits each. This is
not one person's chore: four writers are what makes the cross-writer analysis
possible, and it is the part that cannot be parallelised away.

---

## Agree the interfaces first

Before anyone writes implementation code, confirm the two contracts in
`CLAUDE.md`. Everyone can then develop against a stub
(`return np.zeros((28, 28), dtype=np.float32)`) and integration takes minutes
instead of hours.

---

## If someone drops out

Merge **C and D**. Both sit at the end of the pipeline and work on the same
numbers, so the overlap is smallest there.

Never merge A and B — they are the two heaviest parts, and one person doing
both becomes the bottleneck for everyone else.

---

## For the submission email

- **A** — acquisition: hand tracking, gesture logic, data collection pipeline
- **B** — modelling: CNN architecture, training, baseline, fine-tuning
- **C** — image processing and evaluation: normalisation, augmentation,
  metrics, ablation studies
- **D** — analysis, visualisation, report, coordination
