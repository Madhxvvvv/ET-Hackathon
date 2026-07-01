"""
predict.py
----------
Inference pipeline for Counterfeit Currency Detection.

Day 2 TODO list
~~~~~~~~~~~~~~~
- [ ] Load EfficientNet checkpoint from models/ directory.
- [ ] Implement preprocessing transform (resize, normalise to ImageNet stats).
- [ ] Implement single-image predict() returning label + confidence.
- [ ] Implement batch_predict() for efficiency when processing multiple images.
- [ ] Add GradCAM visualisation for explainability.
- [ ] Cache the loaded model so repeated calls don't reload weights.
- [ ] Expose a FastAPI-compatible function signature for Module 2 integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# TODO Day 2: import torch, PIL, numpy, etc.


@dataclass
class PredictionResult:
    """
    Output of a single inference call.

    Attributes:
        label: ``"genuine"`` or ``"counterfeit"``.
        confidence: Model's softmax probability for the predicted class (0–1).
        image_path: Source image path (for traceability in batch processing).
    """

    label: str
    confidence: float
    image_path: Path


class CurrencyPredictor:
    """
    Stateful inference wrapper that keeps the model loaded between calls.

    TODO Day 2: implement __init__ (load checkpoint + build transform),
    predict(), batch_predict(), and _preprocess().
    """

    def __init__(self, model_path: Path) -> None:
        # TODO Day 2: load EfficientNet weights from model_path.
        raise NotImplementedError("CurrencyPredictor is not yet implemented.")

    def predict(self, image_path: Path) -> PredictionResult:
        """
        Classify a single currency note image.

        Args:
            image_path: Absolute path to a .jpg / .png note image.

        Returns:
            PredictionResult with label and confidence score.
        """
        raise NotImplementedError

    def batch_predict(self, image_paths: list[Path]) -> list[PredictionResult]:
        """
        Classify a batch of images efficiently using a single forward pass.

        Prefer this over calling predict() in a loop when processing >1 image.
        """
        raise NotImplementedError

    def _preprocess(self, image_path: Path):  # -> torch.Tensor
        """
        Load image, resize to model input size, normalise, and add batch dim.
        """
        raise NotImplementedError
