# Recipe Scraper API

A lightweight Flask API that accepts recipe URLs and returns structured recipe data using the `recipe-scrapers` library.

## Features

- 🔗 Accept recipe URLs via POST request
- 📝 Extract structured recipe data (ingredients, instructions, timing, etc.)
- 🌐 Support for 100+ popular recipe websites
- ⚡ Lightweight and fast using Flask
- 📊 RESTful API design
- 🔍 Health check endpoint
- 📋 List supported websites endpoint
- ✅ Comprehensive error handling

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd recipe-scraper-api
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment variables (local)

You can set environment variables locally to configure the app. Example:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_API_KEY="<GET IT FROM_ADMIN>"
```

These differ from the variables used for cloud deployment — see the "Deployment to Google Cloud (GCP)" section below for GCP-specific variables and commands.

## Running the API

### Option 1: Local Development

Start the development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Option 2: Docker

#### Prerequisites

- Docker 20.10 or higher
- Docker Compose 1.29 or higher

#### Quick Start with Docker Compose

The easiest way to run the application is using Docker Compose:

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The API will be available at `http://localhost:5000`

#### View logs:
```bash
docker-compose logs -f recipe-scraper-api
```

#### Stop the container:
```bash
docker-compose down
```

#### Using Docker directly

If you prefer to use Docker without Compose:

```bash
# Build the Docker image
docker build -t recipe-scraper-api .

# Run the container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  --name recipe-scraper-api \
  recipe-scraper-api

# For development with auto-reload, mount the code directory:
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -v $(pwd):/app \
  --name recipe-scraper-api \
  recipe-scraper-api
```

#### Useful Docker commands:

```bash
# View logs
docker logs recipe-scraper-api

# View logs in real-time
docker logs -f recipe-scraper-api

# Stop the container
docker stop recipe-scraper-api

# Remove the container
docker rm recipe-scraper-api

# View running containers
docker ps

# Remove the image
docker rmi recipe-scraper-api
```

#### Environment Variables

You can customize the application behavior using environment variables:

```bash
# Using Docker Compose (edit docker-compose.yml or set via command line)
docker-compose up -e FLASK_ENV=development

# Using Docker run
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=1 \
  recipe-scraper-api
```

Available environment variables:
- `FLASK_ENV`: Set to `development`, `production`, or `testing` (default: `production`)
- `FLASK_DEBUG`: Set to `1` or `0` to enable/disable debug mode (default: `0` in production)

## API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Recipe Scraper API is running"
}
```

---

### 2. Scrape Recipe
**POST** `/scrape`

Extract recipe data from a URL.

**Request Body:**
```json
{
  "url": "https://www.allrecipes.com/recipe/12345/example-recipe/"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "title": "Example Recipe",
    "ingredients": [
      "2 cups flour",
      "1 cup sugar",
      "3 eggs"
    ],
    "instructions": [
      "Mix dry ingredients",
      "Add wet ingredients",
      "Bake at 350°F for 30 minutes"
    ],
    "yields": "8 servings",
    "prep_time": "0:15:00",
    "cook_time": "0:30:00",
    "total_time": "0:45:00",
    "image": "https://example.com/image.jpg",
    "host": "allrecipes.com",
    "description": "A delicious example recipe",
    "ratings": 4.5,
    "cuisine": "American"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "URL is required in the request body",
  "error_type": "invalid_url"
}
```

---

### 3. List Supported Sites
**GET** `/supported-sites`

Get a list of all supported recipe websites.

**Response:**
```json
{
  "success": true,
  "count": 100,
  "sites": [
    "allrecipes.com",
    "bbcgoodfood.com",
    "budgetbytes.com",
    ...
  ]
}
```

---

## Usage Examples

### Using cURL

```bash
# Scrape a recipe
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.allrecipes.com/recipe/12345/example/"}'

# Check health
curl http://localhost:5000/health

# List supported sites
curl http://localhost:5000/supported-sites
```

### Using Python requests

```python
import requests

url = "http://localhost:5000/scrape"
payload = {
    "url": "https://www.allrecipes.com/recipe/12345/example-recipe/"
}

response = requests.post(url, json=payload)
recipe_data = response.json()

if recipe_data['success']:
    print(f"Recipe: {recipe_data['data']['title']}")
    print(f"Ingredients: {recipe_data['data']['ingredients']}")
    print(f"Instructions: {recipe_data['data']['instructions']}")
else:
    print(f"Error: {recipe_data['error']}")
