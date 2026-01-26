from llama_cpp import Llama

model_path = "/Users/yangfengkai/Models/"
gguf_path = f"{model_path}/Qwen_Qwen3-30B-A3B-Q5_K_M.gguf"

model = Llama(
    model_path=gguf_path,
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=0  # Mac CPU
)

prompt = "你是誰"

completion = model(
    prompt,
    max_tokens=512,
    echo=False
)

print("content:", completion["choices"][0]["text"])
