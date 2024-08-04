from textwrap import dedent
from crewai import Agent

from tools import WritingTools, ExaSearchToolset
from langchain_community.llms import Ollama
import os
os.environ["OPENAI_API_KEY"] = "NA"


llm = Ollama(
        model = "llama3",
        base_url = "http://localhost:11434")

class ContentGenerationAgents(): 
    def planner_agent(self):
        return Agent(
            role="Planner",
            goal="Construct a thorough and complete plan for the content to be generated based on the user given prompt, utilizing all of the coworker agents.",
        
            backstory=dedent("""\
                As a Planner, you are very attentive to detail and thorough at reading user input, in whatever format given, and understanding
                the input given as well as the user needs inside out. You are able to create a very detailed and thorough plan for your coworkers to 
                follow, and because of your attention to detail, you do not miss any details necessary and serve as the backbone for the jobs to be completed by your coworkers."""),
            tools=[
                ExaSearchToolset.search,
                ExaSearchToolset.find_similar,
                ExaSearchToolset.get_contents,
                WritingTools.read_file,
                WritingTools.write_file,
                WritingTools.convert_to_markdown,
                WritingTools.create_markdown_document,
                WritingTools.url_to_html,
                WritingTools.pdf_to_md
            ],
            verbose=True,
            llm=llm
        )
    
    def researcher_agent(self):
      return Agent(
        role='Research Specialist',
        goal='',
        backstory=dedent("""\
            As an Research Specialist, your mission is to scrape all necessary, relevant, accurate, and credible information you can find on the topic
            given by the user prompt, and that information should come from both the files provided by the user as well ad the information you scrape from the internet.
            Your insights will lay the groundwork for what the writing piece the writer will write about the topic."""),
        tools=[
                ExaSearchToolset.search,
                ExaSearchToolset.find_similar,
                ExaSearchToolset.get_contents,
                WritingTools.read_file,
                WritingTools.write_file,
                WritingTools.convert_to_markdown,
                WritingTools.create_markdown_document,
                WritingTools.url_to_html,
                WritingTools.pdf_to_md
            ],
        verbose=True,
        llm = llm
      )
      
    def writer_agent(self):
      return Agent(
        role='Professional Writer',
        goal='Write an impressive writing piece that is thorough and accurate in its coverage of the information, as well as stylistically accurate to the context provided.',
        backstory=dedent("""\
            As a Professional Writer, you have the incredible ability of taking on the persona and writing style of the writers of the context files provided.
            In this persona and writing style, you are able to craft insightful, informative, thorough, engaging, stylistically and informationally accurate writing pieces."""),
        tools=[
                WritingTools.read_file,
                WritingTools.write_file,
                WritingTools.convert_to_markdown,
                WritingTools.create_markdown_document,
                WritingTools.url_to_html,
                WritingTools.pdf_to_md
            ],
        verbose=True,
        llm = llm
      )
      
    def critic_agent(self): 
      return Agent(
        role='Critic',
        goal='Critically analyze all of the results from all other agents, and revise upon the given results to create a final output of a complete writing piece.',
        backstory=dedent("""\
            As the Critic, you have the ability to critically analyze the results given by the other agent, looking at it from multiple angles to ensure
            quality and completeness, as well as the incredible ability to take on the role of both the researcher and writer agents and revise the given results to match the standard
            of top quality. You ensure that the writing piece matches all user needs, and is written thoroughly and completely, and after your revision, you deliver a final result."""),
        tools=[
                ExaSearchToolset.search,
                ExaSearchToolset.find_similar,
                ExaSearchToolset.get_contents,
                WritingTools.read_file,
                WritingTools.write_file,
                WritingTools.convert_to_markdown,
                WritingTools.create_markdown_document,
                WritingTools.url_to_html,
                WritingTools.pdf_to_md
            ],
        verbose=True,
        llm = llm
      )