#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from researchcrew.crew import ResearchCrew
from researchcrew.llm import summarize, structured_reasoning
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

inputs = {
    'topic': 'AI for Identifying New Drug Targets and Biomarkers',
    'current_year': str(datetime.now().year),
    'papers_to_review': [
        "https://wdoqeiyrvqpmigzydwys.supabase.co/storage/v1/object/sign/research-documents/ff4b3d50-d3ca-4217-8778-1b86e12c6c7f/1762638892777_pharmaceuticals-16-00253.pdf?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iMTEwOTZhMi1hZDI1LTQ1ZTAtYTQxZi1iOGYzYjQyZmI3MjYiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJyZXNlYXJjaC1kb2N1bWVudHMvZmY0YjNkNTAtZDNjYS00MjE3LTg3NzgtMWI4NmUxMmM2YzdmLzE3NjI2Mzg4OTI3NzdfcGhhcm1hY2V1dGljYWxzLTE2LTAwMjUzLnBkZiIsImlhdCI6MTc2MjYzODk3MCwiZXhwIjoxNzYzMjQzNzcwfQ.SgaHWmK0feqmI406btXHVpILBaDKgDdfXmQZiLc8E_4"
    ]
}

def run():
    """
    Run the crew.
    """
    try:
        ResearchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        ResearchCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResearchCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """

    try:
        ResearchCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

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

    inputs_trigger = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": "",
        "papers_to_review": []
    }

    try:
        result = ResearchCrew().crew().kickoff(inputs=inputs_trigger)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
