# 🤝 Contributing to Face Detection & Recognition Pipeline

Thank you for choosing to contribute! This document outlines guidelines, standards, and practices to ensure smooth integration with our codebase.

---

## 🚀 Setting Up Your Developer Environment

### 1. Fork and Clone the Repository
```bash
git clone https://github.com/jinkavenkatadinesh/face-recognition-system.git
cd face-recognition-system/FaceRecognitionProject
```

### 2. Configure Virtual Environment
We recommend isolating your system dependencies using `venv`:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Packages
Install dependencies along with developer packages:
```bash
pip install -r requirements.txt
```

---

## 📐 Coding Standards & Guidelines

To maintain clean architecture and readable history, please adhere to:
- **Style Standard**: Conform strictly to **PEP 8** style guidelines.
- **Type Annotations**: Provide type annotations for all new method signatures.
- **Documentation**: Write descriptive docstrings using the Google Python Style format.
- **No Duplicate Logic**: Keep the codebase DRY (Don't Repeat Yourself). Extract utility processes to [src/utils.py](file:///C:/face%20regonization%20system/FaceRecognitionProject/src/utils.py) and main classification cores to [src/detector.py](file:///C:/face%20regonization%20system/FaceRecognitionProject/src/detector.py).

---

## 💬 Git Commit Conventions

We enforce standard **Conventional Commits** to keep history understandable:
*   `feat: ...` - Introduces a new feature or capability.
*   `fix: ...` - Fixes an issue or syntax error.
*   `refactor: ...` - Modifies code without altering outward-facing behavior.
*   `docs: ...` - Updates READMEs, internal API guides, or documentation.
*   `style: ...` - Fixes formatting or spacing (no functional changes).
*   `test: ...` - Adds, refactors, or fixes test coverage.

Example:
```bash
git commit -m "feat: integrate DeepFace embedding extraction for facial recognition"
```

---

## 🛠️ Pull Request Checklist

Before submitting a Pull Request, ensure that you have checked off the following:
1.  **Code Validity**: Ensure the code runs flawlessly on your local machine.
2.  **Lint Check**: Run your preferred linter (e.g. `flake8` or `black`) on modified scripts.
3.  **Local CLI Verification**: Run the standard image pipeline:
    ```bash
    python scripts/face_detection.py
    ```
4.  **Local App Verification**: Run the Streamlit interface to verify UI integrity:
    ```bash
    streamlit run app.py
    ```
5.  **Documentation Alignments**: Ensure your modifications are described in [CHANGELOG.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/CHANGELOG.md) and update corresponding guides in the `docs/` folder.
