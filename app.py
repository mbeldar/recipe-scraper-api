from recipe_scraper_api.api import app


if __name__ == '__main__':
    # Keep same default behavior as before
    app.run(debug=True, host='0.0.0.0', port=5000)
