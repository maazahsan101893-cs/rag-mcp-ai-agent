from fastmcp import FastMCP 
from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
load_dotenv()
mcp = FastMCP("RAG")
web_search_tool = DuckDuckGoSearchRun()
Loader = PyPDFLoader("documents/curriculum.pdf")
document = Loader.load()
TextSplitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
chunks = TextSplitter.split_documents(document)
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
model_embed = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
storage = Chroma.from_documents(documents = chunks , embedding = model_embed)
retriever = storage.as_retriever()
def formatdocs(docs) :
  return "\n\n".join(doc.page_content for doc in docs)
prompt = ChatPromptTemplate.from_messages([("system","You are a helpful assistant. Answer using only the provided context. If the answer is not in the context, say you don't know."),
                                           ("human","Context : {context} Question : {question}")])
general_prompt = ChatPromptTemplate.from_messages([("system","You are a helpful AI assistant. Answer the user's question."),("human","Question : {question}")])
web_prompt = ChatPromptTemplate.from_messages([("system","You are a helpful assistant. Answer the question using the web search results provided. If the results don't contain a clear answer, say so."),
 ("human","Web results : {context} Question : {question}")])
parser = StrOutputParser()
rag_chain= {"context": RunnableLambda(lambda x: x["question"]) | retriever | formatdocs , "question": RunnableLambda(lambda x: x["question"])} | prompt |model | parser
general_chain = {"question": RunnableLambda(lambda x: x["question"])} | general_prompt | model | parser
web_search_chain ={"context": RunnableLambda(lambda x: x["question"]) | web_search_tool , "question": RunnableLambda(lambda x: x["question"])} | web_prompt | model | parser
@mcp.tool("search_rag")
def search_rag( question : str ) :
  """IMPORTANT: Use this tool whenever the user's question is about the HEC Generative AI Training Program PDF. Use this for questions about: - What the course is about - Course curriculum - Week 1 - Topics covered - Course structure - Learning objectives - Generative AI training program content Do NOT answer these questions from your own knowledge. ALWAYS call this tool for questions about the HEC course PDF. Args: question: The user's question about the HEC course."""
  return rag_chain.invoke({"question" : question})
@mcp.tool("search_general")
def search_general(question : str) :
  """Use this tool ONLY when the question is NOT about the HEC Generative AI Training Program PDF. Examples: - What is Python? - What is recursion? - Explain object-oriented programming. - What is an API? Do NOT use this tool for questions about the HEC course PDF. Args: question: A general knowledge question."""
  return general_chain.invoke({"question" : question})
@mcp.tool("search_web")
def search_web(question : str) :
  """Use this tool when the user needs CURRENT information from the internet. Examples: - Today's news - Current prices - Recent events - Latest AI developments - Current weather - Information that may have changed recently Do NOT use this tool for questions about the HEC course PDF unless the user explicitly asks for current web information. Args: question: A question requiring current web information."""
  return web_search_chain.invoke({"question": question})

if __name__ == "__main__":
    mcp.run()