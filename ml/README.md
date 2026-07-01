# ML — Counterfeit Currency Detection

**Owner:** Person 1 | Part of: Digital Public Safety Platform — ET AI Hackathon 2026

## What this module does

Classifies Indian currency notes as **genuine** or **counterfeit** from a photograph.
The pipeline covers dataset preparation, image augmentation, and (Day 2) EfficientNet fine-tuning and inference.

---

## Stack

| Library | Purpose |
|---|---|
| PyTorch + torchvision | Model training & inference (Day 2) |
| EfficientNet-B0 | Backbone — pretrained on ImageNet, fine-tuned on currency data |
| Albumentations | Augmentation pipeline |
| OpenCV | Image I/O, resize, hash |
| python-dotenv | Config from environment variables |

---

## Folder structure

```
ml/
├── configs/
│   └── dataset_config.py   # All hyperparameters and paths; override via ML_* env vars
├── datasets/
│   ├── raw_images/         # Source photographs — NOT committed to git
│   │   ├── genuine/        # Authentic notes
│   │   └── counterfeit/    # Fake notes
│   ├── augmented/          # Output of augment.py — NOT committed
│   ├── train/              # Output of prepare_dataset.py
│   ├── validation/         # Output of prepare_dataset.py
│   └── test/               # Output of prepare_dataset.py
├── models/                 # Saved checkpoints (.pt) — NOT committed
├── logs/                   # Runtime logs (ml.log) — NOT committed
├── scripts/
│   ├── augment.py          # Runs the augmentation pipeline
│   └── prepare_dataset.py  # Validates, deduplicates, and splits the dataset
├── src/
│   ├── utils/
│   │   ├── image_utils.py  # Pure image helpers (load, save, hash, resize, collect)
│   │   └── logging_utils.py# Centralised logger factory
│   ├── training/
│   │   ├── model.py        # CounterfeitDetector class skeleton (Day 2)
│   │   └── train.py        # Trainer class skeleton (Day 2)
│   └── inference/
│       └── predict.py      # CurrencyPredictor class skeleton (Day 2)
├── tests/                  # pytest suite — covers Day 1 pipeline
├── requirements.txt
└── README.md
```

---

## Photographing currency notes

### Setup

- **Background:** Plain white or light grey — avoid patterned surfaces.
- **Lighting:** Diffuse natural light or two soft-box lamps at 45° angles. Avoid direct flash (creates hotspots that mask security features).
- **Camera distance:** Note fills ~80 % of the frame. Typical phone: 20–25 cm above the note.
- **Orientation:** Both portrait and landscape shots — the pipeline handles rotation.
- **Focus:** Tap to focus on the centre of the note before capturing.
- **Quantity:** Aim for ≥15 genuine and ≥15 counterfeit notes per denomination.

### Naming convention

```
<denomination>_<class>_<sequence>.jpg

Examples:
  500_genuine_001.jpg
  500_counterfeit_003.jpg
  100_genuine_012.jpg
```

Place files under `datasets/raw_images/genuine/` or `datasets/raw_images/counterfeit/`.

### Supported denominations

₹10 · ₹20 · ₹50 · ₹100 · ₹200 · ₹500 · ₹2000

---

## Setup

```bash
cd ml
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env           # Edit ML_* vars if you need to override paths
```

---

## Day 1 workflow

### 1 — Add raw images

```
datasets/raw_images/
  genuine/   ← drop genuine note photos here
  counterfeit/ ← drop counterfeit note photos here
```

### 2 — Augment (generate ~500 images from ~30 source images)

```bash
python -m scripts.augment
# Options:
#   --source PATH   override raw_images directory
#   --dest   PATH   override augmented output directory
#   --count  N      augmentations per image (default 17)
```

### 3 — Prepare dataset (validate → deduplicate → split)

```bash
python -m scripts.prepare_dataset
# Options:
#   --source      PATH   override raw_images directory
#   --train-ratio 0.70   fraction for training
#   --val-ratio   0.15   fraction for validation
#   --seed        42     random seed
```

This writes files into `datasets/train/`, `datasets/validation/`, and `datasets/test/`,
and saves a JSON report to `logs/prepare_dataset_report.json`.

---

## Configuration

All settings live in `configs/dataset_config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `ML_RAW_IMAGES_DIR` | `datasets/raw_images` | Source image root |
| `ML_AUGMENTED_DIR` | `datasets/augmented` | Augmented output |
| `ML_TRAIN_RATIO` | `0.70` | Training split fraction |
| `ML_VAL_RATIO` | `0.15` | Validation split fraction |
| `ML_TEST_RATIO` | `0.15` | Test split fraction |
| `ML_AUGMENTATIONS_PER_IMAGE` | `17` | Variants per source image |
| `ML_RANDOM_SEED` | `42` | Reproducibility seed |
| `ML_LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Tests

### Install and run

```bash
pip install pytest pytest-cov   # already in requirements.txt

# From the ml/ directory:
pytest tests/ -v
pytest tests/ -v --cov=src --cov=scripts --cov-report=term-missing

# Run a single test file:
pytest tests/test_prepare_dataset.py -v

# Run a single test by name:
pytest tests/test_augmentation.py -v -k "test_correct_file_count"
```

### What is covered

| Test file | Covers |
|---|---|
| `test_config.py` | Config loading, split ratio validation, env overrides, frozen dataclass |
| `test_image_utils.py` | Valid/corrupted/empty images, hashing, resize, load/save, path collection |
| `test_prepare_dataset.py` | Validation, deduplication, split counts, reproducibility, file copying |
| `test_augmentation.py` | Pipeline output shape, count correctness, file integrity, subfolder preservation |

### Expected output

```
tests/test_config.py ............           [PASSED]
tests/test_image_utils.py .............     [PASSED]
tests/test_prepare_dataset.py ..........    [PASSED]
tests/test_augmentation.py .........        [PASSED]
```

All tests should pass without any network access or GPU.

---

## Day 2 plan (do not implement today)

- Implement `CounterfeitDetector` in `src/training/model.py` (EfficientNet-B0, 2-class head).
- Implement `Trainer` in `src/training/train.py` (mixed-precision, LR scheduler, early stopping).
- Implement `CurrencyPredictor` in `src/inference/predict.py` (GradCAM explainability).
- Expose `/api/v1/currency/detect` through the backend (Person 2 integration).
- Uncomment `torch` and `torchvision` in `requirements.txt`.
