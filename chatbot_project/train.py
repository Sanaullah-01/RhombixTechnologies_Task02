import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import os

def train():
    print("Loading intents.json...")
    with open('intents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    patterns = []
    tags = []
    for intent in data['intents']:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            tags.append(intent['tag'])

    print(f"Extracted {len(patterns)} patterns for {len(set(tags))} intents.")

    print("Training TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(lowercase=True)
    X = vectorizer.fit_transform(patterns)
    y = np.array(tags)

    print("Training Logistic Regression Model...")
    clf = LogisticRegression(random_state=42, max_iter=1000, C=10.0)
    clf.fit(X, y)

    print("Saving model and vectorizer...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)

    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    print("Training complete! model.pkl and vectorizer.pkl saved successfully.")

if __name__ == "__main__":
    train()
