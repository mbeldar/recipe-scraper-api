"""Unit tests for src/ingredients.py"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ingredients import (
    normalize_ingredient,
    parse_ingredients,
    _normalize_ingredient_impl
)
from src.utils import clean_unit_string


class TestNormalizeIngredientImpl:
    """Tests for the pure _normalize_ingredient_impl function."""

    def test_dict_like_with_quantity_and_unit(self):
        """Test parsing dict-like with quantity and unit."""
        parsed = {
            'amount': [
                {'quantity': 2.0, 'unit': "Unit('cup')"}
            ],
            'name': [{'text': 'flour'}]
        }
        result = _normalize_ingredient_impl(parsed, "2 cup flour")
        assert result['quantity'] == 2.0
        assert result['unit'] == "cup"
        assert result['name'] == "flour"

    def test_dict_like_with_string_name(self):
        """Test dict-like with string name."""
        parsed = {
            'amount': [{'quantity': 1.0, 'unit': "Unit('egg')"}],
            'name': 'eggs'
        }
        result = _normalize_ingredient_impl(parsed, "1 egg", unit_cleaner=clean_unit_string)
        assert result['quantity'] == 1.0
        assert result['name'] == "eggs"

    def test_dict_like_no_quantity(self):
        """Test dict-like without quantity."""
        parsed = {
            'name': [{'text': 'salt'}]
        }
        result = _normalize_ingredient_impl(parsed, "salt")
        assert result['quantity'] is None
        assert result['name'] == "salt"

    def test_dict_like_no_unit(self):
        """Test dict-like without unit."""
        parsed = {
            'amount': [{'quantity': 1.0}],
            'name': [{'text': 'apple'}]
        }
        result = _normalize_ingredient_impl(parsed, "1 apple")
        assert result['quantity'] == 1.0
        assert result['unit'] is None
        assert result['name'] == "apple"

    def test_object_like_with_attributes(self):
        """Test object-like with attributes."""
        parsed = Mock()
        parsed.name = [Mock(text="sugar")]
        parsed.amount = [Mock(quantity=3.0, unit="Unit('tablespoon')")]
        
        result = _normalize_ingredient_impl(parsed, "3 tbsp sugar", unit_cleaner=clean_unit_string)
        assert result['quantity'] == 3.0
        assert result['name'] == "sugar"

    def test_object_like_string_quantity(self):
        """Test object-like with string quantity (non-convertible)."""
        parsed = Mock()
        parsed.name = [Mock(text="butter")]
        parsed.amount = [Mock(quantity="some", unit="Unit('amount')")]
        
        result = _normalize_ingredient_impl(parsed, "some butter", unit_cleaner=clean_unit_string)
        assert result['quantity'] == "some"
        assert result['name'] == "butter"

    def test_fallback_ingredient_string(self):
        """Test fallback to ingredient string."""
        parsed = {}
        result = _normalize_ingredient_impl(parsed, "2 cups flour")
        assert result['name'] == "2 cups flour"

    def test_dict_with_size_field(self):
        """Test dict with 'size' field instead of 'amount'."""
        parsed = {
            'size': [{'quantity': 1.5, 'unit': "Unit('cup')"}],
            'name': [{'text': 'milk'}]
        }
        result = _normalize_ingredient_impl(parsed, "1.5 cup milk", unit_cleaner=clean_unit_string)
        assert result['quantity'] == 1.5
        assert result['unit'] == "cup"
        assert result['name'] == "milk"

    def test_quantity_as_string_convertible_to_float(self):
        """Test quantity that's a string but convertible to float."""
        parsed = {
            'amount': [{'quantity': "2.5", 'unit': "Unit('cup')"}],
            'name': [{'text': 'water'}]
        }
        result = _normalize_ingredient_impl(parsed, "2.5 cups water", unit_cleaner=clean_unit_string)
        assert result['quantity'] == 2.5
        assert isinstance(result['quantity'], float)


