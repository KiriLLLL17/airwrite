# Writing in the Air

Measuring and mitigating domain shift in handwritten digit recognition.

Course project for *Programming with Python, Fall 2026*, Beijing Institute of
Technology. Deadline: **13 November 2026**.

## The question

A CNN trained on MNIST reaches above 99% accuracy. Does it still work on
digits written in the air with a finger? Those digits have uneven stroke
width, hand tremor, distorted proportions, and unwanted connecting strokes
because the pen cannot be lifted.

We measure how much accuracy is lost, then test which interventions recover
it: stroke normalisation, centre-of-mass alignment, training-time
augmentation, and fine-tuning.

The gesture whiteboard is the instrument for collecting that data, not the
project itself.

## Setup

Python 3.11 (3.10 also works). MediaPipe 0.10.21 has no wheels for 3.13+.

```bash
py -3.11 -m venv .venv            # macOS/Linux: python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
python gestures.py     # gesture logic self-test, no webcam needed
python whiteboard.py   # free drawing
```

Gestures: index finger draws, fist pauses, index+middle moves the cursor
without drawing, open palm clears.

Collecting data:

```bash
python collect_data.py --writer <yourname> --per-digit 10
```

Walks through digits 0-9. SPACE saves, `c` clears, `n` next digit, `b` back,
`q` quits. Safe to stop and resume — numbering continues and nothing is
overwritten.

**Write naturally.** Do not imitate the MNIST style; measuring the real
difference between the two domains is the entire point.

## Experiments

```bash
python train.py        # MNIST: logistic regression, CNN, CNN + augmentation, 3 seeds
python ablation.py     # our data: ablation, fine-tuning, leave-one-writer-out
python analysis.py     # figures/ and results/headline.json
```

On Colab, `airwrite_colab.ipynb` runs all three. On a laptop CPU the full
`train.py` takes roughly an hour; on a Colab T4 about 15-25 minutes.

Self-test without collected data (about 2 minutes, outputs go to `*/smoke/`):

```bash
python train.py --quick
python ablation.py --quick --synthetic
python analysis.py --quick --synthetic
```

`--synthetic` uses stand-in digits made by distorting MNIST. It exists only
to test the pipeline; its numbers are **not** results.

## Tuning

If the whiteboard behaves badly, adjust in `config.py`:

| Setting | Symptom |
|---|---|
| `STROKE_THICKNESS` | strokes too thick or too thin for the digit size |
| `SMOOTHING_WINDOW` | raise if lines are ragged, lower if drawing lags |
| `CAMERA_INDEX` | the wrong webcam opens |

## Documentation

- `CLAUDE.md` — project context, module contracts, current status
- `docs/project-plan.md` — step-by-step plan across all phases
- `docs/division-of-work.md` — who owns which files
- `docs/SETUP_PL.md` — instalacja i zbieranie danych dla zespołu (po polsku)
- `docs/team-tasks.md` — concrete tasks per person for the remaining days
- `docs/course-requirements.md` — course brief as a checklist (Polish)
- `docs/course-brief.pdf` — the original brief
- `docs/project_proposal.pdf` — two-page English proposal

## Status

All pipeline code is written and tested end to end on synthetic stand-in
data. The whiteboard is **not yet verified with a real webcam**, and our own
data has not been collected yet.
