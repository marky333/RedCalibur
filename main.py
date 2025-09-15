#!/usr/bin/env python3
"""
RedCalibur Main Interface
========================

Command-line interface for the AI-powered red teaming toolkit.
"""

import argparse
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
    
    args = parser.parse_args()
    
    if args.module == 'phishing':
        detector = AIPhishingDetector()
        
        if args.train or args.demo:
            print("🧠 Initializing AI models...")
            detector.initialize_transformer()
            
            print("📊 Creating sample dataset...")
            urls, labels = create_sample_dataset()
            
            print("🎯 Training neural networks...")
            detector.train_neural_network(urls, labels, epochs=50)
            
            if args.demo:
                test_urls = [
                    "https://www.google.com",
                    "http://suspicious-bank-login.com/verify",
                    "https://paypa1-security.com/update"
                ]
                
                print("\n🔍 Analyzing test URLs...")
                for url in test_urls:
                    result = detector.predict_url(url)
                    status = "🚨 PHISHING" if result['final_prediction']['is_phishing'] else "✅ LEGITIMATE"
                    confidence = result['final_prediction']['confidence']
                    print(f"{status} - {url} (Confidence: {confidence:.2f})")
        
        elif args.url:
            print(f"🔍 Analyzing: {args.url}")
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
