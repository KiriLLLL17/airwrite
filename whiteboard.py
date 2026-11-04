"""
Gesture-controlled virtual whiteboard.

Tracks one hand through the webcam and turns finger gestures into drawing
commands:

    index finger only  -> draw
    closed fist        -> stop drawing
    index + middle     -> move the cursor without drawing
    open palm          -> clear the canvas

Run directly for free drawing:

    python whiteboard.py

The Whiteboard class is also imported by collect_data.py, which reuses it to
record our own dataset of digits written in the air.
"""

import cv2
import numpy as np
from collections import deque

import config
from gestures import (
    fingers_up, classify_gesture,
    MODE_DRAW, MODE_PAUSE, MODE_MOVE, MODE_CLEAR,
)

# MediaPipe prints a lot of initialisation noise on some platforms; importing
# it after the other modules keeps that noise out of the way of real errors.
import mediapipe as mp


class HandTracker:
    """Thin wrapper around MediaPipe Hands, limited to a single hand."""

    def __init__(self, detection_confidence=0.7, tracking_confidence=0.6):
        self._hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,                # one hand keeps the logic simple
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self._drawing = mp.solutions.drawing_utils
        self._connections = mp.solutions.hands.HAND_CONNECTIONS

    def find(self, frame_bgr):
        """
        Locate the hand in a BGR frame.

        Returns:
            (landmarks, raw_result) where landmarks is a list of 21 (x, y)
            pairs normalised to [0, 1], or None when no hand is visible.
        """
        # MediaPipe expects RGB; OpenCV gives BGR. Forgetting this conversion
        # is the single most common cause of "it never detects my hand".
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False           # small speed-up
        result = self._hands.process(frame_rgb)

        if not result.multi_hand_landmarks:
            return None, result

        hand = result.multi_hand_landmarks[0]
        landmarks = [(lm.x, lm.y) for lm in hand.landmark]
        return landmarks, result

    def draw_skeleton(self, frame_bgr, result):
        """Overlay the detected hand skeleton, useful while debugging."""
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                self._drawing.draw_landmarks(
                    frame_bgr, hand, self._connections)

    def close(self):
        self._hands.close()


