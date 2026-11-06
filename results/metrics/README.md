# results/metrics

Written by `metrics_analysis.py` (person C). Read `results_analysis.ipynb` for
tables, figures and conclusions.

**Current status: preview.** Only `models/cnn_mnist_seed42.pt` is committed to
the repository, so these files cover the CNN with seed 42. To get the full
3 models x 3 seeds tables, put the `models/` folder from the Colab
`outputs.zip` (the run behind `results/ablation_summary.csv`) into the
project and re-run the notebook. Do not retrain instead: a new training run
gives slightly different checkpoints, and the numbers would no longer match
`ablation_summary.csv`.