```

### Using JavaScript/Node.js

```javascript
const url = "http://localhost:5000/scrape";
const recipeUrl = "https://www.allrecipes.com/recipe/12345/example-recipe/";

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ url: recipeUrl })
})
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Recipe:', data.data.title);
      console.log('Ingredients:', data.data.ingredients);
      console.log('Instructions:', data.data.instructions);
    } else {
      console.error('Error:', data.error);
    }
  })
  .catch(error => console.error('Error:', error));
```

## Supported Websites

The API supports 100+ recipe websites including:

- AllRecipes
- BBC Good Food
- Budget Bytes
- Tasty
- FoodNetwork
- Serious Eats
- And many more...

Check the `/supported-sites` endpoint for a complete list.

## Error Handling

The API returns appropriate HTTP status codes and error messages:

| Status Code | Error Type | Description |
|---|---|---|
| 200 | Success | Recipe successfully scraped |
| 400 | invalid_url | URL is invalid or missing |
| 400 | scraping_failed | Could not scrape the URL |
| 404 | not_found | Endpoint not found |
| 405 | method_not_allowed | HTTP method not allowed |
| 500 | server_error | Unexpected server error |

## Deployment to Google Cloud (GCP)

This API can be deployed to Google Cloud Run for serverless, scalable hosting.

### Prerequisites

- Google Cloud project with billing enabled
- gcloud CLI installed and authenticated
- Docker installed locally
- Artifact Registry API enabled in your GCP project

### Setup Steps

1. **Set environment variables** for your GCP deployment:

```bash
export PROJECT_ID="your-gcp-project-id"
export SECRET_API_KEY="<GET IT FROM ADMIN>"
export REPOSITORY_NAME="cloud-run-repo"
export SERVICE_NAME="recipe-scraper-api"
export REGION="us-central1"
```

2. **Build and push Docker image** to Artifact Registry:

```bash
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$SERVICE_NAME:version
```

3. **Deploy to Cloud Run**:

```bash
gcloud run deploy $SERVICE_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$SERVICE_NAME:version \
    --region $REGION \
    --port 5000 \
    --platform managed \
    --allow-unauthenticated \
    --update-secrets SECRET_API_KEY=mobile-api-key:latest
```

### Configuration Notes

- The `--allow-unauthenticated` flag allows public access to the API. Remove this flag if you need authentication.
- The `--update-secrets` flag links your Cloud Run service to secrets stored in Google Secret Manager.
- Update the `version` tag to match your deployment version.
- The `REGION` variable defaults to `us-central1`; adjust as needed for your location.

### Accessing Your Deployed API

Once deployed, Cloud Run will provide you with a service URL like:
```
https://recipe-scraper-api-xxxxx.run.app
```

Use this URL to call your API endpoints:
```bash
curl https://recipe-scraper-api-xxxxx.run.app/health
curl -X POST https://recipe-scraper-api-xxxxx.run.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.allrecipes.com/recipe/12345/example/"}'
```

---

## Configuration

Environment variables can be set to customize the API:

```bash
export FLASK_ENV=development  # development, production, or testing
export FLASK_DEBUG=True       # Enable/disable debug mode
```

## Testing

The project includes a comprehensive test suite with 79 tests covering all functions with 87% code coverage.

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html
```

For detailed testing documentation, see `tests/README.md`.

## Project Structure

```
recipe-scraper-api/
├── app.py                     # Main Flask application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # Main documentation (this file)
├── LICENSE                   # License information
├── src/
│   ├── __init__.py           # Package initialization
│   ├── api.py                # Flask endpoints and API logic
│   ├── scraper.py            # Recipe scraping functions
│   ├── ingredients.py        # Ingredient parsing functions
│   └── utils.py              # Utility functions
└── tests/
    ├── __init__.py           # Test package initialization
    ├── conftest.py           # Pytest configuration and fixtures
    ├── README.md             # Testing documentation
    ├── test_api.py           # API endpoint tests
    ├── test_scraper.py       # Scraper logic tests
    ├── test_ingredients.py   # Ingredient parsing tests
    └── test_utils.py         # Utility function tests
```

## Dependencies

- **Flask** - Lightweight web framework
- **recipe-scrapers** - Library for scraping recipe websites
- **Werkzeug** - WSGI utilities for Flask

## Limitations

- Some websites may block or rate-limit requests
- Recipe format varies across websites, so not all fields may be available for every recipe
- Complex JavaScript-heavy websites may not be scraped successfully
- Some websites require specific headers or user-agents

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes. Please respect the terms of service of recipe websites and ensure you have permission to scrape their content.

---

**Enjoy scraping recipes! 🍳**
