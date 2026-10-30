import requests
import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


load_dotenv()

google_api_key = os.environ['GOOGLE_API_KEY']
model = init_chat_model("google_genai:gemini-3.5-flash", api_key=google_api_key)

@tool
def search_jobs(skill: str, location: str) -> list:
  """Search for jobs requiring a specific skill using JSearch API from RapidAPI."""
  print(f"\nCalling search_jobs tool")
  print(f"Searching jobs for: {skill} in {location}")
  rapidapi_key = os.environ['RAPIDAPI_KEY']
  url = "https://jsearch.p.rapidapi.com/search"
  headers = {
    "x-rapidapi-key": rapidapi_key,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
  }
  querystring = {
    "query": f"{skill} in {location}",
    "page": "1",
    "country": "in",
    "employment_types": "INTERN,FULLTIME",
    "job_requirements": "no_experience,under_3_years_experience"
  }
  response = requests.get(url, headers=headers, params=querystring)
  data = response.json()
  jobs = data.get("data", [])
  print(f"Found {len(jobs)} jobs\n")
  result = []
  for job in jobs:
    result.append({
      "title": job.get("job_title"),
      "company": job.get("employer_name"),
      "location": job.get("job_city"),
      "apply_link": job.get("job_apply_link")
    })
  return result

composio_api_key = os.environ['COMPOSIO_API_KEY']
# Complete the code
client = MultiServerMCPClient(
    {
        "mcp_tavily": {
            "transport": "http",
            "url": "https://backend.composio.dev/api/v1/auth-apps/add",
            "headers" : {"x-api-key" : composio_api_key}

        }
    }
)
system_prompt = """You are a Skill-to-Career Mapping assistant that helps students understand skill demand and find matching job opportunities.

You have access to these tools:
- search tool: Search for industry demand, salary insights, and career trends
- search_jobs: Find actual job listings requiring specific skills

Help the student by researching the skill they ask about and finding relevant opportunities.

Present results in a clean, readable format with clear sections and proper spacing. Include all job details with apply links. Don't use markdown format."""

async def skill_map_agent():
    # Create agent
    mcp_tools = await client.get_tools()
    all_tools = mcp_tools + [search_jobs]

    agent = create_agent(
        model=model,
        tools=all_tools,
        debug=True,
        system_prompt= system_prompt

    )


    # User query
    user_query = "What's the demand for generative AI in the industry and show me related job openings in India"

    # Invoke agent
    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })

    # Print response
    print(response["messages"][-1].content[0]["text"])


# Run function
import asyncio
asyncio.run(skill_map_agent())
