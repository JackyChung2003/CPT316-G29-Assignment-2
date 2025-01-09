from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import load_model
import pickle
import numpy as np

# Load trained model and TfidfVectorizer
model = load_model("../backend/toxic_comment_cnn.h5")

# Load the vectorizer
with open("../backend/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Test with sample inputs
sample_texts = [
    "The food in Malaysia is absolutely delicious!",
    "Why are you always so annoying?",
    "Kuala Lumpur is such a beautiful city to visit.",
    "You are the most useless person I've ever met.",
    "The beaches in Langkawi are breathtaking.",
    "I can't believe how rude you are to everyone.",
    "This laksa is the best thing I've ever eaten.",
    "You are so dumb, it's painful to watch.",
    "Malaysia's diverse culture is truly amazing.",
    "You're such an embarrassment to your family.",
    "Teh tarik makes every day better.",
    "I can't stand your attitude anymore.",
    "The festival decorations are so beautiful this year!",
    "Why do you have to ruin everything you touch?",
    "Penang has the best street food in the world.",
    "You are such a failure, stop pretending otherwise.",
    "Sarawak is home to some incredible natural wonders.",
    "Nobody likes you because you are so arrogant.",
    "The people here are so warm and welcoming.",
    "Your ideas are so stupid, just stop talking.",
    "This roti canai is perfectly flaky and delicious.",
    "You are such a waste of space.",
    "I love how peaceful and serene the islands are.",
    "You never do anything right, do you?",
    "Batu Caves is such an iconic place to visit.",
    "You are nothing but a burden to everyone around you.",
    "The wildlife in Borneo is so unique and fascinating.",
    "Your constant complaining is unbearable.",
    "The cultural dances are mesmerizing to watch.",
    "I wish you would just disappear.",
    "The sunsets here are some of the most beautiful I've ever seen.",
    "You're an absolute disgrace.",
    "The street art in Penang is so creative and inspiring.",
    "You are the worst thing that ever happened to me.",
    "Malaysians are known for their hospitality and kindness.",
    "You're completely useless, just like always.",
    "The festivals here are full of life and color.",
    "I hate everything about you.",
    "The traditional batik patterns are so intricate and beautiful.",
    "You never contribute anything meaningful to the team.",
    "The aroma of nasi lemak always makes my mouth water.",
    "Why are you such a terrible person?",
    "The rainforests in Sarawak are lush and full of life.",
    "You have no talent whatsoever.",
    "I feel so at peace watching the waves on the beach.",
    "You are the most selfish person I've ever met.",
    "Every bite of this rendang is packed with flavor.",
    "Why can't you ever do something useful for once?",
    "The mosque architecture is so stunning and peaceful.",
    "You always ruin everyone's mood.",
]


# Vectorize and predict
X_sample = vectorizer.transform(sample_texts)
X_sample_dense = np.expand_dims(X_sample.toarray(), axis=2)
predictions = model.predict(X_sample_dense).flatten()

# Print predictions
for text, pred in zip(sample_texts, predictions):
    print(f"Text: {text} | Toxic: {pred > 0.5} | Score: {pred:.2f}")
