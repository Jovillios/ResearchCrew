from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from researchai.tools.custom_tool import DocumentTool

@CrewBase
class Researchai():
    """Researchai crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agents aligned with src/researchai/config/agents.yaml
    @agent
    def knowledge_ingestor(self) -> Agent:
        return Agent(
            config=self.agents_config['knowledge_ingestor'], # type: ignore[index]
            tools=[DocumentTool()],
            verbose=True
        )

    @agent
    def research_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['research_reviewer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def insight_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['insight_synthesizer'], # type: ignore[index]
            verbose=True
        )

    # Tasks aligned with src/researchai/config/tasks.yaml
    @task
    def ingestion_task(self) -> Task:
        return Task(
            config=self.tasks_config['ingestion_task'], # type: ignore[index]
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'], # type: ignore[index]
        )

    @task
    def synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesis_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Researchai crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
