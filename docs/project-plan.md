# Project plan

Step-by-step breakdown. `[A]` `[B]` `[C]` `[D]` mark the responsible person,
`[all]` marks joint work. See `division-of-work.md` for who is who.

Critical path: **Phase 1 -> Phase 4 -> Phase 5.** Without a working
whiteboard there is no dataset, and without a dataset there are no
experiments. Finish Phase 1 before anyone invests heavily elsewhere.

---

## Phase 0 — Setup (30 min, all)

1. Clone the repo, everyone on the same commit.
2. Create a virtual environment, `pip install -r requirements.txt`.
3. **Critical test:** every member runs `python whiteboard.py` and confirms
   the webcam opens and the hand skeleton is drawn. Resolve failures now,
   not later.
4. Run `python gestures.py` — the gesture self-test must pass.
5. Agree that nobody changes `config.SEED`.

---

## Phase 1 — Whiteboard [A] (2 h)

Status: code written, **not yet verified on real hardware**.

1. Verify camera opens and frames are mirrored (`cv2.flip`).
2. Verify MediaPipe detects the hand and the skeleton overlay appears.
3. Verify each gesture: index = draw, fist = pause, two fingers = move,
   open palm = clear.
4. Tune `STROKE_THICKNESS` if strokes are too thick or thin relative to
   digit size.
5. Tune `SMOOTHING_WINDOW`: increase if lines are ragged, decrease if
   drawing feels laggy.
6. Confirm that losing the hand breaks the stroke (no long connecting line).
7. Confirm `extract_digit()` crops tightly and saves a raw, uncropped-size
   grayscale PNG.

---

## Phase 2 — Model on MNIST [B] (1.5 h)

1. Load MNIST via `torchvision`, split train into train/val (54k/6k).
2. Save a 5x5 grid of sample images to `figures/`.
3. Baseline: multinomial logistic regression on flattened pixels. Record
   accuracy — this is the reference point in the results table.
4. CNN: 3x (Conv -> BatchNorm -> ReLU -> MaxPool), dropout, one dense layer.
5. Set `torch.manual_seed(SEED)` and `np.random.seed(SEED)`.
6. Training loop with per-epoch validation, 10-15 epochs.
7. **Measure one epoch first**, then extrapolate before committing to a
   number of epochs.
8. Save checkpoint to `models/cnn_mnist.pt`, learning curves to `figures/`.
9. Confusion matrix on the MNIST test set.
10. Expose `predict(img) -> (digit, confidence)` for the others.

---

## Phase 3 — Preprocessing [C] (2 h)

Start before real data exists: build a stand-in set by artificially
thickening, shifting and rescaling MNIST digits.

1. `to_grayscale_binary(img)` — thresholding.
2. `normalize_thickness(img)` — morphological erosion/dilation or
   skeletonisation to a constant stroke width.
3. `center_by_mass(img)` — centre of mass alignment, as in original MNIST.
4. `resize_with_padding(img)` — scale to 20x20 preserving aspect ratio, pad
   to 28x28.
5. `normalize_pixels(img)` — match MNIST value range.
6. `preprocess(img, steps=[...])` — configurable pipeline. **This is the key
   piece**: the ablation depends on being able to switch steps on and off
   without rewriting code.
7. Before/after visualisation for every step, saved to `figures/`.
8. Augmentation for training: random dilation, rotation ±10°, translation,
   elastic deformation.

---

## Phase 4 — Data collection [all] (30 min)

1. [A] confirms `collect_data.py` works and tells the others.
2. Each member runs
   `python collect_data.py --writer <name> --per-digit 20`
   and writes 75-100 digits total.
3. **Write naturally.** Do not imitate MNIST — that would destroy the
   experiment.
4. Everyone commits their `data/raw/<writer>/` folder.
5. [D] checks that every digit has a comparable number of samples per writer.
6. [D] builds `data/labels.csv` with columns: path, label, writer.

Target: 800 images from 4 writers (20 per digit each).

---

## Phase 5 — Experiments [C] + [B] (3 h)

**5.1 Measure the gap (the central result)**
1. Load the MNIST-only checkpoint.
2. Run our data through minimal preprocessing (resize only).
3. Record accuracy — expect a substantial drop.
4. Confusion matrix on our data; which digits are confused.
5. Save misclassified examples to `figures/`.

**5.2 Ablation**
6. + stroke normalisation.
7. + centre-of-mass alignment.
8. + both.
9. Model trained with augmentation, tested on our data.
10. Fine-tuning on 70% of our data, tested on the remaining 30%.
11. Every variant with **3 seeds**, mean ± std.
12. All results into one CSV in `results/`.

**5.3 Cross-writer**
13. Train/fine-tune on 3 writers, test on the fourth.
14. Repeat with each writer held out.
15. Compare — is any writing style systematically harder?

---

## Phase 6 — Analysis and figures [D] (2 h)

1. Bar chart: accuracy per ablation variant, with error bars.
2. Distribution comparison: stroke thickness, fill ratio, MNIST vs. ours.
3. Sample grid: the same digit from MNIST and from each writer.
4. Cross-writer variability chart.
5. Consistent styling and readable captions throughout.
6. Write every number to `results/` so report and code cannot diverge.

---

## Phase 7 — Report [D], input from [all] (3 h)

Follow the template in `course-requirements.md` exactly.

1. **Introduction** — the domain shift problem, why it matters, headline
   result in two sentences.
2. **Method** — justify CNN against the baseline, pipeline diagram, describe
   each preprocessing step.
3. **Results** — both datasets, metrics, ablation table, confusion matrices,
   figures. Include the ablation study: the template explicitly asks for it.
4. **Discussion** — strengths, limitations (small dataset, 4 writers, single
   lighting condition), lessons, future work.
   Stating limitations honestly raises the mark; hiding them lowers it.
5. **References** — MNIST (LeCun et al. 1998), MediaPipe Hands, PyTorch,
   OpenCV, Simard et al. 2003.
6. [all] Each member reviews the section covering their part.
7. [all] Add comments to your own code — a separate course requirement.

---

## Phase 8 — Presentation [all] (1 h)

1. Slides: problem (1), method (2), results (3), demo (1), conclusions (1).
2. [A] prepares the live demo **and a recorded backup** in case the camera
   fails on stage.
3. Speaking order: D intro -> B method -> C results -> A demo -> D
   conclusions. Roughly 2-3 min each.
4. Rehearse once out loud with a timer. The limit is 10 minutes.
5. Prepare answers: why a CNN, why so little data, what next.

---

## Phase 9 — Submission [D] (30 min)

1. Verify the code runs from scratch in a clean environment.
2. Package **separately**: `report.zip`, `code.zip`, `data.zip`.
3. python123.io: **report and code only, no data**.
4. Email to `python_projects@163.com`, subject
   `CourseProjectFall2026-Name1-ID1-Name2-ID2-Name3-ID3-Name4-ID4`.
5. Body: project title, and for every member name, student ID, class,
   responsibilities, contribution.
6. One email for the whole group.
