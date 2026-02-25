from flask import Flask, render_template, request, send_file
import os
import traceback # Added for debugging

# Ensure the analysis folder is treated as a package
try:
    from analysis.image_analysis import analyze_image
    from analysis.audio_analysis import analyze_audio
    from analysis.video_analysis import analyze_video
    from analysis.report_generator import generate_report
except ImportError as e:
    print(f"IMPORT ERROR: {e}")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if 'media' not in request.files: return "No file uploaded"
            file = request.files["media"]
            if file.filename == '': return "No file selected"
            
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            ext = file.filename.split('.')[-1].lower()
            result = {"filename": file.filename}

            # Analysis Routing
            if ext in ["png", "jpg", "jpeg"]:
                result.update(analyze_image(filepath))
            elif ext in ["wav", "mp3"]:
                result.update(analyze_audio(filepath))
            elif ext in ["mp4", "avi", "mov"]:
                result.update(analyze_video(filepath))
            else:
                return "Unsupported file type."

            # Report Generation
            report_path = generate_report(filepath, result)
            
            if os.path.exists(report_path):
                return send_file(report_path, as_attachment=True)
            else:
                return "Analysis complete, but report file was not found."

        except Exception as e:
            # This will show you the EXACT error in the browser if it crashes
            error_details = traceback.format_exc()
            return f"<h1>Forensic Analysis Failed</h1><pre>{error_details}</pre>"
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) # Debug=True helps show errors