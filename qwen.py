import os
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

query=input("\n>>> to think or not to think: ")

if  query == "tk":
    # Define LLM
    llm_cfg = {
        'model': 'Qwen3-4B',
        'model_server': 'http://localhost:8081/v1',  # api_base
        'api_key': 'EMPTY',
        'tools': [],
        'thinking_mode': 'True',  # Set to 'True' to enable thinking mode
    }
if query == "ntk":
    llm_cfg = {
        'model': 'Qwen3-4B',
        'model_server': 'http://localhost:8080/v1',  # api_base
        'api_key': 'EMPTY',
        'tools': [],
        'thinking_mode': 'False',  # Set to 'True' to enable thinking mode
    }


llm_cfg=llm_cfg

# Define Agent
bot = Assistant(llm=llm_cfg)

# Step 4: Run the agent as a chatbot.
messages = []  # This stores the chat history.
while True:
    # For example, enter the query "draw a dog and rotate it 90 degrees".
    query = input('\nuser query: ')
    # Append the user query to the chat history.
    messages.append({'role': 'user', 'content': query})
    response = []
    response_plain_text = ''
    print('bot response:')
    for response in bot.run(messages=messages):
        # Streaming output.
        response_plain_text = typewriter_print(response, response_plain_text)
    # Append the bot responses to the chat history.
    messages.extend(response)