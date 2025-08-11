from autogen import ConversableAgent, LLMConfig
from typing import Dict, List, Optional, Any
import os
import requests
from autogen.tools import tool
from ddgs import DDGS
from pydantic import BaseModel, Field
class SearchHit(BaseModel):
    title: str
    snippet: str

@tool
def duckduckgo_search_tool(input_text: str) -> List[SearchHit]:
    with DDGS() as ddgs:
        raw = ddgs.text(input_text, max_results=5)
    return [SearchHit(title=r["title"], snippet=r["body"]) for r in raw]


llm_config = LLMConfig(
    config_list =[
        {'model': 'Qwen3-4B',  # Specify your model
         'base_url': 'http://localhost:8081/v1',
         'api_key' : 'None'  # API base URL
         }
    ]
)




# 3. Create our LLM agent
with llm_config:
    my_agent = ConversableAgent(
        name="van-gogh",
        system_message="You are a poetic AI assistant, respond in rhyme.",
        functions=[duckduckgo_search_tool],  # Register the search tool
    )

# with llm_config:
#     my_agent = ConversableAgent(
#         name="van-gogh-nonthink",
#         system_message="You are a poetic AI assistant, respond in rhyme.",
#     )


# 4. Run the agent with a prompt
response = my_agent.run(
    message="In one sentence, what's the big deal about AI?",
    max_turns=3,
    user_input=True,
    tools=[duckduckgo_search_tool],  # Register the search tool
)

# 5. Iterate through the chat automatically with console output
response.process()

# 6. Print the chat
print(response.messages)