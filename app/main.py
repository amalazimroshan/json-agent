from fastapi import FastAPI
import os
import json
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate

app = FastAPI()

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
uri = os.getenv("MONGODB_API_KEY")

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.sample_mflix
llm = ChatGroq(model="llama3-8b-8192")

@tool
def get_schema()->dict:
    """Retrieve the schema of the collection by analyzing the first document."""
    collection_name = 'movies'
    print(f'GET SCHEMA FOR COLLECTION: {collection_name}')
    collection = db[collection_name]
    sample_document = collection.find_one()  # Get a single document to infer the schema
    if sample_document is None:
        print('No documents found in collection')
        return {}

    schema = {key: type(value).__name__ for key, value in sample_document.items()}
    print(f'Schema for {collection_name}: {schema}')
    return schema

@tool
def fetch_query_results(query:dict) -> list[dict]:
    """Execute a query on the collection and return the results as a list of documents."""
    print(f'FETCH QUERY RESULTS FROM COLLECTION: Moview WITH QUERY: {query}')
    collection = db['movies']
    results = list(collection.find(query))
    print(f'Results: {results}')
    return results


        
tools = [get_schema,fetch_query_results]
llm_with_tools = llm.bind_tools(tools)


@app.get('/')
async def home():
    return {"messages": "Hello World!"}

@app.get('/api/query/')
async def query(query:str):
    print({"messages":query})
    prompt_template = PromptTemplate.from_template(
        (
            """
            you are a helpful chatbot that can interact with MongoDB database. 
            You will take user questions and turn them into MongoDB quieries using the tools available.
            Use get_schema to get the scheam of the collection and use fetch_query_results to execute a query
            inside MongoDB find function. Give just the query that will execute in MongoDB find function.

            {query}
            """
        ),
    )   
    response = llm_with_tools.invoke(prompt_template.invoke({"query": query}))
    database_data = fetch_query_results.invoke(response.tool_calls[-1]['args'])
    prompt_template = PromptTemplate.from_template(
    (
        """
        you are a helpful chatbot that can interact with MongoDB database. 
        You have given a data retrieved from database, and using that information you need to answer 
        the users query. Give short relevant answers to the question

        DATA:
        {data}

        user question
        {query}
        """
        ),

    )
    response = llm.invoke(prompt_template.invoke({"query": query, "data":database_data}))
    return {"messages":response}



