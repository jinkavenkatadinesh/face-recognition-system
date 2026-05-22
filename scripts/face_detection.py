import cv2
import os
import numpy as np
from mtcnn import MTCNN

# ===============================
# Paths
# ===============================
input_folder = os.path.join("..", "dataset", "raw")
output_folder = os.path.join("..", "dataset", "output")

os.makedirs(output_folder, exist_ok=True)

# ===============================
# Initialize Detectors
# ===============================

# Primary: MTCNN (Deep Learning - more accurate)
mtcnn_detector = MTCNN()
print("✅ MTCNN detector initialized.")

# Fallback: Haar Cascade
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
print("✅ Haar Cascade loaded.\n")

# ===============================
# Preprocessing Settings
# ===============================
MAX_WIDTH = 800          # Resize large images to this max width
DENOISE_STRENGTH = 10    # Denoising filter strength
CLAHE_CLIP = 2.0         # CLAHE contrast limit
CLAHE_GRID = (8, 8)      # CLAHE grid size
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
        print(f"⚠ Skipping {filename} (Invalid image)")
        continue

    print(f"\n{'='*45}")
    print(f"  Processing: {filename}")
    print(f"{'='*45}")
    print(f"  Original Size: {image.shape[1]}x{image.shape[0]}")

    # ========== PREPROCESSING ==========

    # STEP 1: Resize large images
    h, w = image.shape[:2]
    if w > MAX_WIDTH:
        scale = MAX_WIDTH / w
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        print(f"  ↳ Resized to: {image.shape[1]}x{image.shape[0]}")
    else:
        print(f"  ↳ No resizing needed (within {MAX_WIDTH}px)")

    # STEP 2: Denoise
    denoised = cv2.fastNlMeansDenoisingColored(image, None, DENOISE_STRENGTH, DENOISE_STRENGTH, 7, 21)
    print(f"  ↳ Denoising applied")

    # STEP 3: Brightness normalization on color image
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_GRID)
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    print(f"  ↳ CLAHE contrast enhancement applied")

    # ========== FACE DETECTION ==========

    # Primary: MTCNN (deep learning, more accurate)
    rgb_image = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)
    results = mtcnn_detector.detect_faces(rgb_image)

    # Filter by confidence
    faces_mtcnn = [r for r in results if r['confidence'] >= MTCNN_CONFIDENCE]

    print(f"\n  🔍 MTCNN detected: {len(faces_mtcnn)} faces (confidence >= {MTCNN_CONFIDENCE})")

    # Draw MTCNN detections (green boxes)
    for result in faces_mtcnn:
        x, y, fw, fh = result['box']
        confidence = result['confidence']
        # Fix negative coordinates
        x, y = abs(x), abs(y)
        cv2.rectangle(image, (x, y), (x + fw, y + fh), (0, 255, 0), 2)
        cv2.putText(image, f"{confidence:.2f}", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # Fallback: If MTCNN finds nothing, try Haar Cascade
    if len(faces_mtcnn) == 0:
        print("  ⚠ MTCNN found no faces, trying Haar Cascade...")
        gray = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces_haar = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(20, 20)
        )
        print(f"  🔍 Haar Cascade detected: {len(faces_haar)} faces")
        for (x, y, fw, fh) in faces_haar:
            cv2.rectangle(image, (x, y), (x + fw, y + fh), (255, 165, 0), 2)

    # Save output
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, image)
    print(f"  💾 Saved to: {output_path}")

print("\n✅ Face detection with preprocessing completed.")
