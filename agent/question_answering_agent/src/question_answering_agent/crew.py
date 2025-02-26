from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from question_answering_agent.tools.custom_tool import MyCustomTool

@CrewBase
class QuestionAnsweringAgent():
    """QuestionAnsweringAgent crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def converser(self) -> Agent:
        return Agent(
            config=self.agents_config['converser'],
            verbose=True
        )
    


    @task
    def retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieval_task'],
            tools=[MyCustomTool()],
        )

    @task
    def converse_task(self) -> Task:
        return Task(
            config=self.tasks_config['converse_task'],
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True
        )
