"""
AI-Powered Phishing Detection Module
===================================

This module implements neural networks and machine learning models
to detect phishing URLs, emails, and websites using various AI techniques.

Features:
- URL feature extraction and analysis
- Neural network-based classification
- Transformer models for text analysis
- Ensemble methods for improved accuracy
"""

import re
import requests
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
import tldextract
from dataclasses import dataclass

import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from ..ai_core import TransformerClassifier, RedTeamNeuralNet, AIModelConfig


@dataclass
class URLFeatures:
    """Structured representation of URL features for ML models."""
    length: int
    num_dots: int
    num_subdomains: int
    num_special_chars: int
    has_ip: bool
    has_suspicious_words: bool
    domain_age: Optional[int]
    ssl_cert_valid: bool
    redirect_count: int
    entropy: float


class URLFeatureExtractor:
    """
    Extract features from URLs for machine learning models.
    
    This class implements various feature extraction techniques
    commonly used in cybersecurity research for phishing detection.
    """
    
    SUSPICIOUS_WORDS = [
        'secure', 'account', 'update', 'confirm', 'login', 'verify',
        'bank', 'paypal', 'amazon', 'microsoft', 'apple', 'google',
        'suspend', 'limited', 'restricted', 'unusual', 'activity'
    ]
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    
    def extract_features(self, url: str) -> URLFeatures:
        """Extract comprehensive features from a URL."""
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        return URLFeatures(
            length=len(url),
            num_dots=url.count('.'),
            num_subdomains=len(extracted.subdomain.split('.')) if extracted.subdomain else 0,
            num_special_chars=sum(1 for c in url if not c.isalnum() and c not in '.:/-'),
            has_ip=self._has_ip_address(parsed.netloc),
            has_suspicious_words=self._has_suspicious_words(url),
            domain_age=self._get_domain_age(extracted.domain),
            ssl_cert_valid=self._check_ssl_certificate(url),
            redirect_count=self._count_redirects(url),
            entropy=self._calculate_entropy(url)
        )
    
    def _has_ip_address(self, netloc: str) -> bool:
        """Check if URL contains IP address instead of domain."""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return bool(re.search(ip_pattern, netloc))
    
    def _has_suspicious_words(self, url: str) -> bool:
        """Check for suspicious words commonly used in phishing."""
        url_lower = url.lower()
        return any(word in url_lower for word in self.SUSPICIOUS_WORDS)
    
    def _get_domain_age(self, domain: str) -> Optional[int]:
        """Get domain age (placeholder - would need WHOIS integration)."""
        # This would integrate with python-whois in real implementation
        return None
    
    def _check_ssl_certificate(self, url: str) -> bool:
        """Check SSL certificate validity."""
        try:
            response = requests.head(url, timeout=5, verify=True)
            return response.status_code < 400
        except:
            return False
    
    def _count_redirects(self, url: str) -> int:
        """Count number of redirects."""
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            return len(response.history)
        except:
            return 0
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of the URL."""
        if not text:
            return 0
        
        entropy = 0
        for char in set(text):
            prob = text.count(char) / len(text)
            entropy -= prob * np.log2(prob)
        
        return entropy
    
    def features_to_vector(self, features: URLFeatures) -> np.ndarray:
        """Convert URLFeatures to numpy array for ML models."""
        return np.array([
            features.length,
            features.num_dots,
            features.num_subdomains,
            features.num_special_chars,
            int(features.has_ip),
            int(features.has_suspicious_words),
            features.domain_age or 0,
            int(features.ssl_cert_valid),
            features.redirect_count,
            features.entropy
        ])


class PhishingNeuralNetwork(nn.Module):
    """
    Deep Neural Network for Phishing Detection
    
    This neural network is specifically designed for phishing detection
    using URL features and text analysis.
    """
    
    def __init__(self, feature_size: int = 10, embedding_dim: int = 128):
        super(PhishingNeuralNetwork, self).__init__()
        
        # Feature processing layers
        self.feature_net = nn.Sequential(
            nn.Linear(feature_size, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.3),
            
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.2),
        )
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(16, 2)  # Binary classification: phishing vs legitimate
        )
        
    def forward(self, features):
        x = self.feature_net(features)
        output = self.classifier(x)
        return output


class AIPhishingDetector:
    """
    AI-Powered Phishing Detection System
    
    This class combines multiple AI models for comprehensive phishing detection:
    - Neural networks for URL feature analysis
    - Transformer models for content analysis
    - Ensemble methods for improved accuracy
    """
    
    def __init__(self):
        self.feature_extractor = URLFeatureExtractor()
        self.neural_net = PhishingNeuralNetwork()
        self.transformer_model = None
        self.ensemble_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Move neural network to device
        self.neural_net.to(self.device)
        
    def initialize_transformer(self, model_name: str = "distilbert-base-uncased"):
        """Initialize transformer model for text analysis."""
        config = AIModelConfig(
            model_name=model_name,
            model_type='transformer',
            max_length=256
        )
        self.transformer_model = TransformerClassifier(config)
    
    def train_neural_network(self, urls: List[str], labels: List[int], epochs: int = 100):
        """
        Train the neural network on URL data.
        
        Args:
            urls: List of URLs
            labels: List of labels (0 = legitimate, 1 = phishing)
            epochs: Number of training epochs
        """
        # Extract features
        features = []
        for url in urls:
            url_features = self.feature_extractor.extract_features(url)
            feature_vector = self.feature_extractor.features_to_vector(url_features)
            features.append(feature_vector)
        
        X = np.array(features)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Convert to tensors
        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        y_train_tensor = torch.LongTensor(y_train).to(self.device)
        X_test_tensor = torch.FloatTensor(X_test).to(self.device)
        y_test_tensor = torch.LongTensor(y_test).to(self.device)
        
        # Training setup
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.neural_net.parameters(), lr=0.001)
        
        # Training loop
        self.neural_net.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.neural_net(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
        
        # Evaluation
        self.neural_net.eval()
        with torch.no_grad():
            test_outputs = self.neural_net(X_test_tensor)
            _, predicted = torch.max(test_outputs.data, 1)
            accuracy = (predicted == y_test_tensor).sum().item() / len(y_test_tensor)
            print(f'Neural Network Test Accuracy: {accuracy:.4f}')
        
        # Train ensemble model
        self.ensemble_model.fit(X_train, y_train)
        ensemble_accuracy = self.ensemble_model.score(X_test, y_test)
        print(f'Ensemble Model Test Accuracy: {ensemble_accuracy:.4f}')
    
    def predict_url(self, url: str) -> Dict[str, any]:
        """
        Predict if a URL is phishing using AI models.
        
        Returns:
            Dictionary with predictions from different models
        """
        # Extract features
        url_features = self.feature_extractor.extract_features(url)
        feature_vector = self.feature_extractor.features_to_vector(url_features)
        
        results = {
            'url': url,
            'features': url_features,
            'predictions': {}
        }
        
        # Neural network prediction
        feature_tensor = torch.FloatTensor(feature_vector).unsqueeze(0).to(self.device)
        self.neural_net.eval()
        with torch.no_grad():
            nn_output = self.neural_net(feature_tensor)
            nn_probs = torch.nn.functional.softmax(nn_output, dim=1)
            nn_prediction = torch.argmax(nn_probs, dim=1).item()
            nn_confidence = torch.max(nn_probs).item()
        
        results['predictions']['neural_network'] = {
            'prediction': nn_prediction,
            'confidence': nn_confidence,
            'probabilities': nn_probs.cpu().numpy().tolist()[0]
        }
        
        # Ensemble prediction
        ensemble_pred = self.ensemble_model.predict([feature_vector])[0]
        ensemble_proba = self.ensemble_model.predict_proba([feature_vector])[0]
        
        results['predictions']['ensemble'] = {
            'prediction': ensemble_pred,
            'confidence': max(ensemble_proba),
            'probabilities': ensemble_proba.tolist()
        }
        
        # Transformer prediction (if available)
        if self.transformer_model:
            transformer_result = self.transformer_model.predict(url)
            results['predictions']['transformer'] = transformer_result
        
        # Final ensemble decision
        predictions = [
            results['predictions']['neural_network']['prediction'],
            results['predictions']['ensemble']['prediction']
        ]
        final_prediction = max(set(predictions), key=predictions.count)
        
        results['final_prediction'] = {
            'is_phishing': bool(final_prediction),
            'confidence': np.mean([
                results['predictions']['neural_network']['confidence'],
                results['predictions']['ensemble']['confidence']
            ])
        }
        
        return results
    
    def analyze_website_content(self, url: str) -> Dict[str, any]:
        """Analyze website content for phishing indicators."""
        try:
            response = requests.get(url, timeout=10)
            content = response.text
            
            # Use transformer for content analysis if available
            if self.transformer_model:
                content_analysis = self.transformer_model.predict(content)
                return {
                    'url': url,
                    'content_length': len(content),
                    'analysis': content_analysis
                }
            else:
                return {
                    'url': url,
                    'content_length': len(content),
                    'analysis': 'Transformer model not initialized'
                }
        
        except Exception as e:
            return {
                'url': url,
                'error': str(e)
            }


def create_sample_dataset() -> Tuple[List[str], List[int]]:
    """Create a sample dataset for demonstration purposes."""
    # Legitimate URLs
    legitimate_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
        "https://www.microsoft.com"
    ]
    
    # Phishing URLs (simulated - for educational purposes)
    phishing_urls = [
        "http://goog1e.com/secure/login",
        "https://paypa1-security.com/update",
        "http://192.168.1.1/amazon-login",
        "https://microsoft-verify.suspicious.com",
        "http://github-security-alert.com"
    ]
    
    urls = legitimate_urls + phishing_urls
    labels = [0] * len(legitimate_urls) + [1] * len(phishing_urls)
    
    return urls, labels


# Example usage and demonstration
if __name__ == "__main__":
    # Create detector
    detector = AIPhishingDetector()
    
    # Initialize transformer model
    detector.initialize_transformer()
    
    # Create sample dataset
    urls, labels = create_sample_dataset()
    
    # Train the models
    print("Training AI models for phishing detection...")
    detector.train_neural_network(urls, labels, epochs=50)
    
    # Test predictions
    test_url = "http://suspicious-bank-login.com/verify"
    result = detector.predict_url(test_url)
    
    print(f"\nAnalysis for: {test_url}")
    print(f"Final prediction: {'PHISHING' if result['final_prediction']['is_phishing'] else 'LEGITIMATE'}")
    print(f"Confidence: {result['final_prediction']['confidence']:.2f}")
