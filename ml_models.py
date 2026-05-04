from sentence_transformers import SentenceTransformer
import spacy
import sys

# Load Sentence Transformer model
print("Loading SentenceTransformer model...", file=sys.stderr)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load spaCy model
try:
    print("Loading spaCy model...", file=sys.stderr)
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: en_core_web_sm not found. Downloading...", file=sys.stderr)
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def get_embedding(text: str):
    return embedding_model.encode(text)

def extract_entities(text: str):
    doc = nlp(text)
    return doc.ents
