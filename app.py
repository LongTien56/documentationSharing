from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
DOCUMENTS_FILE = "documents/documents.txt"

def load_documents():
    if not os.path.exists(DOCUMENTS_FILE):
        return []
    documents = []
    with open(DOCUMENTS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split('|', 1)
            if len(parts) == 2:  # Ensure both name and link exist
                documents.append(tuple(parts))
    return list(enumerate(documents))  # Return index for editing/deleting

def save_documents(documents):
    """Overwrite the documents file with the updated content."""
    with open(DOCUMENTS_FILE, "w") as f:
        for name, link in documents:
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
            with open(DOCUMENTS_FILE, "a") as f:
                f.write(f"{name}|{link}\n")
        return redirect(url_for("index"))
    return render_template("upload.html")

@app.route('/edit/<int:doc_id>', methods=["GET", "POST"])
def edit(doc_id):
    documents = load_documents()
    if doc_id < 0 or doc_id >= len(documents):
        return "Document not found", 404

    if request.method == "POST":
        new_name = request.form.get("new_name")
        doc_link = request.form.get("doc_link")
        if new_name and doc_link:
            documents[doc_id] = (new_name, doc_link)  # Update name
            save_documents([doc for _, doc in documents])  # Save updates
        return redirect(url_for("index"))

    return render_template("edit.html", document=documents[doc_id][1])

@app.route('/confirm_delete/<int:doc_id>', methods=["GET", "POST"])
def confirm_delete(doc_id):
    documents = load_documents()
    if doc_id < 0 or doc_id >= len(documents):
        return "Document not found", 404

    if request.method == "POST":
        documents.pop(doc_id)  # Remove the document
        save_documents([doc for _, doc in documents])  # Save updates
        return redirect(url_for("index"))

    return render_template("confirm_delete.html", document=documents[doc_id][1])

if __name__ == "__main__":
   app.run(host='0.0.0.0',debug=True)
