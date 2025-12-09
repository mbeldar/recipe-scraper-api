import logging
import os
from flask import Flask, request, jsonify
from .scraper import scrape_recipe_from_url, get_supported_sites, ScrapingError
from .logging_config import setup_logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize logging
setup_logging(app)

EXPECTED_KEY = os.environ.get('SECRET_API_KEY')
if not EXPECTED_KEY:
    raise EnvironmentError("SECRET_API_KEY environment variable not set.")

class InvalidURLError(Exception):
    pass


@app.before_request
def log_request_and_auth():
    logger.info(f"{request.method} {request.path}")
    key = request.headers.get('X-Mobile-Api-Key')
    
    if not key or key != EXPECTED_KEY:
        return jsonify({"error": "Unauthorized Access"}), 401


@app.after_request
def log_response(response):
    url = request.args.get('url') or (request.get_json() or {}).get('url', 'N/A') if request.method == 'POST' else 'N/A'
    logger.info(f"Response: {response.status_code} for URL: {url}")
    return response


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Recipe Scraper API is running'}), 200


@app.route('/scrape', methods=['POST'])
def scrape_endpoint():
    try:
        data = request.get_json()
        if not data:
            raise InvalidURLError('Request body must be JSON')

        url = data.get('url', '').strip()
        if not url:
            raise InvalidURLError('URL is required in the request body')
        if not url.startswith(('http://', 'https://')):
            raise InvalidURLError('URL must start with http:// or https://')

        logger.info('Scraping recipe from: %s', url)
        recipe_data = scrape_recipe_from_url(url)

        return jsonify({'success': True, 'data': recipe_data}), 200

    except InvalidURLError as e:
        logger.warning('Invalid URL error for %s: %s', url, str(e))
        return jsonify({'success': False, 'error': str(e), 'error_type': 'invalid_url'}), 400
    except ScrapingError as e:
        logger.error('Scraping error for %s: %s', url, str(e))
        return jsonify({'success': False, 'error': str(e), 'error_type': 'scraping_failed'}), 400
    except Exception as e:
        logger.exception('Unexpected error during scraping for URL: %s', url)
        return jsonify({'success': False, 'error': str(e), 'error_type': 'server_error'}), 500


@app.route('/supported-sites', methods=['GET'])
def supported_sites():
    sites = get_supported_sites()
    return jsonify({'success': True, 'count': len(sites), 'sites': sites}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found', 'error_type': 'not_found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 'Method not allowed', 'error_type': 'method_not_allowed'}), 405
