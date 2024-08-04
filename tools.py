import os
from exa_py import Exa
from crewai_tools import tool
from markdown2 import markdown
from typing import List, Dict, Any
import requests
import pdfminer
import io



class ExaSearchToolset():
    @tool("Search Web")
    def search(query: str)  -> str: #the input this method expects is a query in the form of a string
        """Search for a webpage based on the query.""" #define the objective of the tool
        return ExaSearchToolset._exa().search(f"{query}", use_autoprompt=True, num_results=3)
    
    @tool("Find Similar Webpage")
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return ExaSearchToolset._exa().find_similar(url, num_results=3)

    @tool("Get Contents of Webpage")
    def get_contents(ids: str):
        """Get the contents of a webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """
        ids = eval(ids)

        contents = str(ExaSearchToolset._exa().get_contents(ids))
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)
    
    def tools(): #this is the function used to assign all the tools to our agents
        return [
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar,
            ExaSearchToolset.get_contents
        ]

    def _exa():
        return Exa(api_key=os.environ.get('EXA_API_KEY'))
    


class WritingTools:

    @tool
    def read_file(self, file_path: str) -> str:
        """Read the contents of a file.
        
        Args:
            file_path (str): The path to the file to be read.
            
        Returns:
            str: The content of the file.
        """
        with open(file_path, 'r') as file:
            return file.read()

    @tool
    def write_file(self, file_path: str, content: str):
        """Write content to a file.
        
        Args:
            file_path (str): The path to the file to be written to.
            content (str): The content to write to the file.
        """
        with open(file_path, 'w') as file:
            file.write(content)

    @tool
    def convert_to_markdown(self, content: str) -> str:
        """Convert text content to markdown format.
        
        Args:
            content (str): The text content to convert.
            
        Returns:
            str: The markdown formatted content.
        """
        return markdown(content)


    @tool
    def create_markdown_document(self, title: str, content: str) -> str:
        """Create a markdown document with a given title and content.
        
        Args:
            title (str): The title of the markdown document.
            content (str): The content of the markdown document.
            
        Returns:
            str: The complete markdown document as a string.
        """
        return f"# {title}\n\n{content}"

    @tool
    def url_to_html(self, url: str) -> str:
        """Fetch the HTML content of a webpage from a given URL.
        
        Args:
            url (str): The URL of the webpage to fetch.
            
        Returns:
            str: The HTML content of the webpage.
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    
    
    @tool
    def pdf_to_md(pdf_file: str) -> str:
        """Converts a PDF file to Markdown format.

        Args:
            pdf_file (str): Path to the PDF file.

        Returns:
            str: Markdown formatted text extracted from the PDF.
        """
        output_string = io.StringIO()
        with open(pdf_file, 'rb') as f:
            pdfminer.high_level.extract_text_to_fp(f, output_string)
        return output_string.getvalue()
    
    def tools():
        return [
            WritingTools.read_file,
            WritingTools.write_file,
            WritingTools.convert_to_markdown,
            WritingTools.create_markdown_document,
            WritingTools.url_to_html,
            WritingTools.pdf_to_md
        ]

