from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pdf2docx import Converter

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("pdfToword.html")


@app.route("/convert", methods=["POST"])
def convert():
    try:
        if "file" not in request.files:
            raise Exception("No file part")
        file = request.files["file"]
        if file.filename == "":
            raise Exception("No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            docx_path = os.path.join(
                app.config["UPLOAD_FOLDER"], filename.rsplit(".", 1)[0] + ".docx"
            )

            # Convert PDF to Word
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            return redirect(
                url_for("success", filename=filename, output_path=docx_path)
            )
        else:
            raise Exception("Invalid file format")
    except Exception as e:
        return redirect(url_for("error", error_message=str(e), filename=file.filename))


@app.route("/success")
def success():
    filename = request.args.get("filename")
    output_path = request.args.get("output_path")
    return render_template("success.html", filename=filename, output_path=output_path)


@app.route("/error")
def error():
    filename = request.args.get("filename")
    output_path = request.args.get("output_path")
    error_message = request.args.get("error_message", "An error occurred")
    return render_template(
        "error.html",
        error_message=error_message,
        filename=filename,
        output_path=output_path,
    )


if __name__ == "__main__":
    app.run(debug=False, host= '192.168.29.167')
