from llama_cpp import Llama

def generate_response(prompt, docs):
    full_prompt = f'Use this context: {docs} to answer to this prompt: {prompt}'

    response = Llama.create_chat_completion(
        messages=[
            {
                "role":"system",
                "content":"You are an expert helpful assistant to answer questions about a company"
            },
            {"role":"user","content":full_prompt}
        ],
        temperature=0.1
    )
    return response["choises"][0]["message"]["content"]


llm = Llama(
    model_path="",
    n_gpu_layers=-1,
    n_ctx=8192,
    verbose=False
)

