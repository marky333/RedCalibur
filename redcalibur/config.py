import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_logging(log_level="INFO"):
    """
    Set up logging configuration for RedCalibur.
    
    Args:
        log_level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = f"{log_dir}/redcalibur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
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
    DEFAULT_PORTS = [22, 80, 443, 21, 23, 25, 53, 110, 993, 995]
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

        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
            
        return issues
