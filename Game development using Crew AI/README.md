# AI Game Development Crew (CrewAI + Gemini)

A Google Colab notebook that uses a team of three AI agents built with [CrewAI](https://www.crewai.com/) to turn a one-paragraph game idea into a playable Pygame game, then builds it for the web with [pygbag](https://pygame-web.github.io/) and shares it through a public [ngrok](https://ngrok.com/) link.

## How it works

```
Game idea → Game Designer → Senior Python Developer → QA Engineer / Code Reviewer → main.py → pygbag build → ngrok public URL
```

1. **Creative Game Designer**: expands the user's idea into a Game Design Document (title, genre, objective, controls, entities, mechanics). Scope is kept small: one level, basic mechanics.
2. **Senior Python Game Developer**: writes a complete, standalone Pygame script from the design. It has access to a web search tool ([Serper](https://serper.dev/)) in case it needs to look something up. The main game loop must sit at the top level of the script (not inside a `main()` function), which is required for the web build.
3. **QA Engineer & Code Reviewer**: reviews the code for syntax and runtime errors, checks it against the design, and outputs the final improved code with play instructions.
4. **Crew**: the three agents run in a `Process.sequential` workflow, with each task receiving the earlier tasks' output as context. The LLM for all agents is Gemini (`gemini/gemini-3.5-flash`).
5. **Web deployment**: the final code is pasted into `main.py`, built to WebAssembly with `pygbag`, served locally on port 8000, and exposed publicly through an ngrok tunnel.

## Example game idea

The notebook ships with this prompt:

> **Ceiling Dash**: a gravity-flip endless runner. A robot runs automatically through a sci-fi corridor. Pressing SPACE flips gravity so the robot runs on the ceiling instead of the floor. Spikes and laser barriers appear on both floor and ceiling, coins add to the score, and the game speeds up over time. It ends when the robot hits a hazard.

## Notebook structure

| Section | What it does |
|---|---|
| Cells 1-2 | Install `crewai`, `crewai[google-genai]` |
| Cells 3-8 | Set up the Gemini LLM and define the three agents, plus install `crewai[tools]` and the Serper search tool |
| Cells 9-13 | Define the three tasks and assemble the sequential crew |
| Cell 14 | Set `game_idea` and run `game_crew.kickoff_async(...)` |
| Cell 15 | `%%writefile main.py`: paste the generated game code here |
| Cells 17-21 | **Do not edit.** Install `pygbag` and `pyngrok`, build the game, serve it, and print the public play link |

## Requirements

* A Google account to run the notebook in [Google Colab](https://colab.research.google.com/)
* **Gemini API key** from [Google AI Studio](https://aistudio.google.com/)
* **Serper API key** from [serper.dev](https://serper.dev/) (web search for the developer agent)
* **ngrok authtoken** from the [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

## Setup

1. **Open the notebook** in Google Colab.
2. **Add your secrets** in Colab: `Secrets` (key icon in the left sidebar), then add each of these and enable notebook access:
   * `GEMINI_API_KEY`
   * `SERPER_API_KEY`
   * `NGROK_AUTH_TOKEN`
3. **Run the install and setup cells** (cells 1 to 13) in order.
4. **Set your game idea** in the `game_idea` variable (cell 14) and run it. The crew will print the final code and play instructions.
5. **Paste the code** into the `%%writefile main.py` cell (cell 15) and run it, replacing the placeholder comment.
6. **Register your ngrok token**: in the `!ngrok authtoken ...` cell, replace `'Auth_token'` with your real token (see the note below).
7. **Build and launch**: run the final cell. When the build finishes, click the printed ngrok link to play in your browser.

## Tips for the generated game to work on the web

* Keep the game loop at module level (not inside a function), as the task prompt already requires.
* If you hand-edit the code, pygbag builds usually need the loop to `await asyncio.sleep(0)` each frame. Add this if the build runs but the page stays on a black screen.
* The notebook's final cell expects the game to be controlled with SPACE or a click. Update the printed instructions in that cell if your game uses different controls.

## Known issues and notes

* **Gemini overload (503)**: the saved notebook output shows repeated `503 UNAVAILABLE` errors from the Gemini model, and the crew eventually failed. This is a temporary capacity issue on the API side. If it happens, wait and re-run, or switch the `model=` string in the `LLM(...)` call to another Gemini model.
* **Placeholder token cell**: `!ngrok authtoken 'Auth_token'` is a placeholder. The notebook also loads `NGROK_AUTH_TOKEN` from Colab secrets in an earlier cell, but that variable isn't passed to this command automatically. Replace the placeholder with your token, or use `!ngrok authtoken {ngrok_auth_token}` instead.
* **Never commit real tokens**: if you export the notebook to a public repo, make sure no API key or ngrok token is saved in the cells or outputs.
* **Free ngrok links are temporary**: the public URL stops working when the Colab session ends or the cell is stopped.
* **Hard-coded path**: the web server serves `/content/build/web`, which is the Colab working directory. Adjust it if you run the notebook elsewhere.
* **Misleading comment**: the error message in the last cell refers to "Cell 3" for the ngrok token, but the token is set in a different cell.

## License

Feel free to use, modify, and share.
