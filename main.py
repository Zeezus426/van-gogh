#!/usr/bin/env python3
from llama_cpp import Llama
import os, sys

MODEL_PATH = (
    "/Users/zacharyaldin/Library/Caches/llama.cpp/"
    "unsloth_Qwen3-4B-Thinking-2507-GGUF_Qwen3-4B-Thinking-2507-Q4_K_M.gguf"
)

print("🚀  Loading model …")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,               # same as your CLI -c 2048
    n_batch=512,              # Metal likes 512-1024
    n_gpu_layers=35,          # leave last layer on CPU to stay under 12 GB 
    chat_format="qwen",    # activates the chat template you saw
    yarn_attn_factor=4.0,


)

# Stateful chat loop (identical to ./main -ins)
messages = []
while True:
    try:
        user = input("\n>>> ")
    except (EOFError, KeyboardInterrupt):
        print("\nBye 👋")
        break

    messages.append({"role": "user", "content": user})

    print("\n--- assistant ---")
    out = ""
    for chunk in llm.create_chat_completion(
        messages,
        stream=True,
        max_tokens=4090,
        temperature=0.8,
        top_p=0.95,
        tools=None,
    ):
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            print(delta["content"], end="", flush=True)
            out += delta["content"]
    messages.append({"role": "assistant", "content": out})