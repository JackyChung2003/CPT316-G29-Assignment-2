from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import load_model
import pickle

# Load trained model and TfidfVectorizer
model = load_model("../backend/toxic_comment_cnn.h5")

# Simulate loading your vectorizer
with open("../backend/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Test with sample inputs
sample_texts = [
    "You are amazing!",
    "I hate you and everything about you.",
    "What a wonderful day to spread joy!",
    "You're so stupid and worthless.",
]

# Vectorize and predict
X_sample = vectorizer.transform(sample_texts)
X_sample_dense = np.expand_dims(X_sample.toarray(), axis=2)
predictions = model.predict(X_sample_dense).flatten()

# Print predictions
for text, pred in zip(sample_texts, predictions):
    print(f"Text: {text} | Toxic: {pred > 0.5}")
