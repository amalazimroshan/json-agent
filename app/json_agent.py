import os
import json
from dotenv import load_dotenv

from langchain_community.agent_toolkits import JsonToolkit, create_json_agent
from langchain_community.tools.json.tool import JsonSpec
from langchain_groq import ChatGroq

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama3-8b-8192")

def read_json():
    with open("app/Procore_Subcontrator_Invoice.json") as f:
        data = json.load(f)
    if isinstance(data, list):
    # Option 1: Extract the first item if it makes sense
        if len(data) > 0:
            data = data[0]  # If you want the first object
        # Option 2: Convert list to dict using indices
        else:
            data = {str(i): item for i, item in enumerate(data)}

    return data


data = read_json()

def invoke_agent(query:str):
    data = read_json()

    json_spec = JsonSpec(dict_=data, max_length=4000)
    json_toolkit = JsonToolkit(spec=json_spec)

    json_agent_executor =  create_json_agent(
        llm=llm,
        toolkit=json_toolkit,
        verbose=True
    )
    
    resp = json_agent_executor.run(
        query
    )

    return resp
