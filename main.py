import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from tools.scraper import ScraperTool

os.environ.get("OPENAI_API_KEY")


scrape_tool = ScraperTool().scrape

class SummaryCrew:
  def __init__(self, urls):
    self.urls = urls

  def run(self):    
    scraper = Agent(
      role='Scraper of websites',
      goal='Ask the user for a list of URLs, then use the WebsiteSearchTool to then scrape the content, and provide the full content to the writer agent so it can then be summarized',
      backstory=
        """Driven by curiosity, you're at the forefront of
        innovation, eager to explore and share knowledge that could change
        the world. You are an expert at taking URLs and taking just the text-based content from them""",
      verbose=True,
      tools=[scrape_tool],
      allow_delegation=False
  )

    writer = Agent(
      role='Cybersecurity Content Summarizer and Writer',
      goal='Craft compelling short-form tech stories about cybersecurity news based on news passed to you by the scraper agent',
      backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
      ),
      verbose=True,
      memory=True,
      allow_delegation=True
    )

    # Research task - scraping the content of the website
    research_task = Task(
      description= f"""
        Take a list of websites and read and scrape the content and
        pass it to the writer agent. Here are the URLs from the user 
        that you need to scrape: {self.urls}""",
      expected_output='The full text content of the blog post',
      agent=scraper,
    )

    # Writing task with language model configuration
    write_task = Task(
      description=""""
        Using the text provided by the scraper agent, develop a short 
        but engaging summary of the article provided to you""",
      expected_output='A summary of the blog post',
      agent=writer,
    )

    SummaryCrew = Crew(
      agents=[scraper, writer],
      tasks=[research_task, write_task],
      process=Process.sequential,
      verbose=2,

    )

    SummaryCrew.kickoff()

if __name__ == "__main__":
  print("## Welcome to the blog summarizer")
  print('-------------------------------')
  urls = input("What is the URL you want to summarize?")
  
  summary_crew = SummaryCrew(urls)
  result = summary_crew.run()
  print("\n\n########################")
  print("## Here is the Result")
  print("########################\n")
  print(result)
  