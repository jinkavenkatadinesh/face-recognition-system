import streamlit as st
import cv2
import numpy as np
import os
import time
from mtcnn import MTCNN
from PIL import Image
import io

# ==========================================
# Page Configuration & Design Theme
# ==========================================
st.set_page_config(
    page_title="Intelligent Face Detection Hub",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Glassmorphism Styling
st.markdown("""
<style>
    /* Main body background & fonts */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Header customizations */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #00D2FF 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .sub-text {
        color: #94A3B8;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #16213E !important;
        border-right: 1px solid #1E293B;
    }
    
    /* Cards and metrics */
    .metric-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 210, 255, 0.5);
    }
    
    .metric-val {
        font-size: 2.25rem;
        font-weight: 700;
        color: #00D2FF;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    /* Upload zone styling */
    .stFileUploader section {
        background-color: #1E293B !important;
        border: 2px dashed #00D2FF !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00D2FF 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# Caching Model Loaders for Speed
# ==========================================
@st.cache_resource
def load_mtcnn():
    return MTCNN()

@st.cache_resource
def load_haar_cascade():
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(cascade_path)

mtcnn_detector = load_mtcnn()
haar_detector = load_haar_cascade()

# ==========================================
# Application Header
# ==========================================
st.markdown('<div class="gradient-text">👤 Intelligent Face Detection Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">A modern hybrid pipeline combining Deep Learning (MTCNN) & classical Computer Vision (Haar Cascade) with real-time image preprocessing.</div>', unsafe_allow_html=True)

# ==========================================
# Sidebar Configuration Panel
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #FFFFFF;'>⚙️ Settings Panel</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 1. Algorithm Selection
st.sidebar.subheader("🛡️ Detection Core")
algo_choice = st.sidebar.selectbox(
    "Select Model Engine:",
    ("Hybrid Pipeline (Best)", "MTCNN Deep Learning", "Haar Cascade Classical")
)

# 2. Preprocessing Options
st.sidebar.subheader("🎨 Preprocessing Pipeline")
enable_resize = st.sidebar.toggle("Auto-scale Large Images", value=True, help="Resizes images with width > max width setting to improve speed.")
max_width = st.sidebar.slider("Max Image Width (px)", 400, 1600, 800, 50, disabled=not enable_resize)

enable_denoise = st.sidebar.toggle("Apply Color Denoising", value=False, help="Reduces sensor noise and compression artifacts using Non-Local Means Denoising.")
denoise_strength = st.sidebar.slider("Denoise Strength", 5, 20, 10, 1, disabled=not enable_denoise)

enable_clahe = st.sidebar.toggle("CLAHE Light Normalization", value=True, help="Equalizes brightness and contrast in LAB color space. Ideal for shadows & low-light.")
clahe_clip = st.sidebar.slider("CLAHE Clip Limit", 1.0, 5.0, 2.0, 0.5, disabled=not enable_clahe)

# 3. Model Parameters
st.sidebar.subheader("📐 Model Tuning")
mtcnn_confidence = st.sidebar.slider("MTCNN Confidence Cutoff", 0.50, 0.99, 0.90, 0.05, disabled=(algo_choice == "Haar Cascade Classical"))

st.sidebar.markdown("**Haar Parameters:**")
haar_scale = st.sidebar.slider("Scale Factor", 1.01, 1.30, 1.05, 0.01, disabled=(algo_choice == "MTCNN Deep Learning"))
haar_neighbors = st.sidebar.slider("Min Neighbors", 1, 10, 3, 1, disabled=(algo_choice == "MTCNN Deep Learning"))


# ==========================================
# Image Processing Core Pipeline
# ==========================================
def preprocess_image(img):
    logs = []
    
    # Step 1: Resize
    h, w = img.shape[:2]
    if enable_resize and w > max_width:
        scale = max_width / w
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        logs.append(f"Resized from {w}x{h} to {img.shape[1]}x{img.shape[0]}")
    else:
        logs.append(f"Image processed at full scale: {w}x{h}")
        
    # Step 2: Denoise
    if enable_denoise:
        img = cv2.fastNlMeansDenoisingColored(img, None, denoise_strength, denoise_strength, 7, 21)
        logs.append("Applied fast Non-Local Means Denoising")
        
    # Step 3: Brightness / Contrast normalization via CLAHE in LAB space
    if enable_clahe:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        img = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        logs.append(f"Normalized illumination using CLAHE (clip={clahe_clip})")
        
    return img, logs


# ==========================================
# Application Workspace
# ==========================================
uploaded_file = st.file_uploader("📥 Drag and drop or browse an image to start face detection:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read uploaded bytes into OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    original_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if original_bgr is not None:
        # Preprocess
        with st.spinner("Executing preprocessing steps..."):
            preprocessed_bgr, pre_logs = preprocess_image(original_bgr.copy())
            
        # Initialize detection states
        annotated_image = preprocessed_bgr.copy()
        faces_detected = []
        engine_used = ""
        
        # Start timer for algorithm execution
        start_time = time.time()
        
        # Determine and run algorithms
        if algo_choice == "MTCNN Deep Learning":
            rgb_img = cv2.cvtColor(preprocessed_bgr, cv2.COLOR_BGR2RGB)
            results = mtcnn_detector.detect_faces(rgb_img)
            faces_detected = [r for r in results if r['confidence'] >= mtcnn_confidence]
            engine_used = "MTCNN Deep Learning"
            
            # Draw MTCNN detections
            for result in faces_detected:
                x, y, w, h = result['box']
                x, y = max(0, x), max(0, y)
                conf = result['confidence']
                
                # Draw bounding box
                cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(annotated_image, f"{conf:.2f}", (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                
                # Draw facial landmarks (eyes, nose, mouth corners)
                for keypoint, pt in result['keypoints'].items():
                    cv2.circle(annotated_image, pt, 3, (255, 0, 0), -1)
                    
        elif algo_choice == "Haar Cascade Classical":
            gray = cv2.cvtColor(preprocessed_bgr, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces_haar = haar_detector.detectMultiScale(
                gray,
                scaleFactor=haar_scale,
                minNeighbors=haar_neighbors,
                minSize=(20, 20)
            )
            for (x, y, w, h) in faces_haar:
                faces_detected.append({'box': [x, y, w, h], 'confidence': 1.0})
                cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (255, 165, 0), 2)
            engine_used = "Haar Cascade"
            
        else: # Hybrid Mode
            # Attempt MTCNN first
            rgb_img = cv2.cvtColor(preprocessed_bgr, cv2.COLOR_BGR2RGB)
            results = mtcnn_detector.detect_faces(rgb_img)
            faces_detected = [r for r in results if r['confidence'] >= mtcnn_confidence]
            engine_used = "MTCNN Deep Learning"
            
            # Draw MTCNN details
            if len(faces_detected) > 0:
                for result in faces_detected:
                    x, y, w, h = result['box']
                    x, y = max(0, x), max(0, y)
                    conf = result['confidence']
                    cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(annotated_image, f"{conf:.2f}", (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                    for keypoint, pt in result['keypoints'].items():
                        cv2.circle(annotated_image, pt, 3, (255, 0, 0), -1)
            else:
                # Fallback to Haar Cascade
                st.warning("⚠️ MTCNN found no faces. Activating Haar Cascade Fallback...")
                gray = cv2.cvtColor(preprocessed_bgr, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                faces_haar = haar_detector.detectMultiScale(
                    gray,
                    scaleFactor=haar_scale,
                    minNeighbors=haar_neighbors,
                    minSize=(20, 20)
                )
                for (x, y, w, h) in faces_haar:
                    faces_detected.append({'box': [x, y, w, h], 'confidence': 1.0})
                    cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (255, 165, 0), 2)
                engine_used = "Haar Fallback"
                
        execution_time = (time.time() - start_time) * 1000 # convert to ms
        
        # Display Premium Metrics Dashboard
        st.markdown("<h3 style='margin-bottom:1rem;'>📊 Real-Time Metrics</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val">{len(faces_detected)}</div>
                <div class="metric-label">Faces Detected</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val">{execution_time:.1f}ms</div>
                <div class="metric-label">Execution Time</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="font-size:1.5rem; line-height:2.25rem; color:#7C3AED;">{engine_used}</div>
                <div class="metric-label">Core Engine</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="font-size:1.5rem; line-height:2.25rem; color:#10B981;">{annotated_image.shape[1]}x{annotated_image.shape[0]}</div>
                <div class="metric-label">Working Dimensions</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display side-by-side images
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("🖼️ Original Uploaded Image")
            original_rgb = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)
            st.image(original_rgb, use_container_width=True)
            
        with col_right:
            st.subheader("🎯 Pipeline Processed Detections")
            annotated_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            st.image(annotated_rgb, use_container_width=True)
            
        # Download capabilities
        st.markdown("---")
        col_down, col_log = st.columns([1, 1])
        
        with col_down:
            st.markdown("### 💾 Export Results")
            annotated_pil = Image.fromarray(annotated_rgb)
            img_buffer = io.BytesIO()
            annotated_pil.save(img_buffer, format="JPEG", quality=95)
            img_bytes = img_buffer.getvalue()
            
            st.download_button(
                label="📥 Download Annotated Image",
                data=img_bytes,
                file_name=f"detected_{uploaded_file.name}",
                mime="image/jpeg"
            )
            
        with col_log:
            st.markdown("### ⚙️ Preprocessing Run-Logs")
            for log in pre_logs:
                st.write(f"✓ {log}")
                
        # Landmark details for MTCNN
        if len(faces_detected) > 0 and 'keypoints' in faces_detected[0]:
            st.markdown("### 📍 Detected Facial Landmarks (MTCNN)")
            for idx, face in enumerate(faces_detected):
                with st.expander(f"Face {idx + 1} Details (Confidence: {face['confidence']:.2%})"):
                    st.json(face['keypoints'])
                    
    else:
        st.error("Error: Could not decode uploaded image. Please check that the file format is valid.")

else:
    # Welcome Layout when no file is uploaded
    st.info("💡 Please upload an image file (.jpg, .jpeg, or .png) in the upload zone above to run the pipeline.")
    
    st.markdown("### 🛠️ How the Hybrid Pipeline Works")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        <div style="background-color: #1E293B; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #00D2FF;">
            <h4>Step 1: Raw Image Preprocessing</h4>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                The image is automatically downscaled for performance, denoised to remove camera grain, and passed through CLAHE (Contrast Limited Adaptive Histogram Equalization) to balance shadows and exposure.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("""
        <div style="background-color: #1E293B; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #7C3AED;">
            <h4>Step 2: Dual-Model Detection</h4>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                <b>MTCNN</b> deep learning engine scans for faces and maps 5 landmarks (eyes, nose, mouth corners). If MTCNN finds zero faces, the fast, classical <b>Haar Cascade</b> classifier serves as a fallback.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_c:
        st.markdown("""
        <div style="background-color: #1E293B; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #10B981;">
            <h4>Step 3: Rendering & Analytics</h4>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                Bounding boxes and landmarks are drawn onto the image. Detection speed, confidence rates, and face counts are tabulated and rendered alongside a download link.
            </p>
        </div>
        """, unsafe_allow_html=True)
