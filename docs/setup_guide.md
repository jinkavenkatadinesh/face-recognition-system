# ⚙️ Setup & Troubleshooting Guide

This guide provides exhaustive, operating-system-specific installation steps and answers to common troubleshooting questions for the **Face Detection & Recognition Pipeline**.

---

## 💻 OS-Specific Installation Guide

Ensure you have **Python 3.8+** installed before proceeding.

### 🔷 Windows Setup
1.  **Open PowerShell or CMD** (as Administrator if resolving virtual environment permissions).
2.  **Navigate to repository**:
    ```powershell
    cd C:\face regonization system\FaceRecognitionProject
    ```
3.  **Establish Virtual Environment**:
    ```powershell
    python -m venv venv
    ```
4.  **Set Execution Policy** (if PowerShell prevents activation):
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```
5.  **Activate environment**:
    ```powershell
    .\venv\Scripts\activate
    ```
6.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

### 🍎 macOS Setup
1.  **Open Terminal**.
2.  **Navigate to repository**:
    ```bash
    cd face-recognition-system/FaceRecognitionProject
    ```
3.  **Establish Virtual Environment**:
    ```bash
    python3 -m venv venv
    ```
4.  **Activate environment**:
    ```bash
    source venv/bin/activate
    ```
5.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Apple Silicon users (M1/M2/M3/M4) may see faster MTCNN execution by installing native tensorflow packages if desired).*

### 🐧 Linux Setup (Ubuntu/Debian)
1.  **Open Shell terminal**.
2.  **Ensure system libraries are present**:
    OpenCV relies on system graphics and hardware acceleration libraries:
    ```bash
    sudo apt-get update
    sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
    ```
3.  **Create and activate environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  **Install packages**:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

---

## 🛠️ Verification Checklist

Run these commands sequentially from the root of `FaceRecognitionProject` with your virtual environment active to verify correctness:

1.  **Environment Check**:
    ```bash
    python scripts/test_setup.py
    ```
    *Verifies that OpenCV, NumPy, and TensorFlow are running correctly and successfully loads the baseline `test.jpg` file.*
2.  **Download Sample Dataset**:
    ```bash
    python scripts/expand_dataset.py
    ```
    *Downloads challenging mock images into `dataset/raw/` to test profile faces, low-light variations, and multi-person scenes.*
3.  **Run Face Detection pipeline**:
    ```bash
    python scripts/face_detection.py
    ```
    *Executes the pipeline, processes all downloaded files in the raw folder, applies modular CLAHE/Denoising, triggers detections, and saves outputs to `dataset/output/`.*
4.  **Launches Streamlit Web Dashboard**:
    ```bash
    streamlit run app.py
    ```
    *Launches the premium UI in your browser (typically `http://localhost:8501`).*
5.  **Slide presentation compilation**:
    ```bash
    python scripts/create_ppt.py
    ```
    *Programmatically compiles `Face_Recognition_Project.pptx` in your root.*

---

## ❓ Troubleshooting & FAQs

### Q1: `ModuleNotFoundError: No module named 'src'`
**Cause**: The Python path does not include the root directory of your project when calling scripts.
**Solution**: The scripts inside `scripts/` have been updated to pro-actively inject the correct parent path into `sys.path`. If you face this in custom code, make sure to execute your python calls from the `FaceRecognitionProject` root, or add:
```python
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Q2: Streamlit uploader returns: `Error: Could not decode uploaded image`
**Cause**: The uploaded file is either empty or in an unsupported format.
**Solution**: Ensure your uploaded images are standard `.png`, `.jpg`, or `.jpeg` formats. Try downloading a fresh image from Pexels and dragging it into the dropzone.

### Q3: `cv2.error: OpenCV(4.x.x) ... OpenCV-headless does not support imshow`
**Cause**: `test_setup.py` calls `cv2.imshow` to display the window, but you are running inside a headless terminal environment or using `opencv-python-headless` from `requirements.txt`.
**Solution**: This is expected behavior for `test_setup.py` when running headlessly. The main pipeline (`scripts/face_detection.py`) and Streamlit web application (`app.py`) do not use `cv2.imshow` and will run without any issues!
