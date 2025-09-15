import pytest
import os
from unittest.mock import patch, MagicMock
from redcalibur.osint.virustotal_integration import scan_url, get_url_report
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def virustotal_api_key():
    return os.getenv("VIRUSTOTAL_API_KEY")

@patch('requests.post')
def test_scan_url_mocked(mock_post, virustotal_api_key):
    """Test VirusTotal URL scan with a mocked API."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': {'id': 'some-scan-id'}}
    mock_post.return_value = mock_response

    scan_results = scan_url(virustotal_api_key, "http://example.com")
    assert scan_results is not None
    assert 'data' in scan_results

@patch('requests.get')
def test_get_url_report_mocked(mock_get, virustotal_api_key):
    """Test VirusTotal URL report with a mocked API."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': {'attributes': {'status': 'completed'}}}
    mock_get.return_value = mock_response

    report = get_url_report(virustotal_api_key, "some-scan-id")
    assert report is not None
    assert 'attributes' in report['data']

@pytest.mark.integration
def test_scan_url_live(virustotal_api_key):
    """Test VirusTotal URL scan with a live API key."""
    if not virustotal_api_key:
        pytest.skip("VIRUSTOTAL_API_KEY not found in .env, skipping live test.")
    
    # This is a safe, well-known URL for testing
    scan_results = scan_url(virustotal_api_key, "http://example.com")
    assert scan_results is not None
    assert "data" in scan_results

# Note: A live test for get_url_report would require a valid, recent scan ID.
# This is harder to automate reliably without first running a scan and waiting.
# The mocked test provides good coverage for the function's logic.
