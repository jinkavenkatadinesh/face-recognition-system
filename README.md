# 👤 Intelligent Face Detection & Recognition Pipeline

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-green.svg?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.4%2B-orange.svg?style=flat-square&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=flat-square)](LICENSE)

An intelligent, production-ready face detection and preprocessing pipeline that combines **Deep Learning (MTCNN)** and classical **Computer Vision (Haar Cascade)** approaches. The system handles end-to-end processing: from adaptive rescaling, color denoising, and CLAHE illumination compensation, to interactive visualization dashboards and automatic PowerPoint generation.

---

## 🌟 Key Features

*   **Hybrid Dual-Core Detection Engine:** Utilizes highly accurate deep learning-based **MTCNN** as the primary tracker (returning 5 facial landmarks), with a lightning-fast classical **Haar Cascade** fallback for resource-constrained environments.
*   **Modular Image Preprocessing Library:**
    *   *Adaptive Rescale:* Protects processing servers from latency spikes by automatically downscaling oversized images.
    *   *Non-Local Means Denoising:* Eliminates sensor noise and compression grain.
    *   *CLAHE Illumination Normalization:* Converts matrices into the LAB color space, equalizing brightness/contrast on the Lightness channel locally to handle extreme shadows.
*   **Premium Web Application:** Run an interactive, glassmorphism-styled Streamlit interface to visualize parameters, test sliders, and inspect face analytics in real-time.
*   **CLI Automations & Slides Compilation:** Fetch curated, high-quality test images from open sources automatically and build dynamic, professional PowerPoint slide reports programmatically.

---

## 📂 Project Architecture Layout

The codebase has been refactored into a high-standard, professional open-source repository layout:

```bash
FaceRecognitionProject/
├── dataset/                  # Test dataset directory
│   ├── raw/                  # Downloaded test inputs
│   └── output/               # preprocessed and annotated outputs
├── docs/                     # Comprehensive documentation guides
│   ├── architecture.md       # Pipeline workflows, mathematical grids, and fallbacks
│   └── setup_guide.md        # Environment setup for CLI & Web app
├── models/                   # Reserved folder for deep trained neural weights
├── scripts/                  # Command-line utility automations
│   ├── test_setup.py         # Diagnostic environment validation script
│   ├── expand_dataset.py     # Pulls face images from public-domain providers
│   ├── face_detection.py     # Batch CLI pipeline script (powered by src/)
│   └── create_ppt.py         # Programmatic slide deck generation script
├── src/                      # [NEW] Reusable core package library
│   ├── __init__.py           # Declares package APIs
│   ├── detector.py           # Core HybridFaceDetector engine
│   └── utils.py              # Preprocessing algorithms (CLAHE, scale, noise)
├── .gitignore                # Optimized exclusion guidelines
├── ABOUT.md                  # Deep technical landscape justifications
├── CHANGELOG.md              # Semantic version changelog details
├── CODE_OF_CONDUCT.md        # Standard Contributor Covenant CoC
├── CONTRIBUTING.md           # Coding style, conventions, and PR guidelines
├── LICENSE                   # Open-source MIT License
├── README.md                 # Project roadmap overview (this document)
└── requirements.txt          # Defined python package dependencies
```

---

## ⚙️ Installation & Setup

Ensure you have **Python 3.8+** installed. Detailed operating-system steps are available in the [Setup Guide](file:///C:/face%20regonization%20system/FaceRecognitionProject/docs/setup_guide.md).

### 1. Clone & Navigate
```bash
git clone https://github.com/jinkavenkatadinesh/face-recognition-system.git
cd face-recognition-system/FaceRecognitionProject
```

### 2. Configure Virtual Environment & Packages
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

---

## 🚀 Execution Routines

With your virtual environment active, follow these steps to run the pipeline:

### Step 1: Diagnose Installation
```bash
python scripts/test_setup.py
```

### Step 2: Download Test Dataset
```bash
python scripts/expand_dataset.py
```

### Step 3: Run Batch CLI Detection
```bash
python scripts/face_detection.py
```
*Outputs are saved to `dataset/output/`.*

### Step 4: Run Streamlit Web Application
Launch the responsive, glassmorphism-styled dashboard:
```bash
streamlit run app.py
```
*This opens your browser automatically at `http://localhost:8501` to drag-and-drop custom images.*

### Step 5: Programmatic Presentation slides
```bash
python scripts/create_ppt.py
```
*Compiles system performance into a sleek `Face_Recognition_Project.pptx` deck in the root folder.*

---

## 🏛️ Comprehensive Guides

-   **Deep Tech & Mathematical Logic**: See [docs/architecture.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/docs/architecture.md) for structural schemas, algorithm matrices, and fallback thresholds.
-   **Troubleshooting & Setup**: See [docs/setup_guide.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/docs/setup_guide.md) for OS-specific support, execution policies, and headless libraries.
-   **Contribution Guidelines**: See [CONTRIBUTING.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/CONTRIBUTING.md) for PEP 8, conventional commits, and review guidelines.

---

## 📜 License & Conduct

-   This project is licensed under the open-source **MIT License** - see [LICENSE](file:///C:/face%20regonization%20system/FaceRecognitionProject/LICENSE) for details.
-   We hold our community to premium standards of collaboration - see [CODE_OF_CONDUCT.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/CODE_OF_CONDUCT.md).
