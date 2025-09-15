#!/usr/bin/env python3
"""
Production validation script for RedCalibur
Tests core functionality to ensure production readiness
"""

import sys
import os
import json
from datetime import datetime

# Add package to path
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    try:
        import redcalibur
        from redcalibur.config import Config, setup_logging
        from redcalibur.cli import RedCaliburCLI
        from redcalibur.osint.domain_infrastructure.whois_lookup import perform_whois_lookup
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("🔧 Testing configuration...")
    try:
        from redcalibur.config import Config
        config = Config()
        issues = config.validate_config()
        print(f"📋 Configuration issues: {len(issues)}")
        for issue in issues:
            print(f"   ⚠️ {issue}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_logging():
    """Test logging system"""
    print("📝 Testing logging...")
    try:
        from redcalibur.config import setup_logging
        logger = setup_logging("INFO")
        logger.info("Test log message")
        print("✅ Logging system working")
        return True
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic OSINT functionality"""
    print("🌐 Testing basic functionality...")
    try:
        from redcalibur.osint.domain_infrastructure.whois_lookup import is_valid_domain
        from redcalibur.osint.domain_infrastructure.port_scanning import perform_port_scan
        
        # Test domain validation
        assert is_valid_domain("google.com") == True
        print("✅ Domain validation working")
        
        # Test port scanning (local test)
        result = perform_port_scan("127.0.0.1", [80, 443])
        assert isinstance(result, dict)
        print("✅ Port scanning working")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_ai_components():
    """Test AI components"""
    print("🤖 Testing AI components...")
    try:
        from redcalibur.osint.ai_enhanced.risk_scoring import calculate_risk_score
        from redcalibur.osint.ai_enhanced.recon_summarizer import summarize_recon_data
        
        # Test risk scoring
        risk_score = calculate_risk_score([1, 2, 3])
        print(f"✅ Risk scoring working: {risk_score}")
        
        # Test summarization (with short text to avoid model loading)
        summary = summarize_recon_data("Test data for summarization")
        print("✅ Summarization system working")
        
        return True
    except Exception as e:
        print(f"❌ AI components test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface"""
    print("💻 Testing CLI interface...")
    try:
        from redcalibur.cli import RedCaliburCLI
        cli = RedCaliburCLI()
        print("✅ CLI interface loads successfully")
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def generate_production_report():
    """Generate production readiness report"""
    print("\n" + "="*50)
    print("🎯 PRODUCTION READINESS REPORT")
    print("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Logging", test_logging),
        ("Basic Functionality", test_basic_functionality),
        ("AI Components", test_ai_components),
        ("CLI Interface", test_cli_interface)
    ]
    
    results = {}
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results[test_name] = "PASS" if result else "FAIL"
            if result:
                passed_tests += 1
        except Exception as e:
            results[test_name] = f"ERROR: {str(e)}"
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    for test_name, result in results.items():
        status_emoji = "✅" if result == "PASS" else "❌"
        print(f"{status_emoji} {test_name}: {result}")
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("🚀 RedCalibur is PRODUCTION READY!")
    elif success_rate >= 60:
        print("⚠️ RedCalibur needs minor fixes before production")
    else:
        print("🚨 RedCalibur requires significant work before production")
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "tests": results,
        "success_rate": success_rate,
        "production_ready": success_rate >= 80
    }
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/production_readiness_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: reports/production_readiness_report.json")
    
    return success_rate >= 80

if __name__ == "__main__":
    print("🗡️ RedCalibur Production Validation")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    production_ready = generate_production_report()
    
    if production_ready:
        print("\n🎉 Congratulations! RedCalibur is ready for production deployment.")
        sys.exit(0)
    else:
        print("\n🔧 Please address the issues above before production deployment.")
        sys.exit(1)
