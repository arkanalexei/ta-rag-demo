import asyncio
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# ASYNC TEST
#async def main():
#  client = ChatNVIDIA(
#    base_url="http://localhost:8000/v1",
#    model="meta/llama-3.1-8b-instruct",
#  )
#
#  async for chunk in client.astream([{"role": "user", "content": "Write a limerick about the wonders of GPU computing."}]):
#    print(chunk.content, end="|")

#asyncio.run(main())


# SYNC TEST

llm = ChatNVIDIA(
	base_url="http://localhost:8000/v1",
	model="meta/llama-3.1-8b-instruct",
	temperature=0,
	max_tokens=16000
      )

content = "Write a limeric about the wonders of GPU computing"
#content = "Discuss the ethical implications of genetic engineering in humans, covering arguments from both sides. Respond with 10 PAGES worth of texts. Do not be lazy!"
for chunk in llm.stream([{"role":"user","content": content}]):
  print(chunk.content, end="")


