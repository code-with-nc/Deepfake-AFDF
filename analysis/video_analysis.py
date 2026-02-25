import cv2
import hashlib
import numpy as np

def get_hashes(path):
    with open(path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest()

def analyze_video(path):
    md5, sha256 = get_hashes(path)
    cap = cv2.VideoCapture(path)
    
    diffs = []
    ret, prev_frame = cap.read()
    
    if not ret:
        return {"error": "Corrupt Video File"}

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    frame_count = 0
    while frame_count < 300: # Analyze first 300 frames for speed
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference between frames
        frame_diff = cv2.absdiff(prev_gray, gray)
        diff_mean = np.mean(frame_diff)
        diffs.append(diff_mean)
        
        prev_gray = gray
        frame_count += 1
    
    cap.release()
    
    # Analyze the 'jitter' (standard deviation of the differences)
    # High jitter between frames is a common indicator of a poor deepfake mask
    jitter = np.std(diffs)
    conf_score = 80 if jitter > 1.5 else 10

    return {
        "md5": md5,
        "sha256": sha256,
        "temporal_jitter_score": round(float(jitter), 4),
        "confidence_score": conf_score,
        "methodology": "Temporal Frame-Diff Consistency Check",
        "observations": "High temporal inconsistency detected at frame boundaries." if conf_score > 50 else "Stable frame transitions."
    }