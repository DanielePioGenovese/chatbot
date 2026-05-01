from llama_cpp import Llama

def generate_response(prompt, docs, llm):
    full_prompt = f'Use this context: {docs} to answer to this prompt: {prompt}'

    response = llm.create_chat_completion(
        messages=[
            {
                "role":"system",
                "content":"You are an expert helpful assistant to answer questions about a company"
            },
            {"role":"user","content":full_prompt}
        ],
        temperature=0.1
    )
    return response["choices"][0]["message"]["content"]

llm = Llama(
    model_path="models/llama-3.2-3b-instruct-q8_0.gguf",
    n_gpu_layers=-1,
    n_ctx=8192,
    verbose=False
)

print(generate_response("What do you think about Apples?","Are a type of fruit",llm=llm))
