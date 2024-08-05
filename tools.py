import requests
from markdownify import MarkdownConverter
from bs4 import BeautifulSoup

class Extraction_Tools:
    def url_to_md(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract the text content of the webpage
        markdown_text = MarkdownConverter().convert_soup(soup)
        return(markdown_text)
        
