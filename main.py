from os import getenv
from agno.agent import Agent, RunResponse
from agno.models.openai.like import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools

query=input("\n>>> to think or not to think: ")

if  query == "tk":
    van_gogh_thinking = Agent(
        tools=[DuckDuckGoTools()], 
        show_tool_calls=True, 
        reasoning=True,
        model=OpenAILike(
            id="qwen3-4b",
            api_key='none',
            base_url="http://localhost:8081/v1",

        )
    )
if query == "ntk":
    van_gogh_nonthinking = Agent(
        tools=[DuckDuckGoTools()], 
        show_tool_calls=True,
        model=OpenAILike(
            id="qwen3-4b",
            api_key='none',
            base_url="http://localhost:8080/v1",

        ),
    )

agent = van_gogh_nonthinking or van_gogh_thinking
user_query = input("Enter your query: ")
# Print the response in the terminal
agent.print_response(message=user_query, 
                     stream=True, 
                     markdown=True,
                     show_message=True,)

