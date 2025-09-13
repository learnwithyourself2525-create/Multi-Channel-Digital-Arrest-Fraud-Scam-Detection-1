import unittest
import os
from pipeline.detection_pipeline import DetectionPipeline

class TestDetectionPipeline(unittest.TestCase):
    """
    Placeholder for unit tests for the DetectionPipeline.
    
    A robust test suite would mock the individual model classes to test the
    pipeline's orchestration and risk aggregation logic in isolation. It would
    also include integration tests with the actual models on known data samples.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up the pipeline instance once for all tests."""
        # This can be slow, so it's done once per test class.
        # In a real test suite, you might use a lighter, mock version.
        cls.pipeline = DetectionPipeline()

    def test_sms_scam_detection(self):
        """Test that a known scam SMS is flagged with high risk."""
        scam_sms = {
            "text": "WINNER!! As a valued network customer you have been selected to receivea £900 prize reward! To claim call 09061701461."
        }
        result = self.pipeline.run(scam_sms, 'sms')
        self.assertIn(result['risk_level'], ['HIGH', 'CRITICAL'])
        self.assertGreater(result['risk_score'], 50)
        
        # Check for specific findings
        findings_text = " ".join([f['finding'] for f in result['findings']])
        self.assertIn("high-risk keywords", findings_text.lower())

    def test_email_phishing_detection(self):
        """Test that a known phishing email is flagged correctly."""
        phishing_email = {
            "sender_email": "support@paypal-security.net",
            "subject": "Security Alert: Unusual Sign-In Activity",
            "body": "Dear Customer, We detected an unusual sign-in. Click here: http://bit.ly/fake-login to confirm your details."
        }
        result = self.pipeline.run(phishing_email, 'email')
        self.assertEqual(result['risk_level'], 'CRITICAL')
        
    def test_legitimate_email(self):
        """Test that a legitimate email has a low risk score."""
        legit_email = {
            "sender_email": "billing@your-service-provider.com",
            "subject": "Your Monthly Invoice is Ready",
            "body": "Hello, Your invoice for May 2024 is available. No action is required."
        }
        result = self.pipeline.run(legit_email, 'email')
        self.assertEqual(result['risk_level'], 'LOW')
        self.assertEqual(result['risk_score'], 0)

if __name__ == '__main__':
    unittest.main()