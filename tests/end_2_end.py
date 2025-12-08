import requests
import json
import os

# --- Configuration ---
SCRAPE_URL = "http://localhost:5000/scrape"
FILE_PATH = "URLs.txt"
LOG_FILE_PATH = "non_200_responses.log"

def log_non_200_response(url, status_code, response_text):
    """
    Logs the details of a response that is not HTTP status 200.
    """
    try:
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"--- Non-200 Response --- \n")
            log_file.write(f"URL: {url}\n")
            log_file.write(f"Status Code: {status_code}\n")
            log_file.write(f"Response Body (partial): {response_text[:500]}{'...' if len(response_text) > 500 else ''}\n")
            log_file.write("-" * 30 + "\n")
        print(f"Logged error for {url} (Status: {status_code})")
    except IOError as e:
        print(f"Error writing to log file {LOG_FILE_PATH}: {e}")

def run_post_test():
    """
    Hits the SCRAPE_URL with a specific POST request body.
    """
    print(f"## 🚀 Running POST Request Test on {SCRAPE_URL}")
    payload = {
        "url": "https://www.allrecipes.com/recipe/20144/banana-banana-bread/"
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(SCRAPE_URL, data=json.dumps(payload), headers=headers)
        print(f"POST Request to {SCRAPE_URL} finished.")
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            log_non_200_response(SCRAPE_URL, response.status_code, response.text)
        else:
            print("Response is 200 OK.")
            # Optional: Print a snippet of the successful response
            # print(f"Response Body Snippet: {response.text[:100]}...")

    except requests.exceptions.ConnectionError:
        print(f"❌ **Connection Error**: Could not connect to {SCRAPE_URL}. Is the server running?")
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred during the request: {e}")

def run_file_urls_test():
    """
    Reads URLs from a file and hits each one with a GET request.
    """
    print(f"\n## 📄 Running File URLs Test from {FILE_PATH}")
    
    if not os.path.exists(FILE_PATH):
        print(f"⚠️ **Warning**: File '{FILE_PATH}' not found. Skipping URL file test.")
        print("Please create this file and populate it with URLs (one per line).")
        return

    try:
        with open(FILE_PATH, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"❌ Error reading file {FILE_PATH}: {e}")
        return

    if not urls:
        print(f"ℹ️ File '{FILE_PATH}' is empty. Skipping URL file test.")
        return

    print(f"Found **{len(urls)}** URLs to test.")
    
    for url in urls:
        print(f"-> Testing URL: {url}")
        try:
            payload = {
                "url": url
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(SCRAPE_URL, data=json.dumps(payload), headers=headers)
            print(f"POST Request to {SCRAPE_URL} finished.")
            
            if response.status_code != 200:
                log_non_200_response(url, response.status_code, response.text)
            else:
                print(f"   Status: 200 OK")

        except requests.exceptions.ConnectionError:
            log_non_200_response(url, "Connection Error", "Could not resolve hostname or connect to server.")
        except requests.exceptions.Timeout:
            log_non_200_response(url, "Timeout Error", "Request timed out after 10 seconds.")
        except requests.exceptions.RequestException as e:
            log_non_200_response(url, "Request Exception", str(e))

def main():
    """
    Main function to execute all tests.
    """
    # Clear the log file from previous runs
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
    print(f"Test run started. Logs will be written to **{LOG_FILE_PATH}**.")
    print("-" * 50)
    
    run_post_test()

    print("-" * 50)
    
    run_file_urls_test()

    print("-" * 50)
    print("Test run finished.")
    if os.path.exists(LOG_FILE_PATH):
        print(f"Review **{LOG_FILE_PATH}** for any non-200 responses.")
    else:
        print("No non-200 responses were logged.")

if __name__ == "__main__":
    main()