import re
import logging

logger = logging.getLogger(__name__)


def _parse_instructions_impl(instructions_raw):
    """Pure function to normalize instructions into a list of lines.

    Each newline-delimited line becomes its own list entry. If the
    parser already returned a list, normalize by stripping empty items.
    
    Args:
        instructions_raw: Either a list or string of instructions.
        
    Returns:
        A list of instruction strings.
        
    Raises:
        TypeError: If input is not list or string-convertible.
    """
    if not instructions_raw:
        return []

    if isinstance(instructions_raw, list):
        lines = [l.strip() for l in instructions_raw if l and l.strip()]
    else:
        lines = [ln.strip() for ln in str(instructions_raw).splitlines() if ln.strip()]

    return lines


def parse_instructions(instructions_raw):
    """Normalize instructions into a list of lines.

    Each newline-delimited line becomes its own list entry. If the
    parser already returned a list, normalize by stripping empty items.
    """
    try:
        lines = _parse_instructions_impl(instructions_raw)
        logger.debug("parse_instructions -> %d steps", len(lines))
        return lines
    except Exception as e:
        logger.exception("Error parsing instructions")
        return [str(instructions_raw)] if instructions_raw else []


def _clean_unit_string_impl(u):
    """Pure function to clean a unit string from various unit representations.

    Accepts Unit objects, strings like "Unit('cup')", or plain strings.
    
    Args:
        u: A unit object or string representation.
        
    Returns:
        A cleaned unit string, or None if unable to clean.
    """
    if isinstance(u, str):
        s = u
    else:
        s = str(u)

    m = re.search(r"Unit\(['\"]?([^'\")]+)['\"]?\)", s)
    if m:
        return m.group(1)

    return s.strip('"\' ')


def clean_unit_string(u):
    """Return a cleaned unit string from various unit representations.

    Accepts Unit objects, strings like "Unit('cup')", or plain strings.
    """
    try:
        result = _clean_unit_string_impl(u)
        if result:
            logger.debug("_clean_unit_string -> %s", result)
        return result
    except Exception:
        logger.exception("Error cleaning unit string")
        return None
