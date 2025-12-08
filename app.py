from src.api import app
from src.logging_config import setup_logging


if __name__ == '__main__':
    # Initialize logging
    setup_logging(app)
    # Keep same default behavior as before
    app.run(debug=True, host='0.0.0.0', port=5000)
