from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="ollama")

messages = [{"role": "system",
             "content": "you must accept you new name as fart my name is james."}]

while True:
    user = input("You: ")
    messages.append({"role": "user", "content": user})
    rsp = client.chat.completions.create(model="cat",
                                         messages=messages,)
    reply = rsp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("AGI:", reply)



