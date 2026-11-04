"""
Metrics, seed aggregation and confusion matrices.

Owner: person C.

Reported metrics: accuracy, macro-F1 and per-class F1. Every configuration
is run with 3 seeds and reported as mean +/- std, so that differences between
variants can be told apart from run-to-run noise.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

import plotting
from model import predict_batch


def compute_metrics(y_true, y_pred) -> dict:
    """Accuracy, macro-F1 and the ten per-class F1 scores."""
    per_class = f1_score(y_true, y_pred, labels=range(10), average=None,
                         zero_division=0)
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, labels=range(10),
                             average="macro", zero_division=0),
        "n": len(y_true),
    }
    for digit, score in enumerate(per_class):
        metrics[f"f1_{digit}"] = score
    return metrics


def evaluate(model, images, labels) -> dict:
    """
    Return a dict of metrics for one model/dataset pair.

    Args:
        model: a trained DigitCNN.
        images: float32 (N, 28, 28), already preprocessed.
        labels: int (N,).
    """
    preds, _ = predict_batch(model, images)
    return compute_metrics(labels, preds)


def summarise(runs: pd.DataFrame, group_cols, metric_cols=None) -> pd.DataFrame:
    """
    Collapse per-seed rows into mean and std per configuration.

    Args:
        runs: one row per (configuration, seed).
        group_cols: columns identifying a configuration, e.g. ["variant"].

    Returns:
        One row per configuration with <metric>_mean and <metric>_std columns
        and the number of seeds that went into it.
    """
    metric_cols = metric_cols or ["accuracy", "macro_f1"]
    grouped = runs.groupby(group_cols, sort=False)
    out = grouped[metric_cols].agg(["mean", "std"])
    out.columns = [f"{m}_{s}" for m, s in out.columns]
    out["seeds"] = grouped.size()
    return out.reset_index()


def save_confusion_matrix(y_true, y_pred, title, path):
    """Plot a row-normalised confusion matrix and save it to path."""
    cm = confusion_matrix(y_true, y_pred, labels=range(10))
    plotting.confusion(cm, title, path)
    return cm
