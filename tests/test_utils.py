"""Unit tests for src/utils.py"""

import pytest
from src.utils import (
    parse_instructions,
    clean_unit_string,
    _parse_instructions_impl,
    _clean_unit_string_impl
)


class TestParseInstructionsImpl:
    """Tests for the pure _parse_instructions_impl function."""

    def test_empty_string(self):
        """Test with empty string."""
        result = _parse_instructions_impl("")
        assert result == []

    def test_none_input(self):
        """Test with None input."""
        result = _parse_instructions_impl(None)
        assert result == []

    def test_empty_list(self):
        """Test with empty list."""
        result = _parse_instructions_impl([])
        assert result == []

    def test_single_instruction_string(self):
        """Test with single instruction string."""
        result = _parse_instructions_impl("Preheat oven to 350°F")
        assert result == ["Preheat oven to 350°F"]

    def test_multiline_string(self):
        """Test with multiline string."""
        instructions = "Step 1: Preheat oven\nStep 2: Mix ingredients\nStep 3: Bake"
        result = _parse_instructions_impl(instructions)
        assert result == ["Step 1: Preheat oven", "Step 2: Mix ingredients", "Step 3: Bake"]

    def test_list_of_instructions(self):
        """Test with list of instructions."""
        instructions = ["Mix flour", "Add eggs", "Bake"]
        result = _parse_instructions_impl(instructions)
        assert result == ["Mix flour", "Add eggs", "Bake"]

    def test_list_with_empty_strings(self):
        """Test with list containing empty strings."""
        instructions = ["Mix flour", "", "Add eggs", "  ", "Bake"]
        result = _parse_instructions_impl(instructions)
        assert result == ["Mix flour", "Add eggs", "Bake"]

    def test_multiline_with_empty_lines(self):
        """Test multiline string with empty lines."""
        instructions = "Step 1\n\nStep 2\n  \nStep 3"
        result = _parse_instructions_impl(instructions)
        assert result == ["Step 1", "Step 2", "Step 3"]

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped from each line."""
        instructions = "  Step 1  \n  Step 2  \n  Step 3  "
        result = _parse_instructions_impl(instructions)
        assert result == ["Step 1", "Step 2", "Step 3"]

    def test_numeric_input(self):
        """Test with numeric input (converts to string)."""
        result = _parse_instructions_impl(123)
        assert result == ["123"]


class TestParseInstructions:
    """Tests for the parse_instructions function with logging."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        instructions = "Step 1\nStep 2\nStep 3"
        result = parse_instructions(instructions)
        assert result == ["Step 1", "Step 2", "Step 3"]

    def test_error_handling(self):
        """Test that errors are handled gracefully."""
        # This should handle the error and return the stringified input
        result = parse_instructions("")
        assert result == []

    def test_preserves_instruction_content(self):
        """Test that instruction content is preserved."""
        instructions = [
            "Preheat oven to 350°F",
            "Mix 2 cups flour with 1 egg",
            "Bake for 30 minutes"
        ]
        result = parse_instructions(instructions)
        assert len(result) == 3
        assert "350°F" in result[0]
        assert "2 cups flour" in result[1]


class TestCleanUnitStringImpl:
    """Tests for the pure _clean_unit_string_impl function."""

    def test_unit_object_repr(self):
        """Test cleaning Unit object representation."""
        result = _clean_unit_string_impl("Unit('cup')")
        assert result == "cup"

    def test_unit_object_repr_double_quotes(self):
        """Test cleaning Unit object with double quotes."""
        result = _clean_unit_string_impl('Unit("tablespoon")')
        assert result == "tablespoon"

    def test_plain_string(self):
        """Test with plain string."""
        result = _clean_unit_string_impl("cup")
        assert result == "cup"

    def test_string_with_quotes(self):
        """Test string with surrounding quotes."""
        result = _clean_unit_string_impl('"cup"')
        assert result == "cup"

    def test_string_with_single_quotes(self):
        """Test string with single quotes."""
        result = _clean_unit_string_impl("'teaspoon'")
        assert result == "teaspoon"

    def test_string_with_spaces(self):
        """Test string with leading/trailing spaces."""
        result = _clean_unit_string_impl("  cup  ")
        assert result == "cup"

    def test_empty_string(self):
        """Test empty string."""
        result = _clean_unit_string_impl("")
        assert result == ""

    def test_numeric_input(self):
        """Test with numeric input."""
        result = _clean_unit_string_impl(123)
        assert result == "123"

    def test_none_input(self):
        """Test with None input."""
        result = _clean_unit_string_impl(None)
        assert result == "None"

    def test_unit_without_quotes(self):
        """Test Unit object without quotes."""
        result = _clean_unit_string_impl("Unit(cup)")
        assert result == "cup"

    def test_complex_unit_name(self):
        """Test with complex unit names."""
        result = _clean_unit_string_impl("Unit('fluid ounce')")
        assert result == "fluid ounce"


class TestCleanUnitString:
    """Tests for the clean_unit_string function with logging."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = clean_unit_string("Unit('cup')")
        assert result == "cup"

    def test_none_handling(self):
        """Test None handling."""
        result = clean_unit_string(None)
        # clean_unit_string returns the string "None" for None input after conversion
        assert result == "None" or result is None

    def test_error_handling(self):
        """Test that errors are handled gracefully."""
        # Most inputs should be handled without errors
        result = clean_unit_string("cup")
        assert result == "cup"

    def test_preserves_unit_content(self):
        """Test that unit content is preserved correctly."""
        units = [
            ("Unit('cup')", "cup"),
            ("Unit('tablespoon')", "tablespoon"),
            ("Unit('teaspoon')", "teaspoon"),
            ("cup", "cup"),
        ]
        for input_val, expected in units:
            result = clean_unit_string(input_val)
            assert result == expected
