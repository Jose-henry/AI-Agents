from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PGSearchTool
# Import the custom PGVector tool.
from retrieval_agent.tools.custom_tool import PGVectorTool



# Not suitable for PROD, since not stable yet
""" 
db_uri = os.getenv(
    "YUGABYTE_DB_URL", 
    "postgresql://localhost:5433/yugabyte?sslmode=disable"
)
tool = PGSearchTool(
    db_uri=db_uri,
    table_name='documents',
    config={
        "llm": {
            "provider": "openai",
            "config": {
                "model": "openai/gpt-4o-mini",
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small"
            },
        },
    }
) """

@CrewBase
class RetrievalAgent():
    """RetrievalAgent crew using PGVector for similarity search."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['retriever'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        # Instantiate the PGVectorTool.
        tool = PGVectorTool()
        return Task(
            config=self.tasks_config['retrieval_task'],
            tools=[tool]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
