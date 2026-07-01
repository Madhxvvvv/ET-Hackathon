"""
train.py
--------
EfficientNet fine-tuning pipeline for Counterfeit Currency Detection.

Day 2 TODO list
~~~~~~~~~~~~~~~
- [ ] Implement CurrencyDataset (torchvision ImageFolder or custom Dataset).
- [ ] Load EfficientNet-B0 from torchvision.models with pretrained weights.
- [ ] Replace classifier head: nn.Linear(features, len(CLASS_LABELS)).
- [ ] Implement training loop with:
      - Mixed-precision (torch.cuda.amp.autocast).
      - Gradient clipping.
      - Learning-rate scheduler (CosineAnnealingLR or ReduceLROnPlateau).
- [ ] Implement validation loop with accuracy + AUC metrics.
- [ ] Save best checkpoint to models/ (by validation AUC).
- [ ] Add early stopping.
- [ ] Log metrics with TensorBoard or W&B.
"""

from __future__ import annotations

from pathlib import Path

# TODO Day 2: import torch, torchvision, etc.


class CurrencyDataset:
    """
    PyTorch Dataset for currency note images.

    Expects the dataset root to follow ImageFolder convention::

        root/
          genuine/
            img1.jpg
            img2.jpg
          counterfeit/
            img3.jpg

    TODO Day 2: Inherit from torch.utils.data.Dataset and implement
    __len__, __getitem__, and optional WeightedRandomSampler support
    to handle class imbalance.
    """

    def __init__(self, root: Path, transform=None) -> None:
        # TODO Day 2: implement
        self.root = root
        self.transform = transform
        raise NotImplementedError("CurrencyDataset is not yet implemented.")


class Trainer:
    """
    Encapsulates the full training lifecycle.

    TODO Day 2: implement __init__, fit(), _train_epoch(), _val_epoch(),
    _save_checkpoint(), and _load_checkpoint().
    """

    def __init__(self, config) -> None:
        # TODO Day 2: accept TrainConfig dataclass; set up model, optimiser, schedulers.
        raise NotImplementedError("Trainer is not yet implemented.")

    def fit(self, train_dataset: CurrencyDataset, val_dataset: CurrencyDataset) -> None:
        """Run the full training loop for the configured number of epochs."""
        raise NotImplementedError

    def _train_epoch(self) -> dict[str, float]:
        """One forward+backward pass over the training set. Returns metric dict."""
        raise NotImplementedError

    def _val_epoch(self) -> dict[str, float]:
        """Evaluation pass over the validation set. Returns metric dict."""
        raise NotImplementedError

    def _save_checkpoint(self, epoch: int, metrics: dict[str, float]) -> None:
        """Persist model weights + optimizer state to models/."""
        raise NotImplementedError

    def _load_checkpoint(self, path: Path) -> None:
        """Restore model + optimizer from a checkpoint file."""
        raise NotImplementedError
