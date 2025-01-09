from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling cross-origin requests
from tensorflow.keras.models import load_model
import pickle
import numpy as np
import os
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ToxicCommentAPI:
    def __init__(self, model_path, vectorizer_path):
        self.model = self.load_model(model_path)
        self.vectorizer = self.load_vectorizer(vectorizer_path)

    @staticmethod
    def load_model(model_path):
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
            model = load_model(model_path)
            logging.info(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            exit(1)

    @staticmethod
    def load_vectorizer(vectorizer_path):
        try:
            if not os.path.exists(vectorizer_path):
                raise FileNotFoundError(
                    f"Vectorizer file not found at {vectorizer_path}"
                )
            with open(vectorizer_path, "rb") as file:
                vectorizer = pickle.load(file)
            logging.info(f"Vectorizer loaded successfully from {vectorizer_path}")
            return vectorizer
        except Exception as e:
            logging.error(f"Error loading vectorizer: {e}")
            exit(1)

    def classify_text(self, text):
        try:
            # Vectorize input text
            vectorized_text = self.vectorizer.transform([text])
            vectorized_text_dense = np.expand_dims(vectorized_text.toarray(), axis=2)

            # Make prediction
            prediction = self.model.predict(vectorized_text_dense).flatten()
            return bool(prediction[0]), float(
                prediction[0]
            )  # Return both binary and score
        except Exception as e:
            logging.error(f"Error during classification: {e}")
            return False, 0.0


def create_app(model_path, vectorizer_path):
    # Initialize API
    api = ToxicCommentAPI(model_path, vectorizer_path)
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    @app.route("/classify", methods=["GET", "POST"])
    def classify():
        if request.method == "GET":
            return jsonify({"message": "Send a POST request with a 'text' field."}), 200

        try:
            # Handle POST request
            data = request.get_json(force=True)
            text = data.get("text", "")
        except Exception as e:
            logging.error(f"Invalid JSON: {e}")
            return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

        if not text:
            logging.warning("No text provided in the request")
            return jsonify({"error": "No text provided"}), 400

        # Classify the text
        is_toxic, score = api.classify_text(text)
        logging.info(
            f"Classified: '{text[:30]}...' -> Toxic: {is_toxic}, Score: {score}"
        )
        return jsonify({"toxic": is_toxic, "toxicity_score": score})

    return app


if __name__ == "__main__":
    # Parse command-line arguments for model and vectorizer paths
    parser = argparse.ArgumentParser(description="Toxic Comment API")
    parser.add_argument(
        "--model",
        type=str,
        default="toxic_comment_cnn.h5",
        help="Path to the Keras model file",
    )
    parser.add_argument(
        "--vectorizer",
        type=str,
        default="tfidf_vectorizer.pkl",
        help="Path to the vectorizer pickle file",
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to run the server on"
    )
    args = parser.parse_args()

    # Create Flask app
    app = create_app(args.model, args.vectorizer)

    # Run the app
    app.run(host="0.0.0.0", port=args.port)
