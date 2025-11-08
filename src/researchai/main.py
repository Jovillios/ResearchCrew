#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from researchai.crew import Researchai
from researchai.tools.custom_tool import DocumentTool
from researchai.llm import summarize, structured_reasoning
from researchai.conversation_graph import ConversationGraph
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }

    try:
        Researchai().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def demo_pdf():
    """Small demo: load PDF (path via env PDF_PATH), summarize, and save conversation graph.

    Useful for manual testing: set PDF_PATH to a local file path relative to repo root.
    """
    pdf_path = os.getenv("PDF_PATH")
    if not pdf_path:
        raise Exception("Set PDF_PATH env var to a local PDF file path relative to repo root to run demo_pdf.")

    # Use DocumentTool to read the PDF
    tool = DocumentTool()
    raw = tool._run(pdf_path, action="read")
    if raw.startswith("ERROR:"):
        raise Exception(f"Failed to load PDF: {raw}")

    # Summarize using our llm helper (may be a lightweight fallback)
    text_summary = summarize(raw)
    reasoning = structured_reasoning(raw)

    # Record into a conversation graph
    graph = ConversationGraph()
    graph.add_exchange(from_agent="ingestor", to_agent="llm", message=f"ingest:{pdf_path}")
    graph.add_exchange(from_agent="llm", to_agent="synthesizer", message="summary", response=text_summary)
    graph.add_exchange(from_agent="llm", to_agent="synthesizer", message="structured_reasoning", response=reasoning)

    out = os.path.abspath("conversation_graph.json")
    graph.save(out)
    return {"summary": text_summary, "reasoning": reasoning, "graph_file": out}


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Researchai().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Researchai().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        Researchai().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = Researchai().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
