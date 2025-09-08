# RedCalibur 🗡️

> "Forged at the intersection of artificial intelligence and offensive cybersecurity."

**RedCalibur** is a professional, AI-powered red teaming toolkit designed to automate and enhance various phases of penetration testing, with a primary focus on comprehensive OSINT (Open Source Intelligence) reconnaissance. It leverages machine learning and large language models (LLMs) to supercharge ethical hacking workflows.

This project serves both as a practical cybersecurity tool and as a demonstration of applying neural networks and AI in cybersecurity for academic purposes.

---
## ⚔️ Features

RedCalibur integrates traditional red teaming techniques with modern AI, offering a wide array of capabilities.

### 🌐 Core OSINT Capabilities
* **Domain & Infrastructure Analysis**:
    * **WHOIS Lookup**: Comprehensive domain registration information.
    * **DNS Enumeration**: Discovery of A, AAAA, MX, TXT, CNAME, and NS records.
    * **Subdomain Discovery**: Automated enumeration using multiple techniques.
    * **SSL/TLS Analysis**: Certificate details and security configuration assessment.
    * **Port Scanning**: Intelligent scanning for open ports and services.
* **Threat Intelligence Integration**:
    * **Shodan**: Discover internet-facing devices, services, and vulnerabilities.
    * **VirusTotal**: Analyze domains and IPs for known malicious activity.
* **Search & Data Mining**:
    * **Google Dorking**: Automate advanced search queries to find sensitive information.
    * **Leak Detection**: Search Pastebin and GitHub for potential data leaks.

### 🧠 AI-Enhanced Features
* **AI-Powered Phishing Detection**:
    * **Custom Neural Networks**: A PyTorch-based classifier for URL and feature analysis.
    * **Ensemble Methods**: Combines a Random Forest and Neural Network for improved accuracy and robustness.
    * **Advanced Feature Engineering**: Extracts over 10 features from URLs, including Shannon entropy and domain structure, for precise analysis.
* **Intelligent Analysis & Reporting**:
    * **LLM Integration**: Leverages large language models (e.g., Gemini) for contextual understanding and summarization.
    * **Automated Risk Scoring**: AI-driven assessment to prioritize findings.
    * **Professional Report Generation**: Automatically create summary reports in PDF and JSON formats.
---

## 🏗️ Architecture

```
RedCalibur/
├── redcalibur/
│   ├── ai_core/              # Core AI components
│   │   └── __init__.py       # Neural nets, transformers, LLM
│   ├── phishing_detection/   # Phishing AI models
│   │   └── __init__.py       # URL analysis, feature extraction
│   ├── reconnaissance/       # AI-powered recon (future)
│   ├── prompt_injection/     # LLM security testing (future)
│   └── payload_generation/   # AI payload creation (future)
├── models/                   # Saved AI models
├── data/                     # Training datasets
├── demo.py                   # Main CLI interface
└── test.py                   # Component testing
```
---

## ⚡ Running the Project

```bash
# Quick demo
.venv/bin/python demo.py phishing --simple

# Test all components
.venv/bin/python test.py

# Custom URL analysis
.venv/bin/python demo.py phishing --url "your-url-here"
```

The toolkit is now ready for demonstration, testing, and further development for your AI and Neural Networks coursework!

---
## 📦 Installation

### Quick Install
```bash
git clone https://github.com/PraneeshRV/RedCalibur.git
cd RedCalibur
pip install -e .
```

### Production Install
```bash
pip install redcalibur
```

### Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv redcalibur-env
source redcalibur-env/bin/activate  # Linux/Mac
# redcalibur-env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required for full functionality
export SHODAN_API_KEY="your_shodan_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# Optional
export REDCALIBUR_OUTPUT_DIR="./reports"
export REDCALIBUR_LOG_LEVEL="INFO"
```

### Configuration Check
```bash
redcalibur config --check
redcalibur config --show
```

## 🎯 Usage

### Command Line Interface

#### Domain Reconnaissance
```bash
# Complete domain analysis
redcalibur domain --target example.com --all

# Specific checks
redcalibur domain --target example.com --whois --dns --ssl
redcalibur domain --target example.com --subdomains
```

#### Network Scanning
```bash
# Port scanning
redcalibur scan --target 192.168.1.1 --ports 80,443,22,21

# Shodan integration
redcalibur scan --target example.com --shodan
```

#### Username Intelligence
```bash
# Multi-platform username lookup
redcalibur username --target johndoe --platforms twitter,linkedin,github

# All supported platforms
redcalibur username --target johndoe
```

#### URL Scanning
```bash
# Scan a URL for malicious activity using VirusTotal
redcalibur urlscan --url http://example.com
```

#### All-in-One Command
```bash
# Run all functionalities and generate a summary report
redcalibur all --target-domain example.com --target-ip 192.168.1.1 --username johndoe --platforms twitter,linkedin --output summary_report
```

#### Report Generation
```bash
# Generate comprehensive reports
redcalibur report --input results.json --format pdf
redcalibur report --input results.json --format both --output custom_name
```

## 📊 Sample Output

```json
{
  "target": "example.com",
  "timestamp": "2025-09-08T01:48:00",
  "whois": {
    "registrar": "Example Registrar",
    "creation_date": "2000-01-01",
    "expiration_date": "2026-01-01"
  },
  "dns": {
    "A": ["93.184.216.34"],
    "MX": ["mail.example.com"]
  },
  "ssl": {
    "issuer": "DigiCert Inc",
    "notAfter": "2025-12-31",
    "subjectAltName": ["example.com", "www.example.com"]
  },
  "ai_summary": "Target shows standard configuration with valid SSL certificate expiring in 2025...",
  "risk_score": 0.3
}
```
### Development Setup
```bash
git clone https://github.com/PraneeshRV/RedCalibur.git
cd RedCalibur
python -m venv dev-env
source dev-env/bin/activate
pip install -e ".[dev]"
```

### Running Tests
```bash
python -m pytest tests/
```


## 🛡️ Security & Ethics

### Responsible Use
- **Educational Purpose**: Designed for security professionals and researchers
- **Legal Compliance**: Ensure you have proper authorization before testing
- **Ethical Guidelines**: Follow responsible disclosure practices
- **Rate Limiting**: Built-in delays to respect target systems

### Disclaimer
⚠️ **IMPORTANT**: This toolkit is for educational and authorized testing purposes only. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical.

## 🤝 Contributing

We welcome contributions!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links
- **Issues**: [Bug Reports](https://github.com/PraneeshRV/RedCalibur/issues)
- **Discussions**: [Community](https://github.com/PraneeshRV/RedCalibur/discussions)

## 🙏 Acknowledgments

- Inspired by the cybersecurity community
- Built with modern AI/ML technologies
- Designed for the next generation of security professionals

---

**RedCalibur** - *Forging the future of automated red teaming* ⚔️