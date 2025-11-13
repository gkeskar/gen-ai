from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from typing import List


@CrewBase
class ProtienFoodFinder():
    """ProtienFoodFinder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools
        self.serper_tool = SerperDevTool()
        self.scraper_tool = ScrapeWebsiteTool()

    @agent
    def store_locator(self) -> Agent:
        return Agent(
            config=self.agents_config['store_locator'],
            tools=[self.serper_tool],# type: ignore[index]
            verbose=True
        )

    @agent
    def nutrition_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['nutrition_researcher'],
            tools=[self.serper_tool, self.scraper_tool],  # Added scraper for detailed product pages
            verbose=True
        )

    @agent
    def nutrition_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['nutrition_validator'],
            verbose=True
        )

    @agent
    def recommendation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_specialist'],
            verbose=True
        )    

  
    @task
    def find_stores_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_stores'], 
        )

    @task
    def research_protein_items_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_protein_items'],
        )

    @task
    def validate_products_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_products'],
        )

    @task
    def create_recommendations_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_recommendations'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ProtienFoodFinder crew with memory enabled"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,  # Enable memory to cache results and avoid redundant searches
            cache=True,   # Enable caching for tool calls
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
