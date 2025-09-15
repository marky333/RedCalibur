#!/usr/bin/env python3
"""
Simple test script for RedCalibur
"""

print("🔍 Testing RedCalibur components...")

try:
    import torch
    print("✅ PyTorch imported successfully")
except ImportError as e:
    print(f"❌ PyTorch import failed: {e}")

try:
    import numpy as np
    print("✅ NumPy imported successfully")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

try:
    from sklearn.ensemble import RandomForestClassifier
    print("✅ Scikit-learn imported successfully")
except ImportError as e:
    print(f"❌ Scikit-learn import failed: {e}")

try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from redcalibur.ai_core import AIModelConfig, RedTeamNeuralNet
    print("✅ RedCalibur AI core imported successfully")
except ImportError as e:
    print(f"❌ RedCalibur AI core import failed: {e}")

try:
    from redcalibur.phishing_detection import URLFeatureExtractor, create_sample_dataset
    print("✅ RedCalibur phishing detection imported successfully")
except ImportError as e:
    print(f"❌ RedCalibur phishing detection import failed: {e}")

print("\n🎯 Running basic functionality test...")

try:
    # Test URL feature extraction
    extractor = URLFeatureExtractor()
    features = extractor.extract_features("https://www.google.com")
    print(f"✅ URL feature extraction works: {features.length} characters")
    
    # Test neural network creation
    net = RedTeamNeuralNet(input_size=10, hidden_sizes=[64, 32], output_size=2)
    print("✅ Neural network creation works")
    
    # Test sample dataset
    urls, labels = create_sample_dataset()
    print(f"✅ Sample dataset created: {len(urls)} URLs")
    
    print("\n🎉 All basic tests passed! RedCalibur is ready.")
    
except Exception as e:
    print(f"❌ Functionality test failed: {e}")
    import traceback
    traceback.print_exc()
