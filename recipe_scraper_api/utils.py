import re
import logging

logger = logging.getLogger(__name__)


def parse_instructions(instructions_raw):
    """Normalize instructions into a list of lines.

    Each newline-delimited line becomes its own list entry. If the
    parser already returned a list, normalize by stripping empty items.
    """
    try:
        if not instructions_raw:
            return []

        if isinstance(instructions_raw, list):
            lines = [l.strip() for l in instructions_raw if l and l.strip()]
        else:
            lines = [ln.strip() for ln in str(instructions_raw).splitlines() if ln.strip()]

        logger.debug("parse_instructions -> %d steps", len(lines))
        return lines
    except Exception as e:
        logger.exception("Error parsing instructions")
        return [str(instructions_raw)] if instructions_raw else []


def clean_unit_string(u):
    """Return a cleaned unit string from various unit representations.

    Accepts Unit objects, strings like "Unit('cup')", or plain strings.
    """
    try:
        if isinstance(u, str):
            s = u
        else:
            s = str(u)

        m = re.search(r"Unit\(['\"]?([^'\")]+)['\"]?\)", s)
        if m:
            logger.debug("_clean_unit_string matched Unit repr -> %s", m.group(1))
            return m.group(1)

        return s.strip('"\' ')
    except Exception:
        return None
