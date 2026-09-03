from fastapi import FastAPI
import os
from pydantic import BaseModel
from langchain.agents import create_agent 
from fastmcp import FastMCP
from langchain_google_genai import ChatGoogleGenerativeAI 
import asyncio 
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
class QueryRequest(BaseModel) :
  query : str 
async def main(request : QueryRequest) :
    client = MultiServerMCPClient(
        {
            "RAG" : {
                "transport" : "stdio",
                "command" : "python" ,
                "args" : ["rag_server.py"],
                "env" : dict(os.environ),
            }
        }
    )
    tools = await client.get_tools()
    print("Tool Names :")
    for tool in tools :
        print(tool.name)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite" , temperature=0)
    agent = create_agent( llm , tools ,system_prompt="""You are an intelligent routing agent.

You have exactly three tools:

1. search_rag
   Use this ONLY for questions about the HEC Generative AI Training Program PDF.
   Examples:
   - What is Week 1 about?
   - What topics are covered?
   - What are the learning objectives?
   - Explain the HEC Generative AI curriculum.

2. search_general
   Use this for stable general-knowledge questions that do NOT require the internet.
   Examples:
   - What is Python?
   - What is recursion?
   - What is OOP?
   - What is an API?
   - What is the capital of Japan?

3. search_web
   Use this whenever the answer depends on information from the internet
   or information that may change over time.

   ALWAYS use search_web for:
   - current information
   - latest information
   - recent news
   - current events
   - today's information
   - prices
   - weather
   - current software/library information
   - recommendations involving websites, YouTube, GitHub, courses,
     products, tools, or online resources
   - "best" or "top" recommendations when external/current information
     would improve the answer

IMPORTANT ROUTING RULES:

- HEC PDF question -> search_rag
- Current/internet-dependent question -> search_web
- Stable general knowledge -> search_general

Never answer an HEC PDF question directly from your own knowledge.
Never use search_general when the user explicitly asks for current or
internet-based information.

After receiving the tool result, answer the user using that result.
IMPORTANT:

For every user question:

1. Select exactly ONE tool.
2. Call that tool exactly ONE time.
3. Do NOT call the same tool again.
4. Do NOT call another tool after receiving the result.
5. After receiving the tool result, immediately give the final answer.
6. Do not generate additional questions yourself.
7. Do not perform multi-step research unless the user explicitly asks for it.""")
    response = await agent.ainvoke(
        {
            "messages" : [
                {
                    "role" : "user" ,
                    "content" : request.query 
                }
            ]
        }
    )
    for message in response["messages"]:
        print("\n--- MESSAGE ---")
        print("Type:", type(message).__name__)
        print("Content:", message.content)

        if hasattr(message, "tool_calls"):
            print("Tool Calls:", message.tool_calls)
    return response["messages"][-1].content
@app.post("/query")
async def query_answer(request : QueryRequest) :
    answer = await (main(request))
    return {"answer" : answer }