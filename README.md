# MongoDB Natural Language Data Interpreter

## Project Overview

This application is a powerful LLM (Large Language Model) powered tool that connects to a MongoDB database and provides natural language explanations of the stored data. By leveraging the Groq API and LangChain, the project transforms raw database information into easily understandable insights.


## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)
- Groq API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/amalazimroshan/json-agent.git
cd json-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
MONGO_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
```

## Dependencies

- FastAPI
- PyMongo
- python-dotenv
- LangChain
- Groq


## Usage

Run the application:

```bash
fastapi dev app/main.py
```
