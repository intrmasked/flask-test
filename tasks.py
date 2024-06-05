from crewai import Task,Agent
from textwrap import dedent
from models import PositionInfoList, PositionInfo
from job_manager import append_event



class CompanyResearchTasks():
    def __init__(self, job_id:str):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        print(f"append event: {self.job_id} with output {task_output}")
        append_event(self.job_id, task_output.exported_output)


    def manage_research(self, agent:Agent, companies:list[str], positions:list[str],tasks:list[Task]):
        return Task(
            description=dedent(f"""Based on the list of companies {companies} and positions {positions}, generate a list of JSON objects containing the urls for 3 recent blog articles , for each company in the list of companies."""),
            agent = agent,
            expected_output=dedent(f"""The final list of JSON objects must include all companies in the list of companies and positions. Do not leave any out. If you cannot find the information for the specific position, fill in the information with the word "MISSING". Do not generate fake information. Only return the information you find. Nothing else! Do not stop researching until you find the requested information for all companies and positions. Make sure each researched position for each company contains 3 blog posts."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=PositionInfoList 
        )

    def company_research(self, agent:Agent, company:str, positions:list[str]):
        return Task(
            description = dedent(f"""Research the position {positions} for the company {company}
                for each position, find 3 urls for recent blogs,
                Return this collected information in a JSON object.
                Helpful information:
                - To find blog artcles names and URLs, perform searches on Google such like following:
                  - "{company} [Position HERE] blog articles"
                

                - Important: 
                    - Once you have found the information, immediately stop searching.
                    - Only return the requested information. NOTHING ELSE!
                    - Make sure you find the person's name who holds the position.
                    - Do not generate fake information. Only return the information you find. Nothing else!               
                """),
            agent = agent,
            expected_output=dedent(f"""Return the requested information in a JSON object. The JSON object should contain the name of the person who holds the position, the company name, the position name, 3 blog articles with their names and URLs"""),
            callback=self.append_event_callback,
            async_execution=True,
            output_json=PositionInfo



           
        )
        

