import cv2
import numpy as np
import hashlib
from PIL import Image, ImageChops
import exifread

def get_hashes(path):
    with open(path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest()

def perform_ela(path, quality=90):
    """Detects re-compression/splicing artifacts."""
    original = Image.open(path).convert('RGB')
    tmp_path = path + "_tmp.jpg"
    original.save(tmp_path, 'JPEG', quality=quality)
    
    tmp_img = Image.open(tmp_path)
    ela_im = ImageChops.difference(original, tmp_img)
    
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    
    # FIX: Ensure scale is an integer by using // or int()
    scale = int(255.0 / max_diff) if max_diff != 0 else 1
    
    # Now this won't throw a TypeError
    ela_im = ImageChops.constant(ela_im, scale) 
    
    ela_path = path + "_ela.png"
    ela_im.save(ela_path)
    return ela_path

def analyze_image(path):
    md5, sha256 = get_hashes(path)
    ela_path = perform_ela(path)
    
    # Metadata Check (Anti-Forensics)
    with open(path, 'rb') as f:
        tags = exifread.process_file(f)
    
    metadata_status = "Intact" if tags else "Stripped/Missing (Potential Anti-Forensics)"
    
    # Noise Analysis for Smoothing
    img = cv2.imread(path, 0)
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
    
    # Simple logic: low noise often means AI smoothing or GAN generation
    conf = 85 if laplacian_var < 100 else 15 

    return {
        "md5": md5, "sha256": sha256,
        "metadata_status": metadata_status,
        "ela_visual": ela_path,
        "confidence_score": conf,
        "methodology": "Error Level Analysis & Noise Variance"
    }