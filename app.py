"""
Recipe Scraper API

A lightweight Flask API that accepts recipe URLs and returns structured recipe data.
Uses the recipe-scrapers library to extract recipe information.
"""

from flask import Flask, request, jsonify
from recipe_scrapers import scrape_me
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Error handlers
class RecipeScraperError(Exception):
    """Base exception for recipe scraper errors"""
    pass


class InvalidURLError(RecipeScraperError):
    """Raised when URL is invalid or not provided"""
    pass


class ScrapingError(RecipeScraperError):
    """Raised when scraping fails"""
    pass


@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"{request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log response status"""
    logger.info(f"Response: {response.status_code}")
    return response


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Recipe Scraper API is running'
    }), 200


@app.route('/scrape', methods=['POST'])
def scrape_recipe():
    """
    Scrape recipe from provided URL.
    
    Expected JSON body:
    {
        "url": "https://example.com/recipe/..."
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "title": "Recipe Title",
            "ingredients": [...],
            "instructions": [...],
            "yields": "4 servings",
            "prep_time": "15 mins",
            "cook_time": "30 mins",
            "total_time": "45 mins",
            ...
        }
    }
    """
    try:
        # Validate request
        data = request.get_json()
        
        if not data:
            raise InvalidURLError("Request body must be JSON")
        
        url = data.get('url', '').strip()
        
        if not url:
            raise InvalidURLError("URL is required in the request body")
        
        if not url.startswith(('http://', 'https://')):
            raise InvalidURLError("URL must start with http:// or https://")
        
        logger.info(f"Scraping recipe from: {url}")
        
        # Scrape the recipe
        try:
            scraper = scrape_me(url)
        except Exception as e:
            logger.error(f"Failed to scrape URL: {str(e)}")
            raise ScrapingError(
                f"Could not scrape recipe from URL. The website may not be supported "
                f"or the URL may be invalid. Error: {str(e)}"
            )
        
        # Extract recipe data
        recipe_data = {
            'title': scraper.title(),
            'ingredients': scraper.ingredients(),
            'instructions': scraper.instructions(),
            'yields': scraper.yields(),
            'prep_time': str(scraper.prep_time()) if scraper.prep_time() else None,
            'cook_time': str(scraper.cook_time()) if scraper.cook_time() else None,
            'total_time': str(scraper.total_time()) if scraper.total_time() else None,
            'image': scraper.image(),
            'host': scraper.host(),
        }
        
        # Try to get optional fields if available
        try:
            recipe_data['description'] = scraper.description()
        except:
            recipe_data['description'] = None
        
        try:
            recipe_data['ratings'] = scraper.ratings()
        except:
            recipe_data['ratings'] = None
        
        try:
            recipe_data['cuisine'] = scraper.cuisine()
        except:
            recipe_data['cuisine'] = None
        
        logger.info(f"Successfully scraped recipe: {recipe_data.get('title')}")
        
        return jsonify({
            'success': True,
            'data': recipe_data
        }), 200
    
    except InvalidURLError as e:
        logger.warning(f"Invalid URL error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': 'invalid_url'
        }), 400
    
    except ScrapingError as e:
        logger.error(f"Scraping error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': 'scraping_failed'
        }), 400
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred',
            'error_type': 'server_error'
        }), 500


@app.route('/supported-sites', methods=['GET'])
def supported_sites():
    """
    Get list of supported recipe websites.
    Returns a list of supported website hosts.
    """
    try:
        from recipe_scrapers import SCRAPERS
        sites = list(SCRAPERS.keys())
        return jsonify({
            'success': True,
            'count': len(sites),
            'sites': sorted(sites)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching supported sites: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Could not fetch supported sites'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'error_type': 'not_found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'error_type': 'method_not_allowed'
    }), 405


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
