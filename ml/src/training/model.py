"""
model.py
--------
EfficientNet model definition for Counterfeit Currency Detection.

Day 2 TODO list
~~~~~~~~~~~~~~~
- [ ] Load EfficientNet-B0 (or B2/B3 if accuracy demands it) from
      torchvision.models with IMAGENET1K_V1 weights.
- [ ] Freeze all layers except the classifier head for first N epochs
      (feature extraction phase), then unfreeze for full fine-tuning.
- [ ] Replace the final Linear layer with a 2-class head.
- [ ] Add dropout before the classifier for regularisation.
- [ ] Implement get_feature_extractor() for GradCAM support in predict.py.
- [ ] Export to ONNX for potential mobile/edge deployment.
"""

from __future__ import annotations

from pathlib import Path

# TODO Day 2: import torch, torch.nn, torchvision.models, etc.


class CounterfeitDetector:
    """
    EfficientNet-based binary classifier: genuine vs. counterfeit currency.

    TODO Day 2: inherit from torch.nn.Module and implement:
        - __init__(num_classes=2, freeze_backbone=True)
        - forward(x)
        - freeze_backbone() / unfreeze_backbone()
        - get_feature_extractor() for GradCAM
    """

    def __init__(self, num_classes: int = 2, freeze_backbone: bool = True) -> None:
        # TODO Day 2: super().__init__(); load EfficientNet; swap head.
        raise NotImplementedError("CounterfeitDetector is not yet implemented.")

    def forward(self, x):  # x: torch.Tensor -> torch.Tensor
        """Standard forward pass. Input: (B, C, H, W). Output: (B, num_classes) logits."""
        raise NotImplementedError

    def freeze_backbone(self) -> None:
        """Freeze all parameters except the classifier head (feature-extraction phase)."""
        raise NotImplementedError

    def unfreeze_backbone(self) -> None:
        """Unfreeze all parameters for end-to-end fine-tuning."""
        raise NotImplementedError

    def save(self, path: Path) -> None:
        """Save model state_dict to *path*."""
        raise NotImplementedError

    @classmethod
    def load(cls, path: Path, num_classes: int = 2) -> "CounterfeitDetector":
        """Instantiate a CounterfeitDetector from a saved state_dict."""
        raise NotImplementedError
