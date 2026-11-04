"""
Gesture recognition from MediaPipe hand landmarks.

This module is deliberately free of any MediaPipe or OpenCV import: it works
on plain (x, y) coordinate lists. That keeps the gesture logic unit-testable
without a webcam, which matters because this is the part most likely to need
tuning.

Landmark convention (MediaPipe Hands, 21 points):
    0  wrist
    1-4   thumb   (4 = tip)
    5-8   index   (8 = tip, 6 = PIP joint)
    9-12  middle  (12 = tip, 10 = PIP)
    13-16 ring    (16 = tip, 14 = PIP)
    17-20 pinky   (20 = tip, 18 = PIP)

Coordinates are normalised to [0, 1] with the origin in the TOP-LEFT corner,
so a smaller y means higher up on the image.
"""

import math

from config import (
    WRIST,
    THUMB_TIP, THUMB_IP,
    INDEX_TIP, INDEX_PIP,
    MIDDLE_TIP, MIDDLE_PIP,
    RING_TIP, RING_PIP,
    PINKY_TIP, PINKY_PIP, PINKY_MCP,
)

# Drawing modes returned by classify_gesture().
MODE_DRAW = "draw"
MODE_PAUSE = "pause"
MODE_MOVE = "move"
MODE_CLEAR = "clear"
MODE_NONE = "none"


def _distance(a, b):
    """Euclidean distance between two (x, y) points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def fingers_up(landmarks):
    """
    Decide which fingers are extended.

    Args:
        landmarks: sequence of 21 (x, y) pairs, normalised to [0, 1].

    Returns:
        list of five ints (0 or 1), ordered
        [thumb, index, middle, ring, pinky].

    The four long fingers use a simple vertical test: a finger is extended
    when its tip sits above its PIP joint. The thumb cannot use that test
    because it bends sideways rather than downwards. Instead we compare how
    far the thumb tip and the thumb IP joint are from the base of the pinky:
    an extended thumb points away from the palm, so its tip is the farther of
    the two. This test needs no knowledge of which hand is in frame, which
    matters here because the camera image is mirrored before processing.
    """
    state = []

    # --- thumb -----------------------------------------------------------
    pinky_base = landmarks[PINKY_MCP]
    tip_far = _distance(landmarks[THUMB_TIP], pinky_base)
    ip_far = _distance(landmarks[THUMB_IP], pinky_base)
    state.append(1 if tip_far > ip_far else 0)

    # --- four long fingers ------------------------------------------------
    for tip, pip in (
        (INDEX_TIP, INDEX_PIP),
        (MIDDLE_TIP, MIDDLE_PIP),
        (RING_TIP, RING_PIP),
        (PINKY_TIP, PINKY_PIP),
    ):
        # Smaller y = higher on the image = finger extended upwards.
        state.append(1 if landmarks[tip][1] < landmarks[pip][1] else 0)

    return state


def classify_gesture(state):
    """
    Map a finger state vector onto a drawing mode.

    Args:
        state: the five-element list returned by fingers_up().

    Returns:
        One of the MODE_* constants.

    The thumb is ignored for the draw and pause gestures. Many people keep
    the thumb loosely extended while pointing, and requiring it to be tucked
    in makes the interface frustrating to use.
    """
    _, index, middle, ring, pinky = state

    if index and not middle and not ring and not pinky:
        return MODE_DRAW                      # pointing: draw

    if index and middle and not ring and not pinky:
        return MODE_MOVE                      # two fingers: reposition

    if not index and not middle and not ring and not pinky:
        return MODE_PAUSE                     # fist: stop drawing

    if index and middle and ring and pinky:
        return MODE_CLEAR                     # open palm: wipe the canvas

    return MODE_NONE                          # anything else: do nothing


# --------------------------------------------------------------------------
# Self-test. Run `python gestures.py` to check the logic without a webcam.
# --------------------------------------------------------------------------
if __name__ == "__main__":
    def make_hand(extended):
        """
        Build a synthetic set of 21 landmarks for testing.

        `extended` is a list of five booleans. Fingers are laid out side by
        side; an extended finger has its tip above its PIP joint, a folded
        one below. The thumb is placed either away from the palm or across
        it, matching the distance test in fingers_up().
        """
        pts = [(0.5, 0.9)] * 21                       # default: wrist height
        pts[WRIST] = (0.5, 0.9)
        pts[PINKY_MCP] = (0.70, 0.75)                 # base of the pinky

        # Thumb: extended points left (away from the pinky base).
        if extended[0]:
            pts[THUMB_IP] = (0.40, 0.75)
            pts[THUMB_TIP] = (0.30, 0.72)
        else:
            pts[THUMB_IP] = (0.55, 0.75)
            pts[THUMB_TIP] = (0.62, 0.74)

        long_fingers = [
            (INDEX_TIP, INDEX_PIP, 0.45),
            (MIDDLE_TIP, MIDDLE_PIP, 0.52),
            (RING_TIP, RING_PIP, 0.59),
            (PINKY_TIP, PINKY_PIP, 0.66),
        ]
        for (tip, pip, x), is_up in zip(long_fingers, extended[1:]):
            pts[pip] = (x, 0.70)
            pts[tip] = (x, 0.50) if is_up else (x, 0.80)

        return pts

    cases = [
        ("point (index only)",      [0, 1, 0, 0, 0], MODE_DRAW),
        ("point with loose thumb",  [1, 1, 0, 0, 0], MODE_DRAW),
        ("fist",                    [0, 0, 0, 0, 0], MODE_PAUSE),
        ("two fingers",             [0, 1, 1, 0, 0], MODE_MOVE),
        ("open palm",               [1, 1, 1, 1, 1], MODE_CLEAR),
        ("three fingers",           [0, 1, 1, 1, 0], MODE_NONE),
    ]

    failures = 0
    for name, truth, expected_mode in cases:
        hand = make_hand(truth)
        detected = fingers_up(hand)
        mode = classify_gesture(detected)

        detect_ok = detected == truth
        mode_ok = mode == expected_mode
        if not (detect_ok and mode_ok):
            failures += 1

        flag = "ok  " if (detect_ok and mode_ok) else "FAIL"
        print(f"[{flag}] {name:24s} expected {truth} -> {expected_mode:5s} "
              f"| got {detected} -> {mode}")

    print()
    print("all tests passed" if failures == 0 else f"{failures} test(s) failed")
