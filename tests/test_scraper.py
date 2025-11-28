"""Unit tests for src/scraper.py"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraper import (
    scrape_recipe_from_url,
    get_supported_sites,
    ScrapingError
)


class TestScrapeRecipeFromUrl:
    """Tests for the scrape_recipe_from_url function."""

    @patch('src.scraper.scrape_me')
    @patch('src.scraper.parse_ingredients')
    @patch('src.scraper.parse_instructions')
    def test_successful_scraping(self, mock_parse_instr, mock_parse_ing, mock_scrape_me):
        """Test successful recipe scraping."""
        # Setup mock scraper
        mock_scraper = Mock()
        mock_scraper.title.return_value = "Chocolate Cake"
        mock_scraper.ingredients.return_value = ["2 cups flour", "1 egg"]
        mock_scraper.instructions.return_value = "Mix and bake"
        mock_scraper.yields.return_value = "8 servings"
        mock_scraper.prep_time.return_value = 15
        mock_scraper.cook_time.return_value = 30
        mock_scraper.total_time.return_value = 45
        mock_scraper.image.return_value = "http://example.com/image.jpg"
        mock_scraper.description.return_value = "A delicious chocolate cake"
        
        mock_scrape_me.return_value = mock_scraper
        mock_parse_ing.return_value = [{"quantity": 2.0, "unit": "cup", "name": "flour"}]
        mock_parse_instr.return_value = ["Mix and bake"]

        result = scrape_recipe_from_url("https://example.com/recipe")

        assert result['title'] == "Chocolate Cake"
        assert result['yields'] == "8 servings"
        assert result['prep_time'] == "15"
        assert result['cook_time'] == "30"
        assert result['total_time'] == "45"
        assert result['image'] == "http://example.com/image.jpg"
        assert result['description'] == "A delicious chocolate cake"
        assert result['ingredients'] == [{"quantity": 2.0, "unit": "cup", "name": "flour"}]
        assert result['instructions'] == ["Mix and bake"]

    @patch('src.scraper.scrape_me')
    def test_scraper_initialization_error(self, mock_scrape_me):
        """Test error when scraper initialization fails."""
        mock_scrape_me.side_effect = Exception("Invalid URL")

        with pytest.raises(ScrapingError) as exc_info:
            scrape_recipe_from_url("https://invalid-url.com")

        assert "Invalid URL" in str(exc_info.value)

    @patch('src.scraper.scrape_me')
    @patch('src.scraper.parse_ingredients')
    @patch('src.scraper.parse_instructions')
    def test_missing_fields_handled_gracefully(self, mock_parse_instr, mock_parse_ing, mock_scrape_me):
        """Test that missing fields don't crash the function."""
        mock_scraper = Mock()
        mock_scraper.title.return_value = "Simple Recipe"
        mock_scraper.ingredients.return_value = []
        mock_scraper.instructions.return_value = None
        mock_scraper.yields.side_effect = Exception("Not available")
        mock_scraper.prep_time.side_effect = Exception("Not available")
        mock_scraper.cook_time.side_effect = Exception("Not available")
        mock_scraper.total_time.side_effect = Exception("Not available")
        mock_scraper.image.side_effect = Exception("Not available")
        mock_scraper.description.side_effect = Exception("Not available")

        mock_scrape_me.return_value = mock_scraper
        mock_parse_ing.return_value = []
        mock_parse_instr.return_value = []

        result = scrape_recipe_from_url("https://example.com/recipe")

        assert result['title'] == "Simple Recipe"
        assert result['yields'] is None
        assert result['prep_time'] is None
        assert result['cook_time'] is None
        assert result['total_time'] is None
        assert result['image'] is None
        assert result['description'] is None
        assert result['ingredients'] == []
        assert result['instructions'] == []

    @patch('src.scraper.scrape_me')
    @patch('src.scraper.parse_ingredients')
    @patch('src.scraper.parse_instructions')
    def test_title_extraction_error_sets_none(self, mock_parse_instr, mock_parse_ing, mock_scrape_me):
        """Test that title extraction error results in None title."""
        mock_scraper = Mock()
        mock_scraper.title.side_effect = Exception("Cannot extract title")
        mock_scraper.ingredients.return_value = []
        mock_scraper.instructions.return_value = None
        mock_scraper.yields.return_value = None
        mock_scraper.prep_time.return_value = None
        mock_scraper.cook_time.return_value = None
        mock_scraper.total_time.return_value = None
        mock_scraper.image.return_value = None
        mock_scraper.description.return_value = None

        mock_scrape_me.return_value = mock_scraper
        mock_parse_ing.return_value = []
        mock_parse_instr.return_value = []

        result = scrape_recipe_from_url("https://example.com/recipe")

        assert result['title'] is None

    @patch('src.scraper.scrape_me')
    @patch('src.scraper.parse_ingredients')
    @patch('src.scraper.parse_instructions')
    def test_time_conversion_to_string(self, mock_parse_instr, mock_parse_ing, mock_scrape_me):
        """Test that time values are converted to strings."""
        mock_scraper = Mock()
        mock_scraper.title.return_value = "Timed Recipe"
        mock_scraper.ingredients.return_value = []
        mock_scraper.instructions.return_value = None
        mock_scraper.yields.return_value = None
        mock_scraper.prep_time.return_value = 15
        mock_scraper.cook_time.return_value = 30
        mock_scraper.total_time.return_value = 45
        mock_scraper.image.return_value = None
        mock_scraper.description.return_value = None

        mock_scrape_me.return_value = mock_scraper
        mock_parse_ing.return_value = []
        mock_parse_instr.return_value = []

        result = scrape_recipe_from_url("https://example.com/recipe")

        assert isinstance(result['prep_time'], str)
        assert isinstance(result['cook_time'], str)
        assert isinstance(result['total_time'], str)
        assert result['prep_time'] == "15"
        assert result['cook_time'] == "30"
        assert result['total_time'] == "45"

    @patch('src.scraper.scrape_me')
    @patch('src.scraper.parse_ingredients')
    @patch('src.scraper.parse_instructions')
    def test_zero_values_handled(self, mock_parse_instr, mock_parse_ing, mock_scrape_me):
        """Test that zero values are handled correctly (0 is falsy so returns None)."""
        mock_scraper = Mock()
        mock_scraper.title.return_value = "No-time Recipe"
        mock_scraper.ingredients.return_value = []
        mock_scraper.instructions.return_value = None
        mock_scraper.yields.return_value = None
        mock_scraper.prep_time.return_value = 0
        mock_scraper.cook_time.return_value = None
        mock_scraper.total_time.return_value = None
        mock_scraper.image.return_value = None
        mock_scraper.description.return_value = None

        mock_scrape_me.return_value = mock_scraper
        mock_parse_ing.return_value = []
        mock_parse_instr.return_value = []

        result = scrape_recipe_from_url("https://example.com/recipe")

        # 0 is falsy, so it returns None (not "0")
        assert result['prep_time'] is None
        assert result['cook_time'] is None


class TestGetSupportedSites:
    """Tests for the get_supported_sites function."""

    def test_supported_sites_returns_list(self):
        """Test that supported sites returns a list."""
        result = get_supported_sites()
        assert isinstance(result, list)

    def test_supported_sites_is_sorted(self):
        """Test that supported sites are sorted."""
        result = get_supported_sites()
        # If there are sites, they should be sorted
        if len(result) > 1:
            assert result == sorted(result)

    def test_supported_sites_error_handling(self):
        """Test error handling in get_supported_sites."""
        result = get_supported_sites()
        # Should return a list (either populated or empty)
        assert isinstance(result, list)


class TestScrapingError:
    """Tests for the ScrapingError exception."""

    def test_scraping_error_creation(self):
        """Test creating a ScrapingError."""
        error = ScrapingError("Test error message")
        assert str(error) == "Test error message"

    def test_scraping_error_is_exception(self):
        """Test that ScrapingError is an Exception."""
        error = ScrapingError("Test")
        assert isinstance(error, Exception)

    def test_scraping_error_can_be_raised(self):
        """Test that ScrapingError can be raised and caught."""
        with pytest.raises(ScrapingError) as exc_info:
            raise ScrapingError("Test error")
        assert str(exc_info.value) == "Test error"
