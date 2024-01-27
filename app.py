from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from clean_analysis import init_dvc, remove_images_and_dvc_commit
from analyze_images import analyze_images
import os


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if "image-file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    files = request.files.getlist("image-file")

    for file in files:
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return jsonify({"message": "Files successfully uploaded"}), 200


@app.route('/api/analyze', methods=['GET'])
def analyze_images_endpoint():
    init_dvc()
    issues_data_frame = analyze_images(app.config["UPLOAD_FOLDER"])
    if not issues_data_frame.empty:
        removed_files = remove_images_and_dvc_commit(issues_data_frame)
        return jsonify({"message": f"Removed {len(removed_files)} files"})
    else:
        return jsonify({"message": "No issues found. No files removed."})


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
