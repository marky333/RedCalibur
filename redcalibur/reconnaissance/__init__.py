"""
AI-Powered Reconnaissance Module
==============================

This module implements intelligent reconnaissance capabilities using AI:
- Automated OSINT with LLM summarization
- AI-powered target analysis
- Neural network-based threat assessment
- Smart data correlation and insights
"""

import asyncio
import json
import logging
import socket
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import re

import requests
import whois
import numpy as np
from urllib.parse import urlparse
import dns.resolver

from ..ai_core import LLMIntegration, TransformerClassifier, AIModelConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ReconTarget:
    """Data structure for reconnaissance targets."""
    domain: str
    ip_addresses: List[str] = None
    subdomains: List[str] = None
    emails: List[str] = None
    technologies: List[str] = None
    vulnerabilities: List[str] = None
    social_media: Dict[str, str] = None
    threat_score: float = 0.0
    
    def __post_init__(self):
        if self.ip_addresses is None:
            self.ip_addresses = []
        if self.subdomains is None:
            self.subdomains = []
        if self.emails is None:
            self.emails = []
        if self.technologies is None:
            self.technologies = []
        if self.vulnerabilities is None:
            self.vulnerabilities = []
        if self.social_media is None:
            self.social_media = {}


class IntelligentWhoisAnalyzer:
    """AI-enhanced WHOIS analysis with threat intelligence."""
    
    def __init__(self, llm_integration: Optional[LLMIntegration] = None):
        self.llm = llm_integration
    
    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Perform AI-enhanced WHOIS analysis."""
        try:
            # Get WHOIS data
            w = whois.whois(domain)
            
            # Extract basic information
            whois_data = {
                'domain': domain,
                'registrar': getattr(w, 'registrar', None),
                'creation_date': getattr(w, 'creation_date', None),
                'expiration_date': getattr(w, 'expiration_date', None),
                'name_servers': getattr(w, 'name_servers', []),
                'emails': getattr(w, 'emails', []),
                'country': getattr(w, 'country', None),
                'org': getattr(w, 'org', None)
            }
            
            # AI analysis
            ai_analysis = self._ai_analyze_whois(whois_data)
            
            return {
                'whois_data': whois_data,
                'ai_analysis': ai_analysis,
                'risk_score': self._calculate_risk_score(whois_data)
            }
            
        except Exception as e:
            logger.error(f"WHOIS analysis failed for {domain}: {e}")
            return {'error': str(e)}
    
    def _ai_analyze_whois(self, whois_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze WHOIS data for suspicious patterns."""
        if not self.llm:
            return {'analysis': 'No LLM integration available'}
        
        # Prepare prompt for LLM analysis
        prompt = f"""
        Analyze this WHOIS data for potential security concerns:
        
        Domain: {whois_data.get('domain')}
        Registrar: {whois_data.get('registrar')}
        Creation Date: {whois_data.get('creation_date')}
        Expiration Date: {whois_data.get('expiration_date')}
        Name Servers: {whois_data.get('name_servers')}
        Country: {whois_data.get('country')}
        Organization: {whois_data.get('org')}
        
        Identify any red flags, suspicious patterns, or security concerns.
        Provide a threat assessment and recommendations.
        """
        
        # This would be implemented with async call in practice
        analysis = self.llm.analyze_for_red_team(json.dumps(whois_data), 'vulnerability')
        
        return analysis
    
    def _calculate_risk_score(self, whois_data: Dict[str, Any]) -> float:
        """Calculate risk score based on WHOIS data patterns."""
        score = 0.0
        
        # Recently registered domains are higher risk
        creation_date = whois_data.get('creation_date')
        if creation_date:
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if isinstance(creation_date, datetime):
                days_old = (datetime.now() - creation_date).days
                if days_old < 30:
                    score += 0.3
                elif days_old < 90:
                    score += 0.1
        
        # Suspicious registrars or privacy protection
        registrar = whois_data.get('registrar', '').lower()
        if any(term in registrar for term in ['privacy', 'protection', 'guard']):
            score += 0.2
        
        # Suspicious countries
        country = whois_data.get('country', '').lower()
        high_risk_countries = ['cn', 'ru', 'pk', 'ng']  # Example list
        if country in high_risk_countries:
            score += 0.1
        
        return min(score, 1.0)


