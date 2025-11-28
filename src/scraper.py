import logging
from recipe_scrapers import scrape_me
from .ingredients import parse_ingredients
from .utils import parse_instructions

logger = logging.getLogger(__name__)


class ScrapingError(Exception):
    pass


def scrape_recipe_from_url(url):
    """Scrape a recipe URL and return cleaned structured data."""
    try:
        scraper = scrape_me(url)
        logger.info("Scraper initialized for URL %s", url)
    except Exception as e:
        logger.exception("Failed to initialize scraper for URL %s", url)
        raise ScrapingError(str(e))

    recipe_data = {}

    # title
    try:
        recipe_data['title'] = scraper.title()
    except Exception:
        logger.exception("Error extracting title")
        recipe_data['title'] = None

    # ingredients
    try:
        raw_ingredients = scraper.ingredients() or []
        logger.debug("raw ingredients count: %d", len(raw_ingredients))
        recipe_data['ingredients'] = parse_ingredients(raw_ingredients)
    except Exception:
        logger.exception("Error extracting or parsing ingredients")
        recipe_data['ingredients'] = []

    # instructions
    try:
        raw_instructions = scraper.instructions()
        recipe_data['instructions'] = parse_instructions(raw_instructions)
    except Exception:
        logger.exception("Error extracting or parsing instructions")
        recipe_data['instructions'] = []

    # yields, times, image, description
    try:
        recipe_data['yields'] = scraper.yields()
    except Exception:
        logger.exception("Error extracting yields")
        recipe_data['yields'] = None

    try:
        recipe_data['prep_time'] = str(scraper.prep_time()) if scraper.prep_time() else None
    except Exception:
        logger.exception("Error extracting prep_time")
        recipe_data['prep_time'] = None

    try:
        recipe_data['cook_time'] = str(scraper.cook_time()) if scraper.cook_time() else None
    except Exception:
        logger.exception("Error extracting cook_time")
        recipe_data['cook_time'] = None

    try:
        recipe_data['total_time'] = str(scraper.total_time()) if scraper.total_time() else None
    except Exception:
        logger.exception("Error extracting total_time")
        recipe_data['total_time'] = None

    try:
        recipe_data['image'] = scraper.image()
    except Exception:
        logger.exception("Error extracting image")
        recipe_data['image'] = None

    try:
        recipe_data['description'] = scraper.description()
    except Exception:
        recipe_data['description'] = None

    return recipe_data


def get_supported_sites():
    try:
        from recipe_scrapers import SCRAPERS
        return sorted(list(SCRAPERS.keys()))
    except Exception:
        logger.exception("Error fetching supported sites")
        return []
