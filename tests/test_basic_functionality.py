import unittest
import sys
import os

# Add project root to path so `import redcalibur` works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from redcalibur.osint.domain_infrastructure.whois_lookup import perform_whois_lookup, is_valid_domain
from redcalibur.osint.domain_infrastructure.dns_enumeration import enumerate_dns_records

class TestDomainInfrastructure(unittest.TestCase):
    
    def test_valid_domain_check(self):
        """Test domain validation"""
        self.assertTrue(is_valid_domain("google.com"))
        self.assertFalse(is_valid_domain("invalid-domain-12345.com"))
    
    def test_whois_lookup(self):
        """Test WHOIS lookup functionality"""
        result = perform_whois_lookup("google.com")
        self.assertIsInstance(result, dict)
        # Should not have error for valid domain
        self.assertNotIn("error", result)
    
    def test_dns_enumeration(self):
        """Test DNS enumeration"""
        result = enumerate_dns_records("google.com")
        self.assertIsInstance(result, dict)
        self.assertIn("A", result)

class TestConfigValidation(unittest.TestCase):
    
    def test_config_validation(self):
        """Test configuration validation"""
        from redcalibur.config import Config
        issues = Config.validate_config()
        self.assertIsInstance(issues, list)

if __name__ == '__main__':
    unittest.main()
