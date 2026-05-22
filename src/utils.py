"""
Image Preprocessing Utilities
Part of the Face Detection & Recognition Pipeline.
"""

import cv2
import numpy as np

def resize_image(img, enable_resize=True, max_width=800):
    """
    Resizes image to a max width while maintaining aspect ratio.
    """
    h, w = img.shape[:2]
    if enable_resize and w > max_width:
        scale = max_width / w
        img_resized = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        log = f"Resized from {w}x{h} to {img_resized.shape[1]}x{img_resized.shape[0]}"
        return img_resized, log
    else:
        log = f"Image processed at full scale: {w}x{h}"
        return img, log

def denoise_image(img, enable_denoise=True, strength=10):
    """
    Applies Non-Local Means Denoising to filter sensor noise.
    """
    if enable_denoise:
        img_denoised = cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)
        log = "Applied fast Non-Local Means Denoising"
        return img_denoised, log
    return img, None

def apply_clahe(img, enable_clahe=True, clip_limit=2.0, tile_grid=(8, 8)):
    """
    Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) on the L channel of LAB space
    to normalize illumination and contrast.
    """
    if enable_clahe:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        img_enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        log = f"Normalized illumination using CLAHE (clip={clip_limit})"
        return img_enhanced, log
    return img, None

def preprocess_pipeline(img, enable_resize=True, max_width=800, 
                        enable_denoise=False, denoise_strength=10, 
                        enable_clahe=True, clahe_clip=2.0):
    """
    Runs the entire sequence of image preprocessing: resizing, denoising, and CLAHE.
    Returns:
        preprocessed_image (numpy.ndarray): Preprocessed image.
        logs (list of str): Detailed steps performed.
    """
    logs = []
    
    # 1. Resize
    img, resize_log = resize_image(img, enable_resize, max_width)
    logs.append(resize_log)
    
    # 2. Denoise
    img, denoise_log = denoise_image(img, enable_denoise, denoise_strength)
    if denoise_log:
        logs.append(denoise_log)
        
    # 3. Illumination Normalization
    img, clahe_log = apply_clahe(img, enable_clahe, clahe_clip)
    if clahe_log:
        logs.append(clahe_log)
        
    return img, logs
