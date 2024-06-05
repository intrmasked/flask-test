from crewai import Agent
from langchain_openai import ChatOpenAI  
from crewai_tools import SerperDevTool

class CompanyResearchAgents():
    def __init__(self):
        
        self.llm =  ChatOpenAI(model="gpt-3.5-turbo")
        self.searchInternetTool = SerperDevTool()
    def research_manager(self, companies:list[str], positions:list[str]) -> Agent:
        return Agent(
           role = "COmpany Research Manager",
           goal = f"""
             Generate a list of JSON objects containing the urls for 3 receent blog articles, for
            each company in the list of companies
            Companies: {companies}
            Positions: {positions}
            
            Important:
            - The final list of JSON objects must include all companies in the list of companies and positions. Do not leave anyout.
            - If you cannot find the information for the specific position fill in the information with the word "MISSING"
            - Do not generate fake information. Only return the information you find. Nothing else!
            - Donot stop researching until you find the requested infrmation for all companies and positions
            -Make sure you each researched position for each company contains 3 blog posts and .
            
             """,

            backstory = """As a company reseeach mamange, you are responsible for aggergating all researched information into a list""",

            llm = self.llm,
            tools=[self.searchInternetTool],
            verbose=True,
            allow_delegation= True,
        )
    

       
    def company_research_agent(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal=f""" Look up the specific positions for a given company and find 3 urls for recent blog articles.
            the url and title for each blog article  should be included in the final list of JSON objects.

            """,
            backstory="""As a company research agent, you are responsible for finding the requested information for a specific company and position
            
            Important:
            - Once you have found the information, immediatly stop searching.
            - Only return the requested information. NOTHING ELSE!
            - Make sure you find the persons name who holds the posiiton.
            - Donot generate fake information. Only return the information you find. Nothing else!
            
            """,

            tools=[self.searchInternetTool],
            llm=self.llm,
            verbose=True,
            
            
        )



       