from flask import Flask, render_template, request
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from document_reader import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

document_lines = []
document_text = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    global document_text, document_lines
    results = []
    query = ''

    if request.method == 'POST':
        if 'document' in request.files:
            uploaded_file = request.files['document']
            if uploaded_file.filename != '':
                os.makedirs('uploads', exist_ok=True)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
                document_text = extract_text(file_path)
                document_lines = [line for line in document_text.split('\n') if line.strip()]

        query = request.form.get('query')
        if query and document_lines:
            vectorizer = TfidfVectorizer().fit(document_lines + [query])
            vectors = vectorizer.transform(document_lines + [query])
            cosine_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
            top_indices = cosine_scores.argsort()[-5:][::-1]
            results = [document_lines[i] for i in top_indices if cosine_scores[i] > 0.1]

    return render_template('index.html', text=document_text, results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)