class AIReconEngine:
    """
    AI-Powered Reconnaissance Engine
    
    This engine combines multiple reconnaissance techniques with AI analysis:
    - Intelligent subdomain discovery
    - AI-enhanced port scanning
    - Neural network threat assessment
    - LLM-based report generation
    """
    
    def __init__(self):
        self.llm = None
        self.whois_analyzer = IntelligentWhoisAnalyzer()
        self.threat_classifier = None
        
    def set_llm_integration(self, llm: LLMIntegration):
        """Set LLM integration for AI analysis."""
        self.llm = llm
        self.whois_analyzer.llm = llm
    
    def initialize_threat_classifier(self):
        """Initialize threat classification model."""
        config = AIModelConfig(
            model_name="distilbert-base-uncased",
            model_type='transformer',
            max_length=512
        )
        self.threat_classifier = TransformerClassifier(config)
    
    async def comprehensive_recon(self, target: str) -> ReconTarget:
        """Perform comprehensive reconnaissance on a target."""
        logger.info(f"Starting comprehensive reconnaissance on: {target}")
        
        recon_target = ReconTarget(domain=target)
        
        # Parallel reconnaissance tasks
        tasks = [
            self._dns_enumeration(target),
            self._subdomain_discovery(target),
            self._port_scanning(target),
            self._technology_detection(target),
            self._email_harvesting(target),
            self._social_media_discovery(target)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        dns_result, subdomains, ports, tech, emails, social = results
        
        if not isinstance(dns_result, Exception):
            recon_target.ip_addresses = dns_result
        
        if not isinstance(subdomains, Exception):
            recon_target.subdomains = subdomains
        
        if not isinstance(tech, Exception):
            recon_target.technologies = tech
        
        if not isinstance(emails, Exception):
            recon_target.emails = emails
        
        if not isinstance(social, Exception):
            recon_target.social_media = social
        
        # AI-powered threat assessment
        recon_target.threat_score = await self._ai_threat_assessment(recon_target)
        
        # WHOIS analysis
        whois_result = self.whois_analyzer.analyze_domain(target)
        
        logger.info(f"Reconnaissance completed for: {target}")
        return recon_target, whois_result
    
    async def _dns_enumeration(self, domain: str) -> List[str]:
        """Perform DNS enumeration to find IP addresses."""
        ip_addresses = []
        
        try:
            # A records
            answers = dns.resolver.resolve(domain, 'A')
            for answer in answers:
                ip_addresses.append(str(answer))
            
            # AAAA records (IPv6)
            try:
                answers = dns.resolver.resolve(domain, 'AAAA')
                for answer in answers:
                    ip_addresses.append(str(answer))
            except:
                pass
                
        except Exception as e:
            logger.error(f"DNS enumeration failed for {domain}: {e}")
        
        return ip_addresses
    
    async def _subdomain_discovery(self, domain: str) -> List[str]:
        """Intelligent subdomain discovery using AI-enhanced techniques."""
        subdomains = []
        
        # Common subdomain wordlist
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging',
            'api', 'blog', 'shop', 'forum', 'support', 'docs',
            'cdn', 'secure', 'login', 'portal', 'dashboard'
        ]
        
        for subdomain in common_subdomains:
            full_domain = f"{subdomain}.{domain}"
            try:
                socket.gethostbyname(full_domain)
                subdomains.append(full_domain)
            except socket.gaierror:
                pass
        
        # AI-enhanced subdomain prediction
        if self.llm:
            ai_subdomains = await self._ai_subdomain_prediction(domain, subdomains)
            subdomains.extend(ai_subdomains)
        
        return list(set(subdomains))
    
    async def _ai_subdomain_prediction(self, domain: str, found_subdomains: List[str]) -> List[str]:
        """Use AI to predict additional subdomains based on patterns."""
        if not self.llm:
            return []
        
        prompt = f"""
        Based on the domain '{domain}' and these discovered subdomains: {found_subdomains}
        
        Predict additional likely subdomains that might exist.
        Consider:
        - Industry patterns
        - Technology stack indicators
        - Common naming conventions
        - Security-related subdomains
        
        Return only the subdomain names (without the domain), one per line.
        """
        
        try:
            response = await self.llm.generate_response(prompt, max_tokens=200)
            predicted_subdomains = [
                line.strip() for line in response.split('\n') 
                if line.strip() and '.' not in line.strip()
            ]
            
            # Validate predicted subdomains
            valid_subdomains = []
            for subdomain in predicted_subdomains[:10]:  # Limit to 10 predictions
                full_domain = f"{subdomain}.{domain}"
                try:
                    socket.gethostbyname(full_domain)
                    valid_subdomains.append(full_domain)
                except socket.gaierror:
                    pass
            
            return valid_subdomains
            
        except Exception as e:
            logger.error(f"AI subdomain prediction failed: {e}")
            return []
    
    async def _port_scanning(self, target: str) -> Dict[str, List[int]]:
        """Perform intelligent port scanning."""
        # This is a simplified version - real implementation would use nmap
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        return {'open_ports': open_ports}
    
    async def _technology_detection(self, domain: str) -> List[str]:
        """Detect technologies used by the target."""
        technologies = []
        
        try:
            url = f"https://{domain}"
            response = requests.get(url, timeout=10, verify=False)
            
            # Analyze headers
            headers = response.headers
            
            # Server detection
            server = headers.get('Server', '')
            if server:
                technologies.append(f"Server: {server}")
            
            # Framework detection
            powered_by = headers.get('X-Powered-By', '')
            if powered_by:
                technologies.append(f"Framework: {powered_by}")
            
            # Content analysis
            content = response.text.lower()
            
            # Technology patterns
            tech_patterns = {
                'WordPress': r'wp-content|wordpress',
                'Drupal': r'drupal',
                'Joomla': r'joomla',
                'React': r'react',
                'Angular': r'angular',
                'Vue.js': r'vue\.js|vuejs',
                'jQuery': r'jquery',
                'Bootstrap': r'bootstrap'
            }
            
            for tech, pattern in tech_patterns.items():
                if re.search(pattern, content):
                    technologies.append(tech)
            
        except Exception as e:
            logger.error(f"Technology detection failed for {domain}: {e}")
        
        return list(set(technologies))
    
    async def _email_harvesting(self, domain: str) -> List[str]:
        """Harvest emails related to the domain."""
        emails = []
        
        try:
            # Search for emails on the website
            url = f"https://{domain}"
            response = requests.get(url, timeout=10, verify=False)
            
            # Email regex pattern
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, response.text)
            
            # Filter emails related to the domain
            for email in found_emails:
                if domain in email:
                    emails.append(email)
            
        except Exception as e:
            logger.error(f"Email harvesting failed for {domain}: {e}")
        
        return list(set(emails))
    
    async def _social_media_discovery(self, domain: str) -> Dict[str, str]:
        """Discover social media profiles associated with the domain."""
        social_media = {}
        
        # Common social media platforms
        platforms = {
            'Twitter': f"https://twitter.com/{domain.split('.')[0]}",
            'LinkedIn': f"https://linkedin.com/company/{domain.split('.')[0]}",
            'Facebook': f"https://facebook.com/{domain.split('.')[0]}",
            'Instagram': f"https://instagram.com/{domain.split('.')[0]}"
        }
        
        for platform, url in platforms.items():
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    social_media[platform] = url
            except:
                pass
        
        return social_media
    
    async def _ai_threat_assessment(self, target: ReconTarget) -> float:
        """AI-powered threat assessment of the target."""
        if not self.llm:
            return 0.5  # Default medium risk
        
        # Prepare data for AI analysis
        target_data = asdict(target)
        
        prompt = f"""
        Assess the cybersecurity threat level of this reconnaissance target:
        
        {json.dumps(target_data, indent=2, default=str)}
        
        Consider:
        - Technology stack vulnerabilities
        - Exposed services and ports
        - Domain reputation indicators
        - Infrastructure complexity
        
        Provide a threat score from 0.0 (low risk) to 1.0 (high risk).
        Return only the numeric score.
        """
        
        try:
            response = await self.llm.generate_response(prompt, max_tokens=50)
            
            # Extract numeric score
            score_match = re.search(r'0\.\d+|1\.0', response)
            if score_match:
                return float(score_match.group())
            else:
                return 0.5
                
        except Exception as e:
            logger.error(f"AI threat assessment failed: {e}")
            return 0.5
    
    async def generate_recon_report(self, target: ReconTarget, whois_data: Dict) -> str:
        """Generate AI-powered reconnaissance report."""
        if not self.llm:
            return self._generate_basic_report(target, whois_data)
        
        prompt = f"""
        Generate a comprehensive cybersecurity reconnaissance report for:
        
        Target Data:
        {json.dumps(asdict(target), indent=2, default=str)}
        
        WHOIS Data:
        {json.dumps(whois_data, indent=2, default=str)}
        
        Include:
        1. Executive Summary
        2. Target Profile
        3. Attack Surface Analysis
        4. Vulnerabilities and Risks
        5. Recommendations
        
        Format as a professional security assessment report.
        """
        
        try:
            report = await self.llm.generate_response(prompt, max_tokens=2000)
            return report
        except Exception as e:
            logger.error(f"AI report generation failed: {e}")
            return self._generate_basic_report(target, whois_data)
    
    def _generate_basic_report(self, target: ReconTarget, whois_data: Dict) -> str:
        """Generate basic report without AI."""
        report = f"""
# Reconnaissance Report: {target.domain}

## Target Summary
- Domain: {target.domain}
- IP Addresses: {', '.join(target.ip_addresses)}
- Threat Score: {target.threat_score:.2f}

## Discovered Assets
- Subdomains: {len(target.subdomains)} found
- Technologies: {', '.join(target.technologies)}
- Email Addresses: {len(target.emails)} found

## WHOIS Information
- Registrar: {whois_data.get('whois_data', {}).get('registrar', 'Unknown')}
- Risk Score: {whois_data.get('risk_score', 0.0):.2f}

## Recommendations
- Review exposed services
- Monitor for vulnerabilities
- Implement security controls
        """
        
        return report


# Example usage
async def example_reconnaissance():
    """Example of how to use the AI reconnaissance engine."""
    engine = AIReconEngine()
    
    # Initialize AI components
    # llm = LLMIntegration('openai')  # Uncomment when API keys are available
    # engine.set_llm_integration(llm)
    engine.initialize_threat_classifier()
    
    # Perform reconnaissance
    target, whois_data = await engine.comprehensive_recon("example.com")
    
    # Generate report
    report = await engine.generate_recon_report(target, whois_data)
    
    print("Reconnaissance Complete!")
    print(f"Threat Score: {target.threat_score:.2f}")
    print(f"Subdomains found: {len(target.subdomains)}")
    print(f"Technologies: {', '.join(target.technologies)}")


if __name__ == "__main__":
    asyncio.run(example_reconnaissance())
