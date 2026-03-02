import json
import pickle
import numpy as np
import random
import os

class ChatbotModel:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.intents_data = None
        self.load_model()

    def load_model(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
            with open(os.path.join(base_dir, 'model.pkl'), 'rb') as f:
                self.model = pickle.load(f)
                
            with open(os.path.join(base_dir, 'vectorizer.pkl'), 'rb') as f:
                self.vectorizer = pickle.load(f)
                
            with open(os.path.join(base_dir, 'intents.json'), 'r', encoding='utf-8') as f:
                self.intents_data = json.load(f)
                
            print("Model and intents loaded successfully.")
        except Exception as e:
            print(f"Error loading model or intents: {e}")

    def predict_intent(self, text):
        if not self.model or not self.vectorizer or not text.strip():
            return "fallback", 0.0

        # Transform the input text
        X = self.vectorizer.transform([text])
        
        # Get prediction probabilities
        probs = self.model.predict_proba(X)[0]
        
        # Get the classes
        classes = self.model.classes_
        
        # Find the index of the highest probability
        max_idx = np.argmax(probs)
        confidence = probs[max_idx]
        intent = classes[max_idx]

        # Use 0.6 as the confidence threshold
        if confidence < 0.6:
            return "fallback", confidence

        return intent, confidence

    def get_response(self, intent_tag):
        if not self.intents_data:
            return "Sorry, I am currently unavailable."
            
        for intent in self.intents_data['intents']:
            if intent['tag'] == intent_tag:
                return random.choice(intent['responses'])
        
        # Default fallback text if intent not found
        return "I'm not sure about that. Would you like to contact support?"

# Singleton instance for easy import
chatbot_model = ChatbotModel()
