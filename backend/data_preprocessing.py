import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import pickle


class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.vectorizer = TfidfVectorizer(max_features=2000, stop_words="english")

    def load_data(self):
        # Load and clean data
        self.data = pd.read_csv(self.file_path)
        print(f"Data loaded successfully from {self.file_path}")

    def preprocess(self):
        # Combine labels into a binary column
        self.data["y"] = self._combine_labels()
        self.data = self._retain_columns()
        self.data = self._remove_missing()

        # Vectorize the text data
        X = self.vectorizer.fit_transform(self.data["text"])
        y = self.data["y"].values

        # Save the fitted vectorizer
        with open("../backend/tfidf_vectorizer.pkl", "wb") as f:
            pickle.dump(self.vectorizer, f)
        print("TfidfVectorizer saved as 'tfidf_vectorizer.pkl'")

        return X, y

    def _combine_labels(self):
        # Combine toxicity labels into a binary column
        return (
            self.data[
                [
                    "toxic",
                    "severe_toxic",
                    "obscene",
                    "threat",
                    "insult",
                    "identity_hate",
                ]
            ].sum(axis=1)
            > 0
        ).astype(int)

    def _retain_columns(self):
        # Retain only relevant columns
        return self.data[["comment_text", "y"]].rename(columns={"comment_text": "text"})

    def _remove_missing(self):
        # Drop rows with missing text
        return self.data.dropna(subset=["text"])


# Workflow function
def preprocess_and_split(input_file):
    processor = DataPreprocessor(input_file)
    processor.load_data()
    X, y = processor.preprocess()

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Compute class weights
    class_weights = compute_class_weight(
        class_weight="balanced", classes=np.unique(y), y=y
    )
    class_weight_dict = dict(enumerate(class_weights))

    return X_train, X_test, y_train, y_test, class_weight_dict


# Main Execution
if __name__ == "__main__":
    input_file = "../data/toxic-comment-ori-file.csv"
    X_train, X_test, y_train, y_test, class_weight = preprocess_and_split(input_file)

    print("Preprocessing complete.")
    print("Class weights:", class_weight)
