from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
DOCUMENTS_FILE = "documents.txt"

def load_documents():
    if not os.path.exists(DOCUMENTS_FILE):
        return []
    with open(DOCUMENTS_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_document(link):
    with open(DOCUMENTS_FILE, "a") as f:
        f.write(link + "\n")

@app.route('/')
def index():
    documents = load_documents()
    return render_template("index.html", documents=documents)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        link = request.form.get("doc_link")
        if link:
            save_document(link)
        return redirect(url_for("index"))
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
