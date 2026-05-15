import anthropic
import json
from tools import TOOLS, dispatch_tool
from prompts import SYSTEM_PROMPT

client = anthropic.Anthropic()

def run_agent(repo_path):
    messages = [
        {"role": "user", "content": f"Please review the code in this repository: {repo_path}"}
    ]

    MAX_ITERATIONS = 20
    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1

        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == 'end_turn':
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
                
        tool_results = []
        for block in response.content:
            if block.type == 'tool_use':
                result = dispatch_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

        messages.append({"role": "user", "content": tool_results})

    return 'ERROR : Max iterations reached'
