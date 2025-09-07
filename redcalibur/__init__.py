"""
🗡️ RedCalibur - AI-Powered Red Teaming Toolkit
===============================================

"Forged at the intersection of artificial intelligence and offensive cybersecurity."

RedCalibur is a modular red teaming toolkit that leverages machine learning 
and large language models (LLMs) to supercharge ethical hacking workflows.

Author: Praneesh R V
Purpose: AI and Neural Networks Major Project
"""

"""
RedCalibur - AI-Powered Red Teaming Toolkit

A comprehensive toolkit for penetration testing and OSINT reconnaissance,
enhanced with artificial intelligence capabilities.

Author: PraneeshRV
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "PraneeshRV"
__email__ = "praneesh@example.com"
__license__ = "MIT"

# Core imports for easy access
from .config import Config, setup_logging

# AI Core components
from .ai_core import (
    NeuralNetwork,
    EnsembleModel,
    TransformerClassifier,
    FeatureExtractor,
    ModelTrainer,
    AIModelManager,
    GPTAnalyzer,
    AnthropicAnalyzer,
    ModelConfig
)

# Phishing Detection
from .phishing_detection import AIPhishingDetector, create_sample_dataset

# Make commonly used functions available at package level
__all__ = [
    "Config",
    "setup_logging",
    "AIPhishingDetector",
    "create_sample_dataset",
    "NeuralNetwork",
    "EnsembleModel",
    "TransformerClassifier",
    "__version__",
    "__author__"
]

# Package metadata
metadata = {
    "name": "RedCalibur",
    "version": __version__,
    "description": "AI-Powered Red Teaming Toolkit",
    "author": __author__,
    "license": __license__,
    "url": "https://github.com/PraneeshRV/RedCalibur"
}
__email__ = "praneeshrv404@gmail.com"
__description__ = "AI-Powered Red Teaming Toolkit"

from .ai_core import (
    BaseAIModel,
    TransformerClassifier,
    RedTeamNeuralNet,
    LLMIntegration,
    EnsembleAISystem,
    create_phishing_detector,
    create_neural_classifier,
    create_llm_integration
)

__all__ = [
    'BaseAIModel',
    'TransformerClassifier', 
    'RedTeamNeuralNet',
    'LLMIntegration',
    'EnsembleAISystem',
    'create_phishing_detector',
    'create_neural_classifier',
    'create_llm_integration'
]
