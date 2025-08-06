from openai import OpenAI
 
client = OpenAI(
    base_url="http://127.0.0.1:8080",  # Local Ollama API
    api_key="ollama"                       # Dummy key
)
 

response = client.chat.completions.create(
    model="gigi",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "what is openai"}
    ]
)
 
print(response.choices[0].message.content)