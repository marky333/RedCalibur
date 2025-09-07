#!/usr/bin/env python3
"""
RedCalibur Main Interface - Simplified Demo
==========================================

Command-line interface for the AI-powered red teaming toolkit.
This version focuses on the custom neural networks without requiring
large transformer model downloads.
"""

import argparse
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from redcalibur.phishing_detection import AIPhishingDetector, create_sample_dataset

def main():
    parser = argparse.ArgumentParser(
        description="RedCalibur - AI-Powered Red Teaming Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='module', help='Available modules')
    
    # Phishing detection module
    phishing_parser = subparsers.add_parser('phishing', help='Phishing detection tools')
    phishing_parser.add_argument('--url', type=str, help='URL to analyze')
    phishing_parser.add_argument('--train', action='store_true', help='Train models with sample data')
    phishing_parser.add_argument('--demo', action='store_true', help='Run demonstration')
    phishing_parser.add_argument('--simple', action='store_true', help='Run simple demo without transformers')
    
    args = parser.parse_args()
    
    if args.module == 'phishing':
        detector = AIPhishingDetector()
        
        if args.train or args.demo or args.simple:
            print("🧠 Initializing AI models...")
            
            # Skip transformer initialization for simple demo
            if not args.simple:
                try:
                    print("⚠️  Note: Transformer model download may take time or fail...")
                    detector.initialize_transformer()
                    print("✅ Transformer model loaded successfully!")
                except Exception as e:
                    print(f"⚠️  Transformer loading failed: {e}")
                    print("🔄 Continuing with neural network only...")
            
            print("📊 Creating sample dataset...")
            urls, labels = create_sample_dataset()
            
            print("🎯 Training neural networks...")
            detector.train_neural_network(urls, labels, epochs=50)
            
            if args.demo or args.simple:
                test_urls = [
                    "https://www.google.com",
                    "http://suspicious-bank-login.com/verify", 
                    "https://paypa1-security.com/update",
                    "http://192.168.1.1/amazon-login",
                    "https://microsoft-verify.suspicious.com"
                ]
                
                print("\n🔍 Analyzing test URLs...")
                for url in test_urls:
                    try:
                        result = detector.predict_url(url)
                        status = "🚨 PHISHING" if result['final_prediction']['is_phishing'] else "✅ LEGITIMATE"
                        confidence = result['final_prediction']['confidence']
                        print(f"{status} - {url}")
                        print(f"   Confidence: {confidence:.2f}")
                        print(f"   Neural Net: {result['predictions']['neural_network']['prediction']}")
                        print(f"   Ensemble: {result['predictions']['ensemble']['prediction']}")
                        print()
                    except Exception as e:
                        print(f"❌ Error analyzing {url}: {e}")
        
        elif args.url:
            print(f"🔍 Analyzing: {args.url}")
            
            # Train a quick model first
            print("📊 Training models with sample data...")
            urls, labels = create_sample_dataset()
            detector.train_neural_network(urls, labels, epochs=30)
            
            result = detector.predict_url(args.url)
            
            status = "🚨 PHISHING" if result['final_prediction']['is_phishing'] else "✅ LEGITIMATE"
            confidence = result['final_prediction']['confidence']
            
            print(f"\nResult: {status}")
            print(f"Confidence: {confidence:.2f}")
            print(f"Neural Network Prediction: {result['predictions']['neural_network']['prediction']}")
            print(f"Ensemble Prediction: {result['predictions']['ensemble']['prediction']}")
        
        else:
            phishing_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
