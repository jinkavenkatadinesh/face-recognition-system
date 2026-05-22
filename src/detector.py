"""
Hybrid Face Detector (MTCNN + Haar Cascade Fallback)
Part of the Face Detection & Recognition Pipeline.
"""

import cv2
import numpy as np

class HybridFaceDetector:
    """
    A unified hybrid face detector that supports deep learning-based MTCNN
    and classical Haar Cascade face detection with intelligent fallback logic.
    """
    def __init__(self, mtcnn_instance=None, haar_instance=None):
        """
        Initializes the detector. Instances of underlying detectors can be passed in,
        allowing for frameworks like Streamlit to pass cached resource loaders.
        """
        self._mtcnn = mtcnn_instance
        self._haar = haar_instance

    @property
    def mtcnn(self):
        if self._mtcnn is None:
            from mtcnn import MTCNN
            self._mtcnn = MTCNN()
        return self._mtcnn

    @property
    def haar(self):
        if self._haar is None:
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            self._haar = cv2.CascadeClassifier(cascade_path)
        return self._haar

    def detect_mtcnn(self, img_bgr, confidence_cutoff=0.90):
        """
        Detects faces using the MTCNN deep learning model.
        Returns a list of matching face detections.
        """
        rgb_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        raw_results = self.mtcnn.detect_faces(rgb_img)
        # Filter detections by confidence cutoff
        filtered_results = [r for r in raw_results if r['confidence'] >= confidence_cutoff]
        return filtered_results

    def detect_haar(self, img_bgr, scale_factor=1.05, min_neighbors=3):
        """
        Detects faces using classical Haar Cascade.
        Converts BGR to Grayscale and runs equalized histogram detection.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces_haar = self.haar.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=(20, 20)
        )
        
        # Format output to match MTCNN box structure: {'box': [x, y, w, h], 'confidence': 1.0}
        formatted_results = []
        for (x, y, w, h) in faces_haar:
            formatted_results.append({
                'box': [int(x), int(y), int(w), int(h)],
                'confidence': 1.0
            })
        return formatted_results

    def detect(self, img_bgr, mode="hybrid", mtcnn_confidence=0.90, haar_scale=1.05, haar_neighbors=3):
        """
        Main interface to perform face detection.
        
        Args:
            img_bgr (numpy.ndarray): Input BGR image.
            mode (str): One of "hybrid", "mtcnn", or "haar".
            mtcnn_confidence (float): Cutoff score for MTCNN detections.
            haar_scale (float): Scale factor for Haar Cascades.
            haar_neighbors (int): Min neighbors parameter for Haar Cascades.
            
        Returns:
            faces (list): List of dicts representing detected faces.
            annotated_img (numpy.ndarray): The BGR image with drawn bounding boxes/landmarks.
            engine_used (str): Descriptive name of the detection path taken.
        """
        annotated_img = img_bgr.copy()
        faces = []
        engine_used = ""

        # Normalize mode string
        mode_lower = mode.lower()

        if "mtcnn" in mode_lower:
            faces = self.detect_mtcnn(img_bgr, mtcnn_confidence)
            engine_used = "MTCNN Deep Learning"
            self.draw_mtcnn_annotations(annotated_img, faces)

        elif "haar" in mode_lower or "cascade" in mode_lower:
            faces = self.detect_haar(img_bgr, haar_scale, haar_neighbors)
            engine_used = "Haar Cascade"
            self.draw_haar_annotations(annotated_img, faces)

        else:  # Hybrid Mode
            # Attempt MTCNN
            faces = self.detect_mtcnn(img_bgr, mtcnn_confidence)
            if len(faces) > 0:
                engine_used = "MTCNN Deep Learning"
                self.draw_mtcnn_annotations(annotated_img, faces)
            else:
                # Fallback to Haar Cascade
                faces = self.detect_haar(img_bgr, haar_scale, haar_neighbors)
                engine_used = "Haar Fallback"
                self.draw_haar_annotations(annotated_img, faces)

        return faces, annotated_img, engine_used

    @staticmethod
    def draw_mtcnn_annotations(img, faces):
        """Draws green bounding boxes and blue landmarks for MTCNN detections."""
        for result in faces:
            x, y, w, h = result['box']
            # Safeguard negative coordinates
            x, y = max(0, x), max(0, y)
            conf = result['confidence']
            
            # Green bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, f"{conf:.2f}", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            # 5-point facial landmarks (eyes, nose, mouth corners)
            if 'keypoints' in result:
                for keypoint, pt in result['keypoints'].items():
                    cv2.circle(img, pt, 3, (255, 0, 0), -1)

    @staticmethod
    def draw_haar_annotations(img, faces):
        """Draws orange bounding boxes for Haar Cascade detections."""
        for result in faces:
            x, y, w, h = result['box']
            x, y = max(0, x), max(0, y)
            # Orange bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 165, 0), 2)
