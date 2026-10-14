# GitHub MCP Agent Chat

An interactive command-line chat with a GitHub MCP agent (`Github-mcp-agent`) hosted in Azure AI Foundry. The agent uses the GitHub MCP server to read and manage repositories: files, commits, branches, issues and pull requests.

## Requirements

- Python 3.10+
- An Azure account with access to the Foundry project `fd-github-mcp`
- Azure CLI, signed in (`az login`), or any other credential supported by `DefaultAzureCredential`

## Setup

```powershell
# From the repo root
python -m venv .venv
.venv\Scripts\activate

pip install "azure-ai-projects>=2.1.0" azure-identity
az login
```

## Running

```powershell
cd githubmcp
$env:PYTHONUTF8=1   # show quotes and other characters correctly in the Windows console
python github_mcp_agent.py
```

Type a message at the `You:` prompt. Type `exit` or `quit`, or press Ctrl+C, to stop.

## Approving tool calls

Before each GitHub tool call, the agent pauses and asks for approval. The script shows the call and its arguments:

```
You: Show me calculator_server.py from agenticai-fde/fastmcp-lab
[Tool call] GitHub.get_file_contents({"owner":"agenticai-fde","repo":"fastmcp-lab","path":"calculator_server.py"})
Approve? (y/n): y
Agent: Here is calculator_server.py ...
```

- Answer `y` to run the tool. Anything else declines it.
- Read the arguments before approving calls that write to GitHub, such as creating issues, branches, files or pull requests.
- If a tool call fails (for example, because the agent passed an invalid argument), the script prints `Agent error: ...` and the chat continues. Asking again usually works.

## Example prompts

**Explore a repository (read-only)**
```
List the files in agenticai-fde/fastmcp-lab
Show me calculator_server.py from agenticai-fde/fastmcp-lab
Show the latest commits in agenticai-fde/fastmcp-lab
List branches in agenticai-fde/fastmcp-lab
```

**Review code**
```
Review calculator_server.py in agenticai-fde/fastmcp-lab and suggest improvements
```

**Make changes (writes to GitHub)**
```
Create an issue in agenticai-fde/fastmcp-lab titled "Add power and modulo tools"
Create a branch called feature/power-tool in agenticai-fde/fastmcp-lab
On branch feature/power-tool, add a power(a, b) tool to calculator_server.py
Open a pull request from feature/power-tool to main
```

The whole session uses one conversation, so after the first prompt you can refer to "this repo" instead of repeating the full name.

## Configuration

Edit these values at the top of `github_mcp_agent.py` to point the script at a different project or agent:

| Variable     | Value                                                                  |
|--------------|------------------------------------------------------------------------|
| `endpoint`   | `https://fd-github-mcp.services.ai.azure.com/api/projects/proj-default` |
| `agent_name` | `Github-mcp-agent`                                                     |
