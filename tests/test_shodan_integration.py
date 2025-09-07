import pytest
import os
from unittest.mock import patch, MagicMock
from redcalibur.osint.shodan_integration import search_shodan, get_host_info
from dotenv import load_dotenv

load_dotenv()

# Fixture to get the real API key from .env
@pytest.fixture
def shodan_api_key():
    return os.getenv("SHODAN_API_KEY")

@patch('shodan.Shodan')
def test_search_shodan_mocked(mock_shodan, shodan_api_key):
    """Test Shodan search with a mocked API."""
    mock_api = MagicMock()
    mock_api.search.return_value = {'total': 1, 'matches': [{'ip_str': '1.1.1.1'}]}
    mock_shodan.return_value = mock_api

    results = search_shodan(shodan_api_key, "apache")
    assert results is not None
    assert results['total'] == 1
    mock_api.search.assert_called_with("apache")

@patch('shodan.Shodan')
def test_get_host_info_mocked(mock_shodan, shodan_api_key):
    """Test Shodan host info with a mocked API."""
    mock_api = MagicMock()
    mock_api.host.return_value = {'ip_str': '8.8.8.8', 'os': 'Linux'}
    mock_shodan.return_value = mock_api

    host_info = get_host_info(shodan_api_key, "8.8.8.8")
    assert host_info is not None
    assert host_info['os'] == 'Linux'
    mock_api.host.assert_called_with("8.8.8.8")

@pytest.mark.integration
def test_search_shodan_live(shodan_api_key):
    """Test Shodan search with a live API key (integration test)."""
    if not shodan_api_key:
        pytest.skip("SHODAN_API_KEY not found in .env, skipping live test.")
    
    results = search_shodan(shodan_api_key, "apache")
    assert results is not None
    assert "total" in results

@pytest.mark.integration
def test_get_host_info_live(shodan_api_key):
    """Test Shodan host info with a live API key (integration test)."""
    if not shodan_api_key:
        pytest.skip("SHODAN_API_KEY not found in .env, skipping live test.")

    host_info = get_host_info(shodan_api_key, "8.8.8.8")
    assert host_info is not None
    assert "ip_str" in host_info
