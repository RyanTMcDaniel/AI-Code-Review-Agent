# AI-Code-Review-Agent

# AI Code Review Agent

An autonomous code review tool powered by the Anthropic Claude API. The agent navigates a repository using a multi-step tool-use loop — reading files, searching for patterns, and running tests — then produces a structured markdown report with categorized issues and exact file and line citations.

## Project Structure

- **main.py** — CLI entry point, accepts a repo path and output file argument
- **agent.py** — Anthropic API calls and the agentic tool-use loop
- **tools.py** — Tool implementations (file traversal, file reading, regex search, code execution, test running) and JSON schema definitions for Claude
- **prompts.py** — System prompt that controls the agent's review behavior
- **report.py** — Formats and saves the final review to a markdown file

## Usage

```bash
python3 main.py --repo /path/to/your/project
```

Output is saved to `review_output.md` by default.

## Note

An Anthropic API key is required to run this project. No key is currently loaded, so the agent will not run as-is. To use it, set your key as an environment variable:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com).
