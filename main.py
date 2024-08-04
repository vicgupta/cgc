# import argparse
from dotenv import load_dotenv
from crewai import Crew
from tasks import ContentGenerationTasks
from agents import ContentGenerationAgents

def main():

    load_dotenv()


    print("## Welcome to the Content Generation Crew")
    print('---------------------------------')

    content_prompt = input("Provide a detailed prompt of what writing piece you would like to be created today, including type of writing piece (blogpost, LinkedIn post, white paper, etc.), as well as any word counts and other limitations/things to consider. \n")
    context_files = input("Provide any files that you would like to provide for the writing context of this piece, such as any files that have a similar writing style, tone, and structure for how you would like your piece to be written. This can be urls (if multiple, separate by space), pdf files, html files, etc. \n")
    context_purpose = input("Is there anything specific you would like us to consider from the context files? (Such as the writing style, the specific page format, or even specfic posts from a broader page)\n")
    content_files = input("Provide any existing files from which content you would like to be included in your new writing piece (such as case studies, white papers, etc.)")

    '''
    parser = argparse.ArgumentParser(description='Process some files and URLs.')
    parser.add_argument('--url', type=str, help='URL to read content from')
    parser.add_argument('--pdf', type=str, help='PDF file path to read content from')
    args = parser.parse_args()

    if args.url:
        try:
            url_content = url_to_html(args.url)
            print(f'Content from URL:\n{url_content}')
        except Exception as e:
            print(f'Failed to read URL: {e}')

    if args.pdf:
        try:
            pdf_content = pdf_to_md(args.pdf)
            print(f'Content from PDF:\n{pdf_content}')
        except Exception as e:
            print(f'Failed to read PDF: {e}')
    '''
    
    
    tasks = ContentGenerationTasks()
    agents = ContentGenerationAgents()

    planner_agent = agents.planner_agent()
    researcher_agent = agents.researcher_agent()
    writer_agent = agents.writer_agent()
    critic_agent = agents.critic_agent()

    planner_task = tasks.planner_task(planner_agent, content_prompt, context_files, context_purpose, content_files)
    researcher_task = tasks.research_task(researcher_agent, context_files)
    writer_task = tasks.writer_task(writer_agent)
    critic_task = tasks.critic_task(critic_agent, content_prompt, context_files, context_purpose, content_files)

    researcher_task.context = [planner_task]
    writer_task.context = [planner_task, researcher_task]
    critic_task.context = [planner_task, writer_task, critic_task]

    
    content_generation_crew = Crew(

        agent = [
            planner_agent,
            researcher_agent,
            writer_agent,
            critic_agent
        ],
        tasks = [
            planner_task,
            researcher_task,
            writer_task,
            critic_task
        ]
    )

    result = content_generation_crew.kickoff()

    print(result)


if __name__ == "__main__":
    main()