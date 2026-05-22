# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-05-22

### Added
- Created [src/](file:///C:/face%20regonization%20system/FaceRecognitionProject/src) core modular package to house reusable utilities.
- Created [src/utils.py](file:///C:/face%20regonization%20system/FaceRecognitionProject/src/utils.py) containing robust functions for image scale handling, color denoising, and Contrast Limited Adaptive Histogram Equalization (CLAHE).
- Created [src/detector.py](file:///C:/face%20regonization%20system/FaceRecognitionProject/src/detector.py) containing a unified `HybridFaceDetector` class supporting MTCNN, Haar Cascades, and deep fallback workflows.
- Created `docs/` folder containing exhaustive guides:
  - [docs/architecture.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/docs/architecture.md) detailing the algorithmic pipeline.
  - [docs/setup_guide.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/docs/setup_guide.md) highlighting setup details.
- Added repository-wide standards documents: [ABOUT.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/ABOUT.md), [CONTRIBUTING.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/CONTRIBUTING.md), [LICENSE](file:///C:/face%20regonization%20system/FaceRecognitionProject/LICENSE), and [CODE_OF_CONDUCT.md](file:///C:/face%20regonization%20system/FaceRecognitionProject/CODE_OF_CONDUCT.md).

### Changed
- Refactored [app.py](file:///C:/face%20regonization%20system/FaceRecognitionProject/app.py) to remove duplicate preprocessing and detection cascades, replacing them with clean calls to the new `src/` modules.
- Refactored [scripts/face_detection.py](file:///C:/face%20regonization%20system/FaceRecognitionProject/scripts/face_detection.py) to import core routines from `src/`, resolving path resolution bugs to allow execution from any command-line context.
- Optimized [.gitignore](file:///C:/face%20regonization%20system/FaceRecognitionProject/.gitignore) to exclude generated PPT files, temporary testing assets, and raw downloads while preserving essential mockups.

---

## [1.0.0] - 2026-05-15

### Added
- Initial release of the Face Detection Pipeline.
- Integrated **MTCNN Deep Learning** model core.
- Integrated **Haar Cascade** classical model core as secondary engine.
- Implemented **Streamlit Web GUI Dashboard** (`app.py`) featuring sliders for CLAHE and confidence cutoffs, and side-by-side comparative views.
- Added programmatic PowerPoint slide generator (`scripts/create_ppt.py`) utilizing `python-pptx` to compile slide presentations of system statistics.
- Added custom mock database expansion tool (`scripts/expand_dataset.py`) pulling raw face images from public-domain providers.
