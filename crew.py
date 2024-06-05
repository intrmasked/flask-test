from job_manager import append_event
from agents import CompanyResearchAgents
from tasks import CompanyResearchTasks
from crewai import Crew

class CompanyResearchCrew:
    def __init__(self, job_id:str):
        self.job_id = job_id
        self.crew = None
      

    def setup_crew(self, companies: list[str], positions: list[str]):
        agents = CompanyResearchAgents()
        research_manager = agents.research_manager(companies, positions)
        company_research_agent = agents.company_research_agent()

        tasks = CompanyResearchTasks(self.job_id)
        company_research_task = [
            tasks.company_research(company_research_agent,company,positions) for company in companies
        ]

        manage_research = tasks.manage_research(research_manager, companies, positions, company_research_task)


        self.crew = Crew(
            agents=[research_manager, company_research_agent],
            tasks=[*company_research_task, manage_research],
            verbose=True,
        )

    def kickoff(self):
        if not self.crew:
            print("crew not setup")
            return
        
        append_event(self.job_id, "Crew started")
        try:
            print(f"running crew for {self.job_id}")
            results= self.crew.kickoff()
            append_event(self.job_id, "Crew complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"Error: {str(e)}")
            return str(e)
