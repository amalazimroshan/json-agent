from fastapi import FastAPI
from app.json_agent import invoke_agent
app = FastAPI()

@app.get('/')
async def home():
    return {"messages": "Hello World!"}

@app.get('/api/query/')
async def query(query:str):

    response = invoke_agent(query)
    return {"messages":response}



