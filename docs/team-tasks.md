# Team tasks

The pipeline code is written and tested end to end on stand-in data
(`--synthetic`). What is left is the part that needs people: verifying the
webcam tool, collecting the data, running the experiments, checking the
results, and writing everything up.

Each task names the files you may edit. **Edit only those files** and do
not change the function signatures listed in `CLAUDE.md`, then merging is
trivial. Fill in who is A-D in `division-of-work.md`.

Target: a presentable version in **3 days**.

---

## Before anyone starts (everyone, 30 min)

1. Install **Python 3.11** (not 3.12+, MediaPipe 0.10.21 has no wheels for it).
2. Create the environment:
   ```bash
   py -3.11 -m venv .venv
   .venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the self-tests. All four must finish without errors (about 2 minutes
   on a laptop, the first run downloads MNIST):
   ```bash
   python gestures.py
   python train.py --quick
   python ablation.py --quick --synthetic
   python analysis.py --quick --synthetic
   ```
   `--quick` and `--synthetic` write to `*/smoke/` and `*/synthetic/`
   folders. **Never quote those numbers in the report**, they are not
   results on our data.
4. `python whiteboard.py`: the webcam window must open, the hand skeleton
   must be drawn, and the index finger must draw a white line.

---

## Day 1: data

### Everyone: collect your digits (20-30 min each)

```bash
python collect_data.py --writer <yourname> --per-digit 10
```

- 10 samples of each digit = 100 images per person.
- **Write naturally, at your normal speed.** Do not try to make the digits
  look like MNIST, because measuring that difference is the whole point.
- Afterwards check `data/raw/<yourname>/`: every digit folder should hold
  10 images. Delete obviously broken ones (an empty or half-drawn digit)
  **before** anyone has seen any results, and note how many you deleted.
- Send your `data/raw/<yourname>/` folder to the coordinator, or commit it.

### A: acquisition and live demo
Files: `whiteboard.py`, `collect_data.py`, `config.py` (only the
acquisition settings).

1. Before the others start collecting, verify the checklist in
   `project-plan.md`, Phase 1. Tune `STROKE_THICKNESS` and
   `SMOOTHING_WINDOW` if needed. **Do not change them after collection has
   started**, otherwise the writers are no longer comparable.
2. Add live prediction for the presentation demo: a `--predict` flag for
   `whiteboard.py` that, while the user pauses (fist), shows the predicted
   digit and confidence on screen. Use only the existing interfaces:
   ```python
   from preprocessing import preprocess, FULL_STEPS
   from model import predict
   digit, conf = predict(preprocess(board.extract_digit(), FULL_STEPS))
   ```
   (Needs `models/cnn_mnist_seed42.pt` from B's training run.)
3. Record a 30-60 s screen video of the demo as a backup in case the
   camera fails on stage.

---

## Day 2: experiments and checks

### B: modelling
Files: `model.py`, `train.py`, `airwrite_colab.ipynb`.

1. Run `airwrite_colab.ipynb` on Colab (T4 GPU) once all data is in.
   It runs `train.py`, `ablation.py` and `analysis.py` and downloads
   `outputs.zip`.
2. Put `results/`, `figures/` and `models/` from the zip into the project
   folder.
3. Check `figures/learning_curves.png`: validation accuracy should
   flatten out by about epoch 6-8 at roughly 99 %. Note the training time
   per epoch from `results/history_*.csv`.
4. Write the **Method** paragraph about the CNN and the logistic-regression
   baseline (why a small CNN, architecture, training setup, seeds).

### C: preprocessing and evaluation
Files: `preprocessing.py`, `evaluate.py`, `ablation.py`.

1. Look at `figures/preprocessing_steps.png` on the real data. Does every
   step do what it says? Report anything broken to the coordinator.
2. `TARGET_STROKE_RATIO` in `preprocessing.py` may be adjusted **only**
   using `results/domain_stats.csv` (stroke widths), **never** by looking at
   which value gives higher accuracy. Tuning on the test data would be
   result manipulation.
3. Go through `figures/misclassified_minimal.png` and
   `confusion_ours_minimal.png`: which digit pairs get confused, and why?
   Write 3-5 sentences for the results section.
4. Write the **Method** paragraph on preprocessing and augmentation, and
   the **Experimental Results** section from `results/*.csv`.

### D: analysis, report, submission
Files: `analysis.py`, `plotting.py`, the report, the slides.

1. Start the report now with the exact 5-section template from
   `course-requirements.md`: Introduction and Method need no results.
2. When results arrive, copy every number from `results/headline.json`,
   `ablation_summary.csv` and `lowo_summary.csv`. Do not round in your
   head and do not quote anything that is not in those files.
3. Write **Discussion and Conclusion** with honest limitations: 4 writers,
   about 400 images, one webcam, one lighting setup, a single session per
   writer.
4. Fill in names, IDs and classes everywhere.

---

## Day 3: report and presentation (everyone)

- Everyone reviews the report section about their part, and checks that
  their own code has enough comments (a separate course requirement).
- Slides (10 min): problem (1), method (2), results (3), live demo (1),
  conclusions (1). Speaking order: D, B, C, A, D.
- Rehearse once with a timer.
- D packages `report.zip`, `code.zip` and `data.zip` and submits both ways
  (see `CLAUDE.md`, "Submission").

---

## Rules that keep the merge painless

- Edit only your own files. If you need a change in someone else's file,
  ask them.
- Before sending or committing code, run the four self-test commands at the
  top of this file.
- Never change `config.SEED` / `config.SEEDS`.
- Never put a number in the report that is not in `results/`.
