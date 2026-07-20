"""
OPTIONAL BEAUTIFUL SOUP CLASSROOM EXAMPLE

This file teaches the structure of a scraper.

Before scraping any website:
1. Check its robots.txt file.
2. Read its terms of service.
3. Prefer an official API when one exists.
4. Do not collect private student information.
5. Do not send too many requests.
"""

# Import requests to download a permitted public webpage.
import requests

# Import BeautifulSoup to read HTML.
from bs4 import BeautifulSoup


def fetch_page_title(url):
    """Download a webpage and return its title."""

    # Identify the classroom project in the request header.
    headers = {
        "User-Agent": "ScholarScoreStudentProject/1.0"
    }

    # Download the page and stop after ten seconds.
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    # Raise an error for failed status codes.
    response.raise_for_status()

    # Convert the page HTML into a BeautifulSoup object.
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Return the page title when one exists.
    if soup.title:
        return soup.title.get_text(strip=True)

    # Return a fallback message when no title exists.
    return "No title found"


# Only run this message when the file is executed directly.
if __name__ == "__main__":
    print(
        "Add a permitted public webpage URL only after reviewing "
        "its terms of use and robots.txt file."
    )
