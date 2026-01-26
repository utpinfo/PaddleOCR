from llama_cpp import Llama

model_path = "/Users/yangfengkai/Models"
gguf_path = f"{model_path}/Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"

model = Llama(
    model_path=gguf_path,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=32  # Mac CPU
)

prompt = (
    "<|start_header_id|>user<|end_header_id|>\n"
    "你知道什麼是增值税發票嗎？請用 3 句話以內回答。\n"
    "<|start_header_id|>assistant<|end_header_id|>\n"
)

completion = model(
    prompt,
    max_tokens=120,
    stop=["<|end_of_text|>", "\n\n"],
    echo=False
)

print("content:", completion["choices"][0]["text"])
