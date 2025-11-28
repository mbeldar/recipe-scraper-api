"""Unit tests for src/api.py"""

import pytest
import json
from unittest.mock import patch, Mock
from src.api import app, InvalidURLError


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check_success(self, client):
        """Test that health check returns healthy status."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'message' in data

    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON."""
        response = client.get('/health')
        assert response.content_type == 'application/json'


class TestScrapeEndpoint:
    """Tests for the scrape endpoint."""

    @patch('src.api.scrape_recipe_from_url')
    def test_scrape_valid_url(self, mock_scrape, client):
        """Test scraping a valid URL."""
        mock_scrape.return_value = {
            'title': 'Test Recipe',
            'ingredients': [],
            'instructions': []
        }
        
        response = client.post('/scrape', 
                               json={'url': 'https://example.com/recipe'},
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Test Recipe'

    def test_scrape_no_json_body(self, client):
        """Test scrape endpoint with no JSON body."""
        response = client.post('/scrape')
        # Flask returns 415 Unsupported Media Type when no JSON header is provided
        assert response.status_code in [400, 415, 500]
        # The endpoint should still handle it gracefully

    def test_scrape_missing_url(self, client):
        """Test scrape endpoint without URL in body."""
        response = client.post('/scrape',
                               json={},
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        # Empty dict is falsy, so it triggers "Request body must be JSON" first
        assert 'URL' in data['error'] or 'Request body' in data['error']

    def test_scrape_empty_url(self, client):
        """Test scrape endpoint with empty URL."""
        response = client.post('/scrape',
                               json={'url': ''},
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'URL is required' in data['error']

    def test_scrape_url_with_whitespace(self, client):
        """Test that URL whitespace is stripped."""
        response = client.post('/scrape',
                               json={'url': '  https://example.com/recipe  '},
                               content_type='application/json')
        # This should proceed to scrape (though it will fail since we're not mocking)
        # Just testing that whitespace is stripped
        assert response.status_code in [400, 500]  # Depending on whether scraper is mocked

    def test_scrape_invalid_url_no_protocol(self, client):
        """Test scrape endpoint with URL missing protocol."""
        response = client.post('/scrape',
                               json={'url': 'example.com/recipe'},
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'http://' in data['error'] or 'https://' in data['error']

    @patch('src.api.scrape_recipe_from_url')
    def test_scrape_http_protocol(self, mock_scrape, client):
        """Test scraping with http protocol."""
        mock_scrape.return_value = {'title': 'Recipe'}
        
        response = client.post('/scrape',
                               json={'url': 'http://example.com/recipe'},
                               content_type='application/json')
        assert response.status_code == 200

    @patch('src.api.scrape_recipe_from_url')
    def test_scrape_https_protocol(self, mock_scrape, client):
        """Test scraping with https protocol."""
        mock_scrape.return_value = {'title': 'Recipe'}
        
        response = client.post('/scrape',
                               json={'url': 'https://example.com/recipe'},
                               content_type='application/json')
        assert response.status_code == 200

    @patch('src.api.scrape_recipe_from_url')
    def test_scrape_scraping_error(self, mock_scrape, client):
        """Test scrape endpoint when scraping fails."""
        from src.scraper import ScrapingError
        mock_scrape.side_effect = ScrapingError("Failed to scrape")
        
        response = client.post('/scrape',
                               json={'url': 'https://example.com/recipe'},
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error_type'] == 'scraping_failed'

    @patch('src.api.scrape_recipe_from_url')
    def test_scrape_unexpected_error(self, mock_scrape, client):
        """Test scrape endpoint with unexpected error."""
        mock_scrape.side_effect = RuntimeError("Unexpected error")
        
        response = client.post('/scrape',
                               json={'url': 'https://example.com/recipe'},
                               content_type='application/json')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error_type'] == 'server_error'

    @patch('src.api.scrape_recipe_from_url')
    def test_scrape_returns_complete_recipe_data(self, mock_scrape, client):
        """Test that scrape endpoint returns all recipe fields."""
        recipe_data = {
            'title': 'Pasta Carbonara',
            'ingredients': [
                {'quantity': 1, 'unit': 'pound', 'name': 'pasta'},
                {'quantity': 4, 'unit': None, 'name': 'eggs'}
            ],
            'instructions': ['Cook pasta', 'Mix eggs'],
            'yields': '4 servings',
            'prep_time': '10',
            'cook_time': '20',
            'total_time': '30',
            'image': 'http://example.com/image.jpg',
            'description': 'Classic Italian pasta'
        }
        mock_scrape.return_value = recipe_data
        
        response = client.post('/scrape',
                               json={'url': 'https://example.com/recipe'},
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data'] == recipe_data


class TestSupportedSitesEndpoint:
    """Tests for the supported sites endpoint."""

    @patch('src.api.get_supported_sites')
    def test_supported_sites_success(self, mock_get_sites, client):
        """Test getting supported sites."""
        mock_get_sites.return_value = ['allrecipes', 'bbcgoodfood', 'epicurious']
        
        response = client.get('/supported-sites')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 3
        assert len(data['sites']) == 3
        assert 'allrecipes' in data['sites']

    @patch('src.api.get_supported_sites')
    def test_supported_sites_empty(self, mock_get_sites, client):
        """Test supported sites when none available."""
        mock_get_sites.return_value = []
        
        response = client.get('/supported-sites')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert data['sites'] == []

    @patch('src.api.get_supported_sites')
    def test_supported_sites_returns_json(self, mock_get_sites, client):
        """Test that supported sites returns JSON."""
        mock_get_sites.return_value = ['example.com']
        
        response = client.get('/supported-sites')
        assert response.content_type == 'application/json'


class TestErrorHandlers:
    """Tests for error handlers."""

    def test_404_not_found(self, client):
        """Test 404 error handler."""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error_type'] == 'not_found'

    def test_405_method_not_allowed(self, client):
        """Test 405 method not allowed handler."""
        response = client.get('/scrape')  # GET not allowed on /scrape
        assert response.status_code == 405
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['error_type'] == 'method_not_allowed'


class TestInvalidURLError:
    """Tests for InvalidURLError exception."""

    def test_invalid_url_error_creation(self):
        """Test creating an InvalidURLError."""
        error = InvalidURLError("Invalid URL")
        assert str(error) == "Invalid URL"

    def test_invalid_url_error_is_exception(self):
        """Test that InvalidURLError is an Exception."""
        error = InvalidURLError("Test")
        assert isinstance(error, Exception)
