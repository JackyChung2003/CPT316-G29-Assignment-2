from app import create_app

# Pass the necessary parameters for the create_app function
application = create_app("toxic_comment_cnn.h5", "tfidf_vectorizer.pkl")
