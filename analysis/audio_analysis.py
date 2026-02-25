import librosa
import numpy as np
import hashlib

def get_hashes(path):
    with open(path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest()

def analyze_audio(path):
    md5, sha256 = get_hashes(path)
    
    # Load audio file
    y, sr = librosa.load(path)
    
    # Feature Extraction: Spectral Centroid (Center of mass of the sound)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    
    # Logic: AI voices often have lower variance in spectral complexity 
    # than natural human speech in noisy environments.
    variance = np.var(cent)
    
    # If variance is extremely low, it might be synthetic/clean-room generated
    # If variance is extremely high, it might be a low-quality 'replay' attack
    conf_score = 70 if variance < 500 else 20 

    return {
        "md5": md5,
        "sha256": sha256,
        "spectral_variance": round(float(variance), 2),
        "confidence_score": conf_score,
        "methodology": "Spectral Centroid Variance Analysis",
        "observations": "Low variance suggests synthetic voice generation." if conf_score > 50 else "Natural frequency patterns detected."
    }