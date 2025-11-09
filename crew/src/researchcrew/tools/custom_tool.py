import os
import io
import requests
from crewai.tools import BaseTool

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


class KnowledgeIngestionTool(BaseTool):
    name: str = "Knowledge Ingestion Tool"
    description: str = (
        "Get knowledge"
    )

    def _run(self) -> str:
        """
        The main execution method for the tool.
        It extracts papers from `PAPERS_DIR` and return it
        """
        PAPERS_DIR = os.getenv("PAPERS_DIR", "knowledge/papers")
        content = ""
        for paper_file in os.listdir(PAPERS_DIR):
            if paper_file.endswith(".pdf"):
                with open(os.path.join(PAPERS_DIR, paper_file), "rb") as f:
                    content += "--- Start of Document ---\n"
                    content += self._parse_pdf_content(f)
                    content += "--- End of Document ---\n"

        return content
        
    def _parse_pdf_content(self, pdf_file_object) -> str:

        if PdfReader is None:
            raise ImportError("PyPDF2 is not installed. Please run 'pip install PyPDF2'.")
        
        reader = PdfReader(pdf_file_object)
        text_content = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content += page_text + "\n"
        return text_content
        

    def _process_url(self, url: str) -> str:
        """
        Fetches content from a URL. Intelligently handles PDF files.
        """

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        # --- KEY CHANGE: DETECT PDF CONTENT ---
        content_type = response.headers.get('Content-Type', '')
        is_pdf = 'application/pdf' in content_type or url.lower().endswith('.pdf')

        if is_pdf:
            # It's a PDF, so we download and parse its content
            pdf_bytes = io.BytesIO(response.content)
            return self._parse_pdf_content(pdf_bytes)
        else:
            # It's a regular webpage, return the text content
            # Ensure we decode properly
            return response.text

    
    
