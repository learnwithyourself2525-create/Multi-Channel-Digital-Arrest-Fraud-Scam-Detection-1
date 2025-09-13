# models/text_classifier.py

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os

class TextClassifier:
    def __init__(self, model_path="./models/saved_models/scam_text_classifier"):
        """
        Initializes the text classifier.
        
        Args:
            model_path (str): Path to the saved fine-tuned model.
        """
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            print(f"Warning: Model not found at {self.model_path}. Using default model.")
            # Fallback to a pre-trained model if no fine-tuned one is found
            self.model_name = "distilbert-base-uncased"
            self.classifier = None
        else:
            self.model_name = self.model_path
            self.classifier = pipeline("text-classification", model=self.model_path)

    def predict(self, text: str) -> dict:
        """
        Analyzes a text string and predicts if it's a scam.

        Args:
            text (str): The input text (SMS, email, etc.).

        Returns:
            dict: A dictionary containing the prediction and explanation.
        """
        if self.classifier is None:
            # Lazy load the pipeline if it wasn't loaded in __init__
            self.classifier = pipeline("text-classification", model=self.model_name)
            
        prediction = self.classifier(text)
        is_scam = True if prediction['label'].lower() == 'spam' else False
        
        # Simple Explainability: Identify trigger phrases
        trigger_phrases = [
            "digital arrest", "verify your identity", "account suspended",
            "legal action", "immediate payment", "urgent", "click this link"
        ]
        found_triggers = [phrase for phrase in trigger_phrases if phrase in text.lower()]

        return {
            "is_scam": is_scam,
            "confidence": round(prediction['score'], 2),
            "explanation": {
                "model_label": prediction['label'],
                "trigger_phrases": found_triggers
            }
        }

# Note: The training script from the initial report can be adapted and placed here
# as a separate function, e.g., `def train_and_save_model():...`
# This keeps the inference class clean and focused.