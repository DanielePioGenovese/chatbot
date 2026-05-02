from pydantic_ai import Agent
import asyncio

agent = Agent(
    model="meta-llama/Llama-3.2-3B-Instruct",
    base_url='http://localhost:8000/v1',
    api_key='vllm-is-free'
)

async def main():

    result = await agent.run('What is the capital of italy?')
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())


# outputs = llm.generate("Hello, my name is")

# for output in outputs:
#     prompt = output.prompt
#     generated_text = output.outputs[0].text
#     print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

