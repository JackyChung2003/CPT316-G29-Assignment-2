import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from sklearn.metrics import classification_report
from data_preprocessing import (
    preprocess_and_split,
)  # Import your preprocessing function


def build_cnn_model(input_shape):
    # Define the CNN model
    model = Sequential(
        [
            Conv1D(
                filters=128, kernel_size=5, activation="relu", input_shape=input_shape
            ),
            MaxPooling1D(pool_size=2),
            Flatten(),
            Dense(128, activation="relu"),
            Dropout(0.5),
            Dense(1, activation="sigmoid"),  # Binary classification
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def train_and_evaluate(X_train, X_test, y_train, y_test, class_weight):
    # Add a channel dimension for Conv1D
    X_train = np.expand_dims(X_train.toarray(), axis=2)  # Convert sparse to dense
    X_test = np.expand_dims(X_test.toarray(), axis=2)  # Convert sparse to dense

    # Build and train the model
    model = build_cnn_model((X_train.shape[1], 1))
    history = model.fit(
        X_train,
        y_train,
        epochs=20,
        batch_size=32,
        validation_data=(X_test, y_test),
        class_weight=class_weight,  # Apply class weights
    )

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    # Classification report
    y_pred_probs = model.predict(X_test).flatten()
    y_pred = (y_pred_probs > 0.5).astype(int)
    print(classification_report(y_test, y_pred))

    return model, history


if __name__ == "__main__":
    input_file = "../data/toxic-comment-ori-file.csv"

    # Preprocess and split the data
    X_train, X_test, y_train, y_test, class_weight = preprocess_and_split(input_file)

    # Train and evaluate the model
    model, history = train_and_evaluate(X_train, X_test, y_train, y_test, class_weight)

    # Save the model
    model.save("../backend/toxic_comment_cnn.h5")
    print("Model saved as 'toxic_comment_cnn.h5'")
