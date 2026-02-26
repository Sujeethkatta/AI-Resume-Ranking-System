import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "python machine learning deep learning data science",
    "java spring boot microservices backend developer",
    "react javascript frontend developer",
    "sql database mysql postgresql",
    "nlp artificial intelligence tensorflow pytorch"
]

vectorizer = TfidfVectorizer()
vectorizer.fit(documents)

joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Vectorizer trained and saved.")