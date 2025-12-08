# Logging Configuration

This application uses a comprehensive logging system that captures logs to both console and files.

## Log Files

All log files are stored in the `logs/` directory in the project root.

### File Types:

1. **error.log** - Contains only ERROR and CRITICAL level logs
   - Used for tracking exceptions and critical failures
   - Useful for production monitoring and debugging issues

2. **app.log** - Contains all log levels (DEBUG through CRITICAL)
   - Contains full application activity
   - Useful for tracing complete application flow

## Log Rotation

Both log files are configured with rotating file handlers:
- **Maximum file size**: 10 MB per log file
- **Backup files**: 5 backup copies are retained
- **Encoding**: UTF-8

When a log file reaches 10 MB, it's automatically rotated (backed up) and a new log file is created.

## Log Format

### Console Output:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```
Example:
```
2025-11-28 14:30:15 - src.api - ERROR - Scraping error for https://example.com: Connection timeout
```

### File Output (Error.log):
```
%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s
```
Example:
```
2025-11-28 14:30:15 - src.scraper - ERROR - [scraper.py:42] - Error extracting title from https://example.com
```

## Log Levels

- **DEBUG**: Detailed diagnostic information (e.g., raw ingredients count)
- **INFO**: General informational messages (e.g., request/response logging)
- **WARNING**: Warning messages about unexpected situations (e.g., invalid URLs)
- **ERROR**: Error messages for exceptions (written to error.log)
- **CRITICAL**: Critical errors (written to error.log)

## Suppressed Loggers

The following third-party loggers are suppressed to reduce noise:
- `werkzeug` (Flask development server) - set to WARNING
- `urllib3` - set to WARNING

## Usage Example

When an error occurs during scraping:

```
2025-11-28 14:30:15 - src.scraper - ERROR - [scraper.py:25] - Error extracting title from https://www.example.com/recipe
2025-11-28 14:30:15 - src.api - ERROR - Scraping error for https://www.example.com/recipe: Failed to extract title
```

Both the error and its URL context are logged, making it easy to identify and debug problematic URLs.

## Accessing Logs

To view error logs:
```bash
tail -f logs/error.log
```

To view all logs:
```bash
tail -f logs/app.log
```

To search for errors related to a specific URL:
```bash
grep "example.com" logs/error.log
```
