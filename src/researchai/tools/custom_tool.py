import os
import io
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
        content = ""
        for filename in os.listdir(os.getenv("PAPERS_DIR")):
            if filename.endswith(".pdf"):
                file_path = os.path.join(os.getenv("PAPERS_DIR"), filename)
                content += "\n--- Start of the paper ---\n"
                content += self._process_pdf(file_path)
                content += "\n--- End of the paper ---\n"

        return content
        
    def _process_pdf(self, file_path: str) -> str:
        """
        Process a PDF file and extract its text content.
        """
        if PdfReader is None:
            return "PyPDF2 is not installed. Please install it to process PDF files."

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error processing PDF file: {e}"
        
        
