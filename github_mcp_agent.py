# Before running the sample:
#    pip install "azure-ai-projects>=2.1.0"

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import APIError

endpoint = "https://fd-github-mcp.services.ai.azure.com/api/projects/proj-default"
agent_name = "Github-mcp-agent"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    # Bind the OpenAI client to the existing agent endpoint.
    openai_client = project_client.get_openai_client(agent_name=agent_name)

    # GitHub Copilot preview agents require a conversation for every Responses turn.
    # Reuse one conversation so the agent remembers earlier messages.
    conversation = openai_client.conversations.create()

    print(f"Chatting with {agent_name}. Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_message:
            continue
        if user_message.lower() in ("exit", "quit"):
            break

        try:
            response = openai_client.responses.create(
                conversation=conversation.id,
                input=[{"role": "user", "content": user_message}],
            )

            # The agent pauses with an approval request before each GitHub MCP tool call.
            # Ask the user, send the decision back, and repeat until the agent answers in text.
            while approvals := [item for item in response.output if item.type == "mcp_approval_request"]:
                decisions = []
                for request in approvals:
                    print(f"[Tool call] {request.server_label}.{request.name}({request.arguments})")
                    answer = input("Approve? (y/n): ").strip().lower()
                    decisions.append({
                        "type": "mcp_approval_response",
                        "approval_request_id": request.id,
                        "approve": answer in ("y", "yes"),
                    })
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=decisions,
                )

            print(f"Agent: {response.output_text}\n")
        except APIError as e:
            # A failed tool call (e.g. bad arguments) shouldn't end the chat.
            print(f"Agent error: {e.message}\n")
