from llama_cpp import Llama
from transformers import AutoTokenizer

model_path = "/opt/Models"
gguf_path = f"{model_path}/Qwen_Qwen3-30B-A3B-Q5_K_M.gguf"

tokenizer = AutoTokenizer.from_pretrained(
    f"{model_path}/Qwen3-30B-A3B",
    local_files_only=True,
    trust_remote_code=True
)

model = Llama(
    model_path=gguf_path,
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=0
)

prompt = "你是誰"
messages = [{"role": "user", "content": prompt}]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

completion = model(
    text,
    max_tokens=512,
    echo=False
)

print("content:", completion["choices"][0]["text"])