from pdb import run
import streamlit as st
import time
from src.researchcrew.crew import ResearchCrew
import json
import concurrent.futures

st.set_page_config(page_title="ResearchCrew", page_icon="🔬", layout="wide")

def run_research_crew(topic):
    ResearchCrew().crew().kickoff(inputs={
        'topic': topic,
        'current_year': str(time.localtime().tm_year),
    })


def reset_output():
    """Reset the output.json file."""
    output_file = "output.json"
    with open(output_file, "w") as f:
        json.dump([], f)

def render_agent_icon(agent_name):
    """Render an icon for the given agent name."""
    icons = {
        "Senior Research Analyst": "🔬",
        "Critical Reviewer": "🧐",
        "Insight Synthesizer": "📝",
        "Data Visualizer": "📊",
        "Hypothesis Tester": "🧪",
    }
    return icons.get(agent_name, "🤖")

def render_output():
    """
    Render the output of the crew execution.
    [
    {
        "timestamp": "2025-11-08 21:24:58",
        "task_name": "synthesis_task",
        "task": "",
        "agent": " Synthesizer",
        "status": "",
        "output": "optional"
    },
]
    """
    output_file = "output.json"
    try:
        with open(output_file, "r") as f:
            output_data = json.load(f)
    except FileNotFoundError:
        st.error("Output file not found.")
        return
    st.subheader("Crew Execution Output:")
    
    for entry in output_data:
        if entry.get("output") is None or entry.get("status") != "completed":
            continue
        c = st.container()
        col1, col2, col3 = c.columns([1, 5, 1])
        col3.markdown(f"{entry.get('timestamp', '')}")
        col1.markdown(f"{render_agent_icon(entry.get('agent', '').strip())} {entry.get('agent', '')}")

        with col2.expander(f"{entry.get('task', '')}"):
            st.markdown(f"{entry.get('output', '')}")


st.title("ResearchCrew: AI-Powered Research Assistant")

# topic input and file uploader to knowledge/papers
topic = st.text_input("Enter the research topic:", value="AI for Identifying New Drug Targets and Biomarkers")
uploaded_files = st.file_uploader("Upload research documents (PDFs):", accept_multiple_files=True, type=["pdf"])

# save in knowledge base
if topic and uploaded_files:
    for uploaded_file in uploaded_files:
        # Save each uploaded file to the knowledge base
        with open(f"knowledge/papers/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("Files uploaded and saved to knowledge base.")

# launch button
if st.button("Launch ResearchCrew"):
    st.info("ResearchCrew is running... This may take a few minutes.")
    # Simulate ResearchCrew processing
    # here launch ResearchCrew with topic and list of uploaded file paths in parallel render output in live
    reset_output()
    run_research_crew(topic)
    st.success("ResearchCrew has completed execution.")
    render_output()
