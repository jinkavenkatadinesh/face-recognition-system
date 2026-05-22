# 👤 Face Detection & Recognition Pipeline

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-green.svg?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.4%2B-orange.svg?style=flat-square&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=flat-square)](LICENSE)

An intelligent, hybrid face detection pipeline that combines modern **Deep Learning (MTCNN)** and classical **Computer Vision (Haar Cascade)** approaches. The system handles end-to-end processing, from robust image preprocessing (denoising and CLAHE brightness/contrast normalization) to visual annotations and automatic PowerPoint generation.

---

## 🌟 Key Features

*   **Hybrid Detection Pipeline:** Uses deep learning-based **MTCNN** (Multi-task Cascaded Convolutional Networks) for high-accuracy face and landmark localization, with an automated **Haar Cascade** fallback for resource-constrained scenarios or extremely fast processing.
*   **Robust Image Preprocessing:**
    *   *Adaptive Resizing:* Automatically scales down high-resolution images to a maximum width of `800px` for optimal processing speed.
    *   *Color Denoising:* Applies Non-Local Means Denoising (`fastNlMeansDenoisingColored`) to remove image grain and sensor noise.
    *   *Adaptive Contrast Normalization (CLAHE):* Converts images to the `LAB` color space and performs Contrast Limited Adaptive Histogram Equalization on the Lightness (`L`) channel to normalize faces under extreme shadows or low-light conditions.
*   **Automated Dataset Expander:** Includes a script to pull curated, high-quality, open-source face images from Pexels (e.g., side profiles, groups, family portraits, low-light) to thoroughly test detection accuracy.
*   **Automated Slide Generator:** A script using `python-pptx` programmatically compiles a premium-themed PowerPoint presentation showcasing the project's architecture, methodology, and comparative analysis.

---

## 📂 Project Structure

```bash
FaceRecognitionProject/
├── dataset/
│   ├── raw/               # Raw test images (input)
│   ├── output/            # Preprocessed and annotated images (output)
│   └── test.jpg           # Initial system setup verification image
├── models/                # Reserved for trained weight models
├── scripts/
│   ├── test_setup.py      # Verifies local system environment & libraries
│   ├── expand_dataset.py  # Fetches additional sample face images from Pexels
│   ├── face_detection.py  # Fully preprocessed detection pipeline (MTCNN + Haar fallback)
│   ├── mtcnn_detection.py # Pure MTCNN detection script
│   └── create_ppt.py      # Programmatic PowerPoint generation script
├── .gitignore             # Git exclusion rules
├── requirements.txt       # Project python dependencies
└── README.md              # Project documentation (this file)
```

---

## ⚙️ Installation & Setup

Ensure you have **Python 3.8+** installed. Then, follow these steps:

### 1. Clone & Navigate to the Repository
```bash
git clone https://github.com/jinkavenkatadinesh/face-recognition-system.git
cd face-recognition-system/FaceRecognitionProject
```

### 2. Set Up a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Step 1: Verify the Installation
Run the setup script to verify OpenCV, NumPy, and TensorFlow are running correctly and to test basic image loading:
```bash
python scripts/test_setup.py
```

### Step 2: Download Test Images
Use the dataset expander to pull a set of challenging face detection test samples:
```bash
python scripts/expand_dataset.py
```

### Step 3: Run the Detection Pipeline
Execute the main hybrid face detection pipeline. This script will preprocess raw images, attempt MTCNN detection, fall back to Haar Cascades if no faces are found, and save annotated outputs:
```bash
python scripts/face_detection.py
```

### Step 4: Generate the Presentation
Build the professional PowerPoint slide deck dynamically:
```bash
python scripts/create_ppt.py
```
This saves a sleek presentation file: `Face_Recognition_Project.pptx` in the project root.

---

## 📊 Comparison: Haar Cascade vs. MTCNN

| Metric | Haar Cascade | MTCNN (Deep Learning) |
| :--- | :--- | :--- |
| **Speed** | ⚡ Extremely Fast | 🐢 Slower (Highly optimized with GPU) |
| **Accuracy** | Moderate (Misses non-frontal faces) | ✅ Extremely High |
| **Pose Tolerance** | Primarily Frontal | Multi-angle (Side-profiles, tilted) |
| **Lighting Sensitivity** | High (Degrades in low light) | Robust (Handles shadows & low-contrast) |
| **Facial Landmarks** | ❌ None | ✅ 5-point landmarks (Eyes, nose, mouth) |
| **Dependencies** | OpenCV only | TensorFlow + MTCNN package |

---

## 🔮 Future Roadmap

1.  **Face Recognition:** Integrate deep embedding extractors (like **FaceNet** or **ArcFace**) with a database to perform face identification (matching detected faces to names).
2.  **Real-Time Video Stream:** Support live video/webcam processing with multi-object tracking.
3.  **FastAPI REST Web App:** Construct an API server allowing users to upload images and receive JSON-formatted face coordinates and landmarks.
4.  **Web UI:** Develop a modern frontend (React or simple Streamlit) for user-friendly testing.
