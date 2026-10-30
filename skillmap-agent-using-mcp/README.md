
# Skill-to-Career Mapping Agent (LangChain + MCP)
 
A LangChain agent that helps students understand how in-demand a skill is and find matching job openings. Given a question like *"What's the demand for generative AI in the industry and show me related job openings in India"*, the agent researches industry demand through an MCP search tool, pulls live job listings from the JSearch API, and returns a clean plain-text summary with apply links.
 
## How it works
 
```
User query → LangChain agent (Gemini) ─┬─→ MCP search tool (via Composio)  → demand, salary & career trends
                                       └─→ search_jobs tool (JSearch API)  → live job listings
                                                   ↓
                              Plain-text report with sections and apply links
```
 
1. **Model**: Google Gemini, loaded through `init_chat_model("google_genai:...")`.
2. **MCP tools**: `MultiServerMCPClient` from `langchain-mcp-adapters` connects to an MCP server over HTTP (authenticated with a Composio API key) and exposes its tools to the agent, used for industry demand, salary insights and career trends.
3. **Custom tool, `search_jobs(skill, location)`**: calls the [JSearch API on RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) and returns the title, company, city and apply link for each job. It is currently restricted to:
   * `country=in` (India)
   * `INTERN` and `FULLTIME` roles
   * `no_experience` and `under_3_years_experience` requirements (entry-level, student friendly)
4. **Agent**: built with `create_agent`, combining the MCP tools and `search_jobs`. A system prompt tells it to act as a Skill-to-Career Mapping assistant and to output readable plain text (no markdown) with all job details and apply links.
5. **Output**: the final message is printed to the console. `debug=True` is on, so you also see the agent's intermediate steps and tool calls.
## Project structure
 
```
skillmap-agent-using-mcp/
├── app.py             # Agent, tools and entry point
├── requirements.txt   # Python dependencies
└── .evalignore        # Files excluded from evaluation (.env, requirements.txt)
```
 
## Requirements
 
* Python 3.10+
* A **Google AI Studio** API key for Gemini
* A **RapidAPI** key subscribed to the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
* A **Composio** API key for the MCP connection
## Setup
 
1. **Install dependencies**
   `requirements.txt` currently lists only `langchain-mcp-adapters`, but `app.py` also imports other packages. Install them all:
```bash
   pip install -r requirements.txt
   pip install langchain langchain-google-genai python-dotenv requests
```
 
2. **Create a `.env` file** in this folder:
```env
   GOOGLE_API_KEY=your_google_ai_studio_key
   RAPIDAPI_KEY=your_rapidapi_key
   COMPOSIO_API_KEY=your_composio_key
```
 
   > ⚠️ Never commit `.env` to a public repo. It is already listed in `.evalignore`; also add it to `.gitignore`.
 
3. **Run the agent**
```bash
   python app.py
```
 
## Customization
 
* **Change the question**: edit `user_query` inside `skill_map_agent()` in `app.py`.
* **Change the search region or experience level**: edit the `querystring` in `search_jobs` (`country`, `employment_types`, `job_requirements`).
* **Swap the model**: change the model string in `init_chat_model(...)`.
* **Change the MCP server**: edit the `MultiServerMCPClient` config (`transport`, `url`, `headers`). You can register multiple servers in the same dictionary.
## Example output (shape)
 
```
Industry Demand: Generative AI
  <demand, salary and trend insights from the search tool>
 
Related Job Openings (India)
  1. <Job title> - <Company> - <City>
     Apply: <link>
  ...
```
 
## Known limitations
 
* The user query is hardcoded; there is no interactive prompt or UI yet.
* `search_jobs` only fetches page 1 of JSearch results and has no error handling for failed API calls or rate limits.
* The MCP server URL and tool name in `app.py` should be checked against your Composio setup before running; the server entry is named `mcp_tavily` and the URL looks like a Composio auth endpoint rather than an MCP server endpoint.
* The final print expects `response["messages"][-1].content[0]["text"]`, which assumes Gemini returns content as a list of blocks.
## License
 
Feel free to use, modify, and share.
