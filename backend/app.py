from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import pickle
import numpy as np


class ToxicCommentAPI:
    def __init__(self, model_path, vectorizer_path):
        self.model = self.load_model(model_path)
        self.vectorizer = self.load_vectorizer(vectorizer_path)

    @staticmethod
    def load_model(model_path):
        try:
            model = load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            exit(1)

    @staticmethod
    def load_vectorizer(vectorizer_path):
        try:
            with open(vectorizer_path, "rb") as file:
                vectorizer = pickle.load(file)
            print(f"Vectorizer loaded successfully from {vectorizer_path}")
            return vectorizer
        except FileNotFoundError:
            print(f"Error: Vectorizer file not found at {vectorizer_path}")
            exit(1)

    def classify_text(self, text):
        # Vectorize input text
        vectorized_text = self.vectorizer.transform([text])
        vectorized_text_dense = np.expand_dims(vectorized_text.toarray(), axis=2)

        # Make prediction
        prediction = self.model.predict(vectorized_text_dense).flatten()
        return bool(prediction[0]), float(prediction[0])  # Return both binary and score


def create_app(model_path, vectorizer_path):
    # Initialize API
    api = ToxicCommentAPI(model_path, vectorizer_path)
    app = Flask(__name__)

    @app.route("/classify", methods=["GET", "POST"])
    def classify():
        if request.method == "GET":
            return (
                jsonify({"message": "Please send a POST request with a 'text' field."}),
                200,
            )

        try:
            # Handle POST request
            data = request.get_json(force=True)
            text = data.get("text", "")
        except Exception as e:
            return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Classify the text
        is_toxic, score = api.classify_text(text)
        return jsonify({"toxic": is_toxic, "toxicity_score": score})

    return app


# Main Execution
if __name__ == "__main__":
    model_file = "toxic_comment_cnn.h5"  # Adjust path as necessary
    vectorizer_file = "tfidf_vectorizer.pkl"
    app = create_app(model_file, vectorizer_file)
    app.run(debug=True)
