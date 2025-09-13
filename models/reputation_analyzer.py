import phonenumbers
from email_validator import validate_email, EmailNotValidError

class ReputationAnalyzer:
    """
    Analyzes sender metadata (email, phone number) for reputation-based risk signals.

    This module provides a first line of defense by checking for common red flags:
    1. Email Analysis: Validates email syntax and checks for disposable domains,
       which are frequently used for scams.[14, 15]
    2. Phone Number Analysis: Validates phone number format and attempts to identify
       the carrier and number type (e.g., mobile vs. VoIP), as spoofed or temporary
       numbers are common in fraud.[16, 17]
    """
    def __init__(self):
        """
        Initializes the analyzer with a list of known disposable email providers.
        """
        self.disposable_domains = {
            'mailinator.com', 'temp-mail.org', '10minutemail.com', 'yopmail.com'
        }
        print("Reputation analyzer initialized.")

    def analyze_email(self, email_address):
        """
        Analyzes an email address for validity and reputation.

        Args:
            email_address (str): The email address to analyze.

        Returns:
            dict: A dictionary of findings, including validity, domain, and whether
                  it's from a disposable provider.
        """
        findings = {
            "is_valid_syntax": False,
            "is_disposable": False,
            "domain": None,
            "error": None
        }
        if not email_address:
            findings["error"] = "Email address is empty."
            return findings

        try:
            # Use email-validator to check syntax and deliverability (MX records)
            validation = validate_email(email_address, check_deliverability=False) # Set to False for speed in PoC
            findings["is_valid_syntax"] = True
            findings["domain"] = validation.domain
            
            if validation.domain in self.disposable_domains:
                findings["is_disposable"] = True
                
        except EmailNotValidError as e:
            findings["error"] = str(e)
            
        return findings

    def analyze_phone_number(self, phone_number_str, country_code="US"):
        """
        Analyzes a phone number for validity and type.

        Args:
            phone_number_str (str): The phone number as a string.
            country_code (str): The default country code to assume if not provided.

        Returns:
            dict: A dictionary of findings, including validity, type, and carrier.
        """
        findings = {
            "is_valid": False,
            "number_type": "UNKNOWN",
            "carrier": "UNKNOWN",
            "error": None
        }
        if not phone_number_str:
            findings["error"] = "Phone number is empty."
            return findings

        try:
            # The phonenumbers library can parse, format, and validate numbers.
            parsed_number = phonenumbers.parse(phone_number_str, country_code)
            
            if phonenumbers.is_valid_number(parsed_number):
                findings["is_valid"] = True
                
                # Get number type (MOBILE, FIXED_LINE, VOIP, etc.)
                num_type = phonenumbers.number_type(parsed_number)
                type_map = {
                    phonenumbers.PhoneNumberType.MOBILE: "MOBILE",
                    phonenumbers.PhoneNumberType.FIXED_LINE: "FIXED_LINE",
                    phonenumbers.PhoneNumberType.VOIP: "VOIP",
                    phonenumbers.PhoneNumberType.TOLL_FREE: "TOLL_FREE",
                }
                findings["number_type"] = type_map.get(num_type, "UNKNOWN")
                
            else:
                findings["error"] = "Invalid phone number format or non-existent number."

        except phonenumbers.phonenumberutil.NumberParseException as e:
            findings["error"] = str(e)
            
        return findings

# Example usage:
if __name__ == '__main__':
    analyzer = ReputationAnalyzer()
    
    # Email examples
    valid_email = "test@gmail.com"
    disposable_email = "scammer@mailinator.com"
    invalid_email = "not-an-email"
    
    print(f"Analysis for '{valid_email}': {analyzer.analyze_email(valid_email)}")
    print(f"Analysis for '{disposable_email}': {analyzer.analyze_email(disposable_email)}")
    print(f"Analysis for '{invalid_email}': {analyzer.analyze_email(invalid_email)}")
    
    # Phone number examples
    valid_phone = "202-456-1111"
    invalid_phone = "12345"
    
    print(f"\nAnalysis for '{valid_phone}': {analyzer.analyze_phone_number(valid_phone, 'US')}")
    print(f"Analysis for '{invalid_phone}': {analyzer.analyze_phone_number(invalid_phone, 'US')}")