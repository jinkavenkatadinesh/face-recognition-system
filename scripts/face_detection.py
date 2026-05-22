import os
import sys
import cv2

# Ensure the parent directory is in the path so we can import src
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "..")))

from src import HybridFaceDetector, preprocess_pipeline

# ===============================
# Paths
# ===============================
input_folder = os.path.abspath(os.path.join(script_dir, "..", "dataset", "raw"))
output_folder = os.path.abspath(os.path.join(script_dir, "..", "dataset", "output"))

os.makedirs(output_folder, exist_ok=True)

# ===============================
# Initialize Detectors
# ===============================
detector = HybridFaceDetector()
print("[+] Hybrid Face Detector initialized (MTCNN + Haar fallback).")

# ===============================
# Preprocessing Settings
# ===============================
MAX_WIDTH = 800          # Resize large images to this max width
DENOISE_STRENGTH = 10    # Denoising filter strength
CLAHE_CLIP = 2.0         # CLAHE contrast limit
MTCNN_CONFIDENCE = 0.90  # Minimum confidence for MTCNN

# ===============================
# Process Images
# ===============================
for filename in os.listdir(input_folder):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(input_folder, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"[!] Skipping {filename} (Invalid image)")
        continue

    print(f"\n{'='*45}")
    print(f"  Processing: {filename}")
    print(f"{'='*45}")
    print(f"  Original Size: {image.shape[1]}x{image.shape[0]}")

    # ========== PREPROCESSING ==========
    preprocessed, logs = preprocess_pipeline(
        image.copy(),
        enable_resize=True,
        max_width=MAX_WIDTH,
        enable_denoise=True,
        denoise_strength=DENOISE_STRENGTH,
        enable_clahe=True,
        clahe_clip=CLAHE_CLIP
    )
    for log in logs:
        print(f"  -> {log}")

    # ========== FACE DETECTION ==========
    faces_detected, annotated_image, engine_used = detector.detect(
        preprocessed,
        mode="hybrid",
        mtcnn_confidence=MTCNN_CONFIDENCE,
        haar_scale=1.05,
        haar_neighbors=3
    )

    print(f"  -> Detection Core: {engine_used}")
    print(f"  -> Detected: {len(faces_detected)} faces")

    # Save output
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, annotated_image)
    print(f"  -> Saved to: {output_path}")

print("\n[+] Face detection with preprocessing completed.")
