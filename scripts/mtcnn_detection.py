import os
import cv2
from mtcnn import MTCNN

# ===============================
# Paths
# ===============================
input_folder = os.path.join("..", "dataset", "raw")
output_folder = os.path.join("..", "dataset", "output")

os.makedirs(output_folder, exist_ok=True)

# ===============================
# Initialize Detector
# ===============================
detector = MTCNN()

print("✅ MTCNN detector initialized.\n")

# ===============================
# Process Images
# ===============================
for filename in os.listdir(input_folder):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(input_folder, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"⚠ Skipping {filename}")
        continue

    print(f"\nProcessing: {filename}")

    # Convert BGR to RGB (MTCNN requires RGB)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces
    results = detector.detect_faces(rgb_image)

    print(f"Faces detected: {len(results)}")

    # Draw bounding boxes
    for result in results:
        x, y, w, h = result['box']
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save output image
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, image)

print("\n✅ Face detection completed using MTCNN.")
