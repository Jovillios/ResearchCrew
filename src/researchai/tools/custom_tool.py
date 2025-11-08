from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import urllib.request
import mimetypes
from pathlib import Path
try:
    import PyPDF2
except Exception:  # pragma: no cover - optional dependency fallback
    PyPDF2 = None

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."


class DocumentToolInput(BaseModel):
    """Input schema for DocumentTool."""
    path: str = Field(..., description="Local file path relative to repo root or a URL")
    action: str = Field("read", description="Action: 'read' or 'summary'")
    n_lines: int = Field(5, description="Number of lines for quick summary")

class DocumentTool(BaseTool):
    name: str = "document_tool"
    description: str = (
        "Read local knowledge files (e.g., knowledge/*.txt) or URLs and return the full content "
        "or a short summary."
    )
    args_schema: Type[BaseModel] = DocumentToolInput

    def _run(self, path: str, action: str = "read", n_lines: int = 5) -> str:
        """
        Simple, dependency-free document reader:
        - If path starts with http/https, fetch via urllib.
        - Otherwise, open the file relative to the repository root.
        - action='summary' returns the first n_lines non-empty lines as bullets.
        """
        try:
            if path.startswith("http://") or path.startswith("https://"):
                with urllib.request.urlopen(path, timeout=10) as resp:
                    raw = resp.read().decode("utf-8", errors="ignore")
            else:
                # repo root is assumed two levels up from this file
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                abs_path = os.path.abspath(os.path.join(repo_root, path))

                # If the file is a PDF, try to extract text using PyPDF2
                p = Path(abs_path)
                if p.suffix.lower() == ".pdf":
                    if PyPDF2 is None:
                        return "ERROR: PyPDF2 is not installed. Please install PyPDF2 to read PDF files."
                    try:
                        with open(abs_path, "rb") as f:
                            reader = PyPDF2.PdfReader(f)
                            pages = []
                            for pg in reader.pages:
                                try:
                                    pages.append(pg.extract_text() or "")
                                except Exception:
                                    # best-effort extraction
                                    pages.append("")
                        raw = "\n\n".join(pages)
                    except Exception as e:
                        return f"ERROR: failed to read PDF: {e}"
                else:
                    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                        raw = f.read()
        except Exception as e:
            return f"ERROR: {e}"

        if action == "read":
            return raw
        if action == "summary":
            lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
            summary = lines[:max(0, int(n_lines))]
            return "\n".join(f"- {l}" for l in summary)
        # fallback: return a limited preview
        return raw[:2000]