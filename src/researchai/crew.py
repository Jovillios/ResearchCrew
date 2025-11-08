from gc import callbacks
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os

# Import your custom tool.
from .tools.custom_tool import KnowledgeIngestionTool

@CrewBase
class ResearchCrew:
    """A crew of AI agents designed to conduct research, review findings,
    and synthesize insights into a final report."""
    
    # The agents.yaml file is loaded into self.agents_config
    # The tasks.yaml file is loaded into self.tasks_config
    
    # --- AGENT DEFINITIONS ---
    # The names of these methods MUST match the keys in your agents.yaml file.
    
    @agent
    def researcher(self) -> Agent:
        """Agent responsible for ingesting and summarizing research material."""
        return Agent(
            config=self.agents_config['researcher'],
            tools=[KnowledgeIngestionTool()], # Assign the custom tool
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        """Agent responsible for critically reviewing the summarized research."""
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True
        )

    @agent
    def synthesizer(self) -> Agent:
        """Agent responsible for synthesizing insights into a report."""
        return Agent(
            config=self.agents_config['synthesizer'],
            verbose=True
        )

    @agent
    def data_visualizer(self) -> Agent:
        """Optional agent responsible for creating visualizations from
        the synthesized insights. This method must exist because
        `visualization_task` in `tasks.yaml` refers to the
        'data_visualizer' agent.
        """
        return Agent(
            config=self.agents_config['data_visualizer'],
            verbose=True
        )
    
    @agent
    def hypothesis_tester(self) -> Agent:
        """Optional agent responsible for testing hypotheses based
        on the research findings. This method must exist because
        `hypothesis_testing_task` in `tasks.yaml` refers to the
        'hypothesis_tester' agent.
        """
        return Agent(
            config=self.agents_config['hypothesis_tester'],
            verbose=True
        )
    
    @agent
    def historian(self) -> Agent:
        """Optional agent responsible for providing historical context
        to the research topic. This method must exist because
        `historical_context_task` in `tasks.yaml` refers to the
        'historian' agent.
        """
        return Agent(
            config=self.agents_config['historian'],
            verbose=True
        )

    # --- TASK DEFINITIONS ---
    # The names of these methods MUST match the keys in your tasks.yaml file.

    @task
    def research_task(self) -> Task:
        """Task for the researcher to ingest and analyze the source material."""
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher() # Assign the task to the researcher agent
        )

    @task
    def review_task(self) -> Task:
        """Task for the reviewer to critique the initial research summary."""
        return Task(
            config=self.tasks_config['review_task'],
            agent=self.reviewer(),
            # The context is automatically managed by CrewAI based on the
            # 'context' key in your tasks.yaml file.
            context=[self.research_task()]
        )

    @task
    def synthesis_task(self) -> Task:
        """Task for the synthesizer to create the final insight report."""
        return Task(
            config=self.tasks_config['synthesis_task'],
            agent=self.synthesizer(),
            context=[self.research_task(), self.review_task()],
            # Define an output file for the final report.
            output_file='final_insight_report.md'
        )

    # --- CREW DEFINITION ---
    
    @crew
    def crew(self) -> Crew:
        """Creates and configures the research crew."""
        return Crew(
            # The agents and tasks are automatically collected from the
            # decorated methods.
            agents=self.agents,
            tasks=self.tasks,
            tracing=True,
            output_log_file=os.getenv("OUTPUT_FILE"),
        )
    
    