class TestNormalizeIngredient:
    """Tests for the normalize_ingredient function."""

    @patch('src.ingredients.ip_parse_ingredient')
    def test_successful_parsing(self, mock_parse):
        """Test successful ingredient parsing."""
        mock_parse.return_value = {
            'amount': [{'quantity': 2.0, 'unit': "Unit('cup')"}],
            'name': [{'text': 'flour'}]
        }
        result = normalize_ingredient("2 cups flour")
        assert result['quantity'] == 2.0
        assert result['unit'] == "cup"
        assert result['name'] == "flour"

    @patch('src.ingredients.ip_parse_ingredient')
    def test_parsing_error_handling(self, mock_parse):
        """Test error handling during parsing."""
        mock_parse.side_effect = Exception("Parse error")
        result = normalize_ingredient("some ingredient")
        assert result['quantity'] is None
        assert result['unit'] is None
        assert result['name'] == "some ingredient"

    @patch('src.ingredients.ip_parse_ingredient')
    def test_ingredient_with_special_characters(self, mock_parse):
        """Test ingredient with special characters."""
        mock_parse.return_value = {
            'amount': [{'quantity': 1.0}],
            'name': [{'text': 'fresh mozzarella'}]
        }
        result = normalize_ingredient("1 fresh mozzarella")
        assert result['name'] == "fresh mozzarella"


class TestParseIngredients:
    """Tests for the parse_ingredients function."""

    @patch('src.ingredients.normalize_ingredient')
    def test_empty_list(self, mock_normalize):
        """Test with empty ingredient list."""
        result = parse_ingredients([])
        assert result == []

    @patch('src.ingredients.normalize_ingredient')
    def test_single_ingredient(self, mock_normalize):
        """Test with single ingredient."""
        mock_normalize.return_value = {
            'quantity': 2.0,
            'unit': 'cup',
            'name': 'flour'
        }
        result = parse_ingredients(["2 cups flour"])
        assert len(result) == 1
        assert result[0]['quantity'] == 2.0
        assert result[0]['unit'] == 'cup'
        assert result[0]['name'] == 'flour'

    @patch('src.ingredients.normalize_ingredient')
    def test_multiple_ingredients(self, mock_normalize):
        """Test with multiple ingredients."""
        return_values = [
            {'quantity': 2.0, 'unit': 'cup', 'name': 'flour'},
            {'quantity': 1.0, 'unit': None, 'name': 'egg'},
            {'quantity': 0.5, 'unit': 'teaspoon', 'name': 'salt'}
        ]
        mock_normalize.side_effect = return_values
        
        ingredients = ["2 cups flour", "1 egg", "0.5 tsp salt"]
        result = parse_ingredients(ingredients)
        
        assert len(result) == 3
        assert result[0]['quantity'] == 2.0
        assert result[1]['name'] == 'egg'
        assert result[2]['unit'] == 'teaspoon'

    @patch('src.ingredients.normalize_ingredient')
    def test_ingredient_error_handling(self, mock_normalize):
        """Test that errors in ingredient parsing are handled."""
        mock_normalize.side_effect = [
            {'quantity': 1.0, 'unit': 'cup', 'name': 'flour'},
            Exception("Parse error"),  # This will trigger the except block
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'salt'}
        ]
        
        ingredients = ["1 cup flour", "bad ingredient", "0.5 tsp salt"]
        result = parse_ingredients(ingredients)
        
        assert len(result) == 3
        # Second item should have the original ingredient as name with None for quantity/unit
        assert result[1]['name'] == "bad ingredient"

    @patch('src.ingredients.normalize_ingredient')
    def test_quantity_type_conversion(self, mock_normalize):
        """Test that quantities are converted to appropriate types."""
        return_values = [
            {'quantity': 2.0, 'unit': 'cup', 'name': 'flour'},
            {'quantity': 'some', 'unit': 'amount', 'name': 'herbs'},
            {'quantity': None, 'unit': None, 'name': 'salt'}
        ]
        mock_normalize.side_effect = return_values
        
        result = parse_ingredients(["2 cups flour", "some herbs", "salt"])
        
        assert isinstance(result[0]['quantity'], float)
        assert isinstance(result[1]['quantity'], str)
        assert result[2]['quantity'] is None

    @patch('src.ingredients.normalize_ingredient')
    def test_unit_type_conversion(self, mock_normalize):
        """Test that units are converted to strings."""
        mock_normalize.return_value = {
            'quantity': 1.0,
            'unit': 'cup',
            'name': 'milk'
        }
        result = parse_ingredients(["1 cup milk"])
        assert isinstance(result[0]['unit'], str)

    @patch('src.ingredients.normalize_ingredient')
    def test_name_type_conversion(self, mock_normalize):
        """Test that names are converted to strings."""
        mock_normalize.return_value = {
            'quantity': 1,
            'unit': None,
            'name': 'egg'
        }
        result = parse_ingredients(["1 egg"])
        assert isinstance(result[0]['name'], str)
        assert result[0]['name'] == 'egg'
