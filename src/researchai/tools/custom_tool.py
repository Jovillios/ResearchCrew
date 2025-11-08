import os
import requests
from crewai.tools import BaseTool
from pydantic.v1 import BaseModel, Field

# --- Optional Dependencies ---
try:
    import arxiv
except ImportError:
    arxiv = None

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
# --- ---

class KnowledgeIngestionTool(BaseTool):
    name: str = "Knowledge Ingestion Tool"
    description: str = (
        "Ingests knowledge from various sources (arXiv, URL, PDF). "
        "The input should be a string specifying the source type and the identifier. "
        "Formats: 'arxiv:PAPER_ID', 'url:URL_LINK', 'pdf:FILE_PATH'"
    )

    def _run(self, source_identifier: str) -> str:
        """
        The main execution method for the tool.
        It parses the input string to determine the source type and identifier,
        then calls the appropriate method to fetch and process the content.
        """
        try:
            source_type, identifier = source_identifier.split(':', 1)
            source_type = source_type.strip().lower()
            identifier = identifier.strip()

            if source_type == 'arxiv':
                return self._process_arxiv(identifier)
            elif source_type == 'url':
                return self._process_url(identifier)
            elif source_type == 'pdf':
                return self._process_pdf(identifier)
            else:
                return "Error: Invalid source type. Use 'arxiv', 'url', or 'pdf'."
        except ValueError:
            return "Error: Input string is not in the correct 'source_type:identifier' format."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def _process_arxiv(self, paper_id: str) -> str:
        """
        Fetches and processes the content of a research paper from arXiv.
        """
        if arxiv is None:
            return "Error: 'arxiv' library is not installed. Please run 'pip install arxiv'."
        try:
            search = arxiv.Search(id_list=[paper_id])
            paper = next(search.results())
            
            # Concatenate title, authors, and summary for a comprehensive overview
            content = f"Title: {paper.title}\n"
            content += f"Authors: {', '.join(author.name for author in paper.authors)}\n\n"
            content += f"Summary:\n{paper.summary}"
            
            return content
        except StopIteration:
            return f"Error: No paper found with arXiv ID: {paper_id}"
        except Exception as e:
            return f"Error fetching or processing from arXiv: {e}"

    def _process_url(self, url: str) -> str:
        """
        Fetches and processes the main text content from a URL.
        This is a basic implementation and could be enhanced with more sophisticated
        web scraping libraries like BeautifulSoup for better content extraction.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            # This is a very basic way to get text. For production, use libraries
            # like BeautifulSoup to extract the main article text.
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error fetching from URL: {e}"

    def _process_pdf(self, file_path: str) -> str:
        """
        Extracts and processes text content from a local PDF file.
        """
        if PdfReader is None:
            return "Error: 'PyPDF2' library is not installed. Please run 'pip install PyPDF2'."
        if not os.path.exists(file_path):
            return f"Error: PDF file not found at path: {file_path}"
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text() + "\n"
                return text_content
        except Exception as e:
            return f"Error reading or processing PDF file: {e}"