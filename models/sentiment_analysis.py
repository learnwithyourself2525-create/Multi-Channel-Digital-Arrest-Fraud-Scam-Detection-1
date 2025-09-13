from textblob import TextBlob
import re

class SentimentAnalyzer:
    """
    Analyzes text for sentiment and keywords associated with fraudulent activities.
    
    This module uses a dual approach:
    1. Polarity/Subjectivity Analysis: Uses TextBlob, a simple and effective library for
       general sentiment analysis.[6] A highly negative or unusually positive sentiment
       can be a red flag.
    2. Keyword Spotting: Scans for specific words and phrases commonly used in scams
       to create a sense of urgency, fear, or authority (e.g., "urgent", "verify", "suspended").
    """
    def __init__(self):
        """
        Initializes the sentiment analyzer with a predefined list of scam keywords.
        """
        # This list can be expanded based on common scam tactics.
        self.scam_keywords = [
            'urgent', 'immediate', 'action required', 'verify', 'account suspended',
            'security alert', 'winner', 'prize', 'claim', 'free', 'reward', 'refund',
            'confidential', 'ssn', 'password', 'bank account', 'credit card', 'irs',
            'tax refund', 'w-2', 'invoice', 'overdue'
        ]
        # Regex pattern to find any of the keywords, case-insensitive.
        self.keyword_pattern = re.compile(r'\b(' + '|'.join(self.scam_keywords) + r')\b', re.IGNORECASE)
        print("Sentiment analyzer initialized.")

    def analyze(self, text):
        """
        Performs sentiment analysis and keyword spotting on the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            dict: A dictionary containing sentiment scores (polarity, subjectivity)
                  and a list of any flagged keywords found.
        """
        if not text:
            return {"polarity": 0.0, "subjectivity": 0.0, "flagged_keywords":}

        try:
            # Perform sentiment analysis using TextBlob.
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            # Spot keywords using the pre-compiled regex pattern.
            found_keywords = self.keyword_pattern.findall(text.lower())
            
            return {
                "polarity": sentiment.polarity,
                "subjectivity": sentiment.subjectivity,
                "flagged_keywords": list(set(found_keywords)) # Return unique keywords
            }
        except Exception as e:
            print(f"Error during sentiment analysis: {e}")
            return {"polarity": 0.0, "subjectivity": 0.0, "flagged_keywords":, "error": str(e)}

# Example usage:
if __name__ == '__main__':
    analyzer = SentimentAnalyzer()
    
    scam_text = "URGENT action required! Your bank account has been suspended. Please verify your details to avoid closure."
    legit_text = "Here is the invoice for your recent purchase. Let us know if you have any questions."
    
    scam_analysis = analyzer.analyze(scam_text)
    legit_analysis = analyzer.analyze(legit_text)
    
    print(f"Scam Text Analysis: {scam_analysis}")
    print(f"Legit Text Analysis: {legit_analysis}")