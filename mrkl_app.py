import os
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain import SQLDatabase, SQLDatabaseChain

os.environ["SERPER_API_KEY"] = "<YOUR_SERPER_API_KEY>"
os.environ["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>"
os.environ["WOLFRAM_ALPHA_APPID"] = "<YOUR_WOLFRAM_ALPHA_APPID>"

llm = OpenAI(temperature=0)
search = GoogleSerperAPIWrapper()
wolfram = WolframAlphaAPIWrapper()
db = SQLDatabase.from_uri("sqlite:///foo_db/Chinook.db")
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    Tool(
        name="Wolfram",
        func=wolfram.run,
        description="Useful for when you need to answer questions about math, science, geography"
    ),
    Tool(
        name="FooBar DB",
        func=db_chain.run,
        description="Useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context"
    )
]

mrkl = initialize_agent(tools, llm, agent="zero-shot-react-description")

query = "Who is the prime minister of the UK?\nWhere was he or she born?\nHow far is their birth place from London?"
response = mrkl.run(query)
print(f"Query: {query}\n\nResponse: {response}")

query = "What is the full name of the artist who\nrecently released an album called 'The Storm Before the Calm'\nand are they in the FooBar database?\nIf so, what albums of theirs are in the FooBar database?"
response = mrkl.run(query)
print(f"Query: {query}\n\nResponse: {response}")
