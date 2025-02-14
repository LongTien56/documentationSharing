from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
DOCUMENTS_FILE = "documents.txt"

def load_documents():
    if not os.path.exists(DOCUMENTS_FILE):
        return []
    documents = []
    with open(DOCUMENTS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split('|', 1)
            if len(parts) == 2:  # Ensure both name and link exist
                documents.append(tuple(parts))
    return documents

def save_document(name, link):
    with open(DOCUMENTS_FILE, "a") as f:
        f.write(f"{name}|{link}\n")

@app.route('/')
def index():
    documents = load_documents()
    return render_template("index.html", documents=documents)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        name = request.form.get("doc_name")
        link = request.form.get("doc_link")
        if name and link:
            save_document(name, link)
        return redirect(url_for("index"))
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
