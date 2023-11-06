import logging

from flask import Flask, render_template, request, send_from_directory
import os

from werkzeug import run_simple

from lan_file import net

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "lan_folder"

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return f"File {filename} uploaded successfully."

    return render_template("upload.html")


@app.route("/files/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    port = 5555
    print(f"Running on http://{net.get_local_ip()}:{port}")
    run_simple("0.0.0.0", port, app)