class Whiteboard:
    """
    Canvas plus drawing state.

    The canvas is a single-channel image holding white strokes on a black
    background, which is exactly the MNIST convention. Keeping it that way
    means no colour inversion is needed later in the pipeline.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width), dtype=np.uint8)

        # Sliding window of recent fingertip positions. Raw MediaPipe output
        # jitters by several pixels between frames, which produces visibly
        # ragged strokes; averaging the last few positions smooths them.
        self._recent = deque(maxlen=config.SMOOTHING_WINDOW)
        self._prev_point = None
        self.mode = MODE_PAUSE

    # -- state ------------------------------------------------------------

    def clear(self):
        """Wipe the canvas and forget the current stroke."""
        self.canvas[:] = 0
        self._recent.clear()
        self._prev_point = None

    def is_empty(self):
        return not self.canvas.any()

    # -- per-frame update --------------------------------------------------

    def update(self, landmarks):
        """
        Advance the whiteboard by one frame.

        Args:
            landmarks: 21 normalised (x, y) pairs, or None if no hand was
                       detected this frame.

        Returns:
            (mode, cursor) where cursor is an (x, y) pixel position or None.
        """
        if landmarks is None:
            # Losing the hand must break the stroke, otherwise the next
            # detection is joined to the last one by a long straight line.
            self._end_stroke()
            self.mode = MODE_PAUSE
            return self.mode, None

        state = fingers_up(landmarks)
        self.mode = classify_gesture(state)

        # Convert the index fingertip from normalised to pixel coordinates.
        nx, ny = landmarks[config.INDEX_TIP]
        raw = (int(nx * self.width), int(ny * self.height))

        if self.mode == MODE_CLEAR:
            self.clear()
            return self.mode, raw

        if self.mode != MODE_DRAW:
            # Pause, move, or an unrecognised gesture: break the stroke so
            # that drawing resumes from wherever the finger reappears.
            self._end_stroke()
            return self.mode, raw

        cursor = self._smooth(raw)
        if self._prev_point is not None:
            cv2.line(self.canvas, self._prev_point, cursor,
                     color=255, thickness=config.STROKE_THICKNESS,
                     lineType=cv2.LINE_AA)
        self._prev_point = cursor
        return self.mode, cursor

    def _smooth(self, point):
        """Average the last few fingertip positions."""
        self._recent.append(point)
        xs = [p[0] for p in self._recent]
        ys = [p[1] for p in self._recent]
        return (int(sum(xs) / len(xs)), int(sum(ys) / len(ys)))

    def _end_stroke(self):
        self._recent.clear()
        self._prev_point = None

    # -- output ------------------------------------------------------------

    def overlay(self, frame_bgr):
        """Composite the canvas onto a camera frame for display."""
        strokes = cv2.cvtColor(self.canvas, cv2.COLOR_GRAY2BGR)
        mask = self.canvas > 0
        out = frame_bgr.copy()
        out[mask] = strokes[mask]
        return out

    def extract_digit(self, margin=None):
        """
        Crop the drawn shape out of the canvas.

        Returns a grayscale image containing just the digit plus a margin, or
        None if the canvas is empty.

        The crop is deliberately NOT resized to 28x28 here. Preprocessing
        variants are compared later in the project, and they must all start
        from the same raw drawing; baking one particular resize into the
        saved data would make that comparison impossible.
        """
        if self.is_empty():
            return None

        margin = config.CROP_MARGIN if margin is None else margin
        ys, xs = np.nonzero(self.canvas)
        y0, y1 = ys.min(), ys.max()
        x0, x1 = xs.min(), xs.max()

        y0 = max(0, y0 - margin)
        x0 = max(0, x0 - margin)
        y1 = min(self.height - 1, y1 + margin)
        x1 = min(self.width - 1, x1 + margin)

        return self.canvas[y0:y1 + 1, x0:x1 + 1].copy()


def open_camera():
    """Open the webcam and apply the configured resolution."""
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera {config.CAMERA_INDEX}. "
            "Close any other application using the webcam, or change "
            "CAMERA_INDEX in config.py."
        )
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    return cap


def draw_hud(frame, lines, cursor=None, mode=None):
    """Write status text onto the frame, and mark the cursor position."""
    for i, text in enumerate(lines):
        cv2.putText(frame, text, (12, 28 + i * 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 4)
        cv2.putText(frame, text, (12, 28 + i * 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 1)

    if cursor is not None:
        # Filled circle while drawing, hollow otherwise, so the current mode
        # is obvious without reading the text.
        filled = -1 if mode == MODE_DRAW else 2
        cv2.circle(frame, cursor, 10, (0, 220, 255), filled)


def main():
    """Free-drawing mode: draw with gestures, press q to quit."""
    cap = open_camera()
    tracker = HandTracker()

    # Read one frame first: the configured resolution is a request, not a
    # guarantee, and the canvas must match what the camera actually returns.
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Camera opened but returned no frame.")
    height, width = frame.shape[:2]
    board = Whiteboard(width, height)

    print(f"Camera running at {width}x{height}")
    print("index finger = draw | fist = pause | two fingers = move | "
          "open palm = clear | q = quit")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Mirror the image so that moving the hand right moves the stroke
        # right. Without this the interaction feels inverted.
        frame = cv2.flip(frame, 1)

        landmarks, result = tracker.find(frame)
        mode, cursor = board.update(landmarks)

        display = board.overlay(frame)
        tracker.draw_skeleton(display, result)
        draw_hud(display, [f"mode: {mode}"], cursor, mode)

        cv2.imshow("Air whiteboard", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
