import logging
from ingredient_parser import parse_ingredient as ip_parse_ingredient
from .utils import clean_unit_string

logger = logging.getLogger(__name__)


def _normalize_ingredient_impl(parsed, ingredient_str, unit_cleaner=None):
    """Pure function to normalize parsed ingredient into a dict.

    Handles both dict-like parser returns and object-like returns.
    
    Args:
        parsed: The parsed ingredient data (dict or object).
        ingredient_str: Original ingredient string for fallback.
        unit_cleaner: Optional callable to clean unit strings.
        
    Returns:
        A dict with keys: quantity, unit, name.
    """
    if unit_cleaner is None:
        unit_cleaner = clean_unit_string
    
    quantity = None
    unit = None
    name = ingredient_str

    # dict-like
    if isinstance(parsed, dict):
        amt = parsed.get('amount') or parsed.get('size') or parsed.get('size_amount')
        if isinstance(amt, list) and len(amt) > 0:
            first_amt = amt[0]
        else:
            first_amt = amt if isinstance(amt, dict) else None

        if first_amt:
            q = first_amt.get('quantity') or first_amt.get('value') or first_amt.get('amount')
            if q is not None:
                try:
                    quantity = float(q)
                except Exception:
                    quantity = q
            u = first_amt.get('unit')
            if u:
                unit = unit_cleaner(u)

        nm = parsed.get('name') or parsed.get('ingredient') or parsed.get('parsed')
        if isinstance(nm, list) and len(nm) > 0:
            first = nm[0]
            if isinstance(first, dict):
                name = first.get('text') or ingredient_str
            else:
                name = str(first)
        elif isinstance(nm, str):
            name = nm

        return {'quantity': quantity, 'unit': unit, 'name': name}

    # object-like (ParsedIngredient)
    if hasattr(parsed, 'name') and parsed.name:
        try:
            first_name = parsed.name[0]
            name = getattr(first_name, 'text', str(first_name)) or ingredient_str
        except Exception:
            name = getattr(parsed, 'name', ingredient_str) or ingredient_str

    if hasattr(parsed, 'amount') and parsed.amount:
        try:
            first_amt = parsed.amount[0]
            q = getattr(first_amt, 'quantity', None)
            if q is not None:
                try:
                    quantity = float(q)
                except Exception:
                    quantity = q

            unit_obj = getattr(first_amt, 'unit', None)
            if unit_obj:
                unit = unit_cleaner(unit_obj)
        except Exception:
            q = getattr(parsed, 'quantity', None)
            if q is not None:
                try:
                    quantity = float(q)
                except Exception:
                    quantity = q
            unit = getattr(parsed, 'unit', None)

    if (not name or name == ingredient_str) and hasattr(parsed, 'sentence'):
        name = getattr(parsed, 'sentence') or name

    return {'quantity': quantity, 'unit': unit, 'name': name}


def normalize_ingredient(ingredient_str):
    """Return a normalized dict for a single ingredient string.

    Handles both dict-like parser returns and object-like returns
    (e.g., ParsedIngredient). Returns a dict with keys: quantity, unit, name.
    """
    try:
        parsed = ip_parse_ingredient(ingredient_str)
        logger.debug("ingredient parsed: %r", parsed)

        result = _normalize_ingredient_impl(parsed, ingredient_str)
        logger.debug("_normalize_ingredient -> %r %r %r", 
                     result.get('quantity'), result.get('unit'), result.get('name'))
        return result

    except Exception as e:
        logger.exception("Error normalizing ingredient: %s", str(e))
        return {'quantity': None, 'unit': None, 'name': ingredient_str}


def parse_ingredients(ingredient_list):
    """Parse and sanitize a list of ingredient strings into JSON-safe dicts."""
    parsed_ingredients = []
    for ingredient_str in ingredient_list:
        try:
            normalized = normalize_ingredient(ingredient_str)

            qty = normalized.get('quantity')
            try:
                if qty is not None and not isinstance(qty, (int, float, str)):
                    qty = float(qty)
            except Exception:
                qty = str(qty)

            unit = normalized.get('unit')
            if unit is not None:
                unit = str(unit)

            name = normalized.get('name')
            name = str(name) if name is not None else None

            sanitized = {'quantity': qty, 'unit': unit, 'name': name}
            logger.debug('sanitized ingredient -> %s', sanitized)
            parsed_ingredients.append(sanitized)
        except Exception as e:
            logger.exception("Error parsing ingredient '%s'", ingredient_str)
            parsed_ingredients.append({'quantity': None, 'unit': None, 'name': ingredient_str})

    return parsed_ingredients
