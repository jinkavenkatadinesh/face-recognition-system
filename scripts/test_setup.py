import cv2
import numpy as np
import tensorflow as tf
import os

print("OpenCV Version:", cv2.__version__)
print("NumPy Version:", np.__version__)
print("TensorFlow Version:", tf.__version__)

# Image path
image_path = os.path.join("..", "dataset", "test.jpg")

# Load image
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found. Check path.")
else:
    print("Image loaded successfully.")

    # Display image
    cv2.imshow("Test Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
