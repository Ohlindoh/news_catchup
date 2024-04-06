import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

class ScraperTool():
  @tool("Scraper Tool")
  def scrape(url: str):
    """Useful tool to scrap a website content, use to learn more about a given url."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content div. Adjust this selector as needed.
        main_content_div = soup.find('div', class_='entry-content')

        text = ""
        if main_content_div:
            # Extract and concatenate text from all <p> tags within the div
            for paragraph in main_content_div.find_all('p'):
                text += paragraph.get_text(separator=' ', strip=True) + '\n\n'

            # Optionally, add headings from <h2> tags
            for heading in main_content_div.find_all('h2'):
                text += heading.get_text() + '\n\n'
        else:
            print("Main content div not found.")
        
        return text.strip()  # Strip to remove any leading/trailing whitespace
    else:
        print("Failed to retrieve the webpage")
        return ""