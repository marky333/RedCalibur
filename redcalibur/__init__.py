"""
🗡️ RedCalibur - AI-Powered Red Teaming Toolkit
===============================================

"Forged at the intersection of artificial intelligence and offensive cybersecurity."

RedCalibur is a modular red teaming toolkit that leverages machine learning 
and large language models (LLMs) to supercharge ethical hacking workflows.

Author: Praneesh R V
Purpose: AI and Neural Networks Major Project
"""

__version__ = "0.1.0"
__author__ = "Praneesh R V"
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
