import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_logging(log_level="INFO"):
    """
    Set up logging configuration for RedCalibur.
    Serverless-friendly version that only uses console logging.
    
    Args:
        log_level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # For serverless environments, only use console logging
    # File logging is not supported in serverless functions
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ],
        force=True  # Override any existing configuration
    )
    
    return logging.getLogger("RedCalibur")

class Config:
    """Configuration class for RedCalibur"""
    
    # API Keys (to be set via environment variables)
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
    
    # Rate limiting
    REQUEST_DELAY = 1  # seconds between requests
    MAX_RETRIES = 3
    
    # Output settings
    OUTPUT_DIR = "reports"
    REPORT_FORMAT = "both"  # pdf, json, or both
    
    # OSINT settings
    DEFAULT_PORTS = [
        20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 123, 135, 137, 138, 139, 143, 161, 162, 
        179, 389, 443, 445, 465, 514, 515, 587, 636, 993, 995, 1080, 1433, 1434, 1521, 1723, 
        2049, 3306, 3389, 5432, 5900, 5901, 6379, 8000, 8080, 8443, 8888, 9090, 27017
    ]
    SUBDOMAIN_WORDLIST = ["www", "mail", "ftp", "admin", "test", "dev", "staging", "api"]
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        issues = []
        
        if not cls.SHODAN_API_KEY:
            issues.append("SHODAN_API_KEY not set")
        
        if not cls.GEMINI_API_KEY:
            issues.append("GEMINI_API_KEY not set")
        
        if not cls.VIRUSTOTAL_API_KEY:
            issues.append("VIRUSTOTAL_API_KEY not set")

        # Skip directory creation in serverless environments
        # as we don't have write access to the filesystem
        try:
            if not os.path.exists(cls.OUTPUT_DIR):
                os.makedirs(cls.OUTPUT_DIR)
        except (OSError, PermissionError):
            # Ignore filesystem errors in serverless environments
            pass
            
        return issues
