import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

def initialize_components():
    """Initialize environment, LLM, and database connection."""
    load_dotenv()
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ["GOOGLE_API_KEY"])
    db = SQLDatabase.from_uri(
        os.environ["OUTPUT_STRING"], 
        sample_rows_in_table_info=3
    )
    return llm, db

def generate_natural_language_response(llm, db, question):
    """Generate a natural language response from a database query based on a question."""
    # Create SQL query chain
    sql_query_chain = create_sql_query_chain(llm, db)
    
    # Generate SQL query
    query = sql_query_chain.invoke({"question": question})
    cleaned_query = query.strip('sql\n').strip('\n')
    
    # Execute query
    result = db.run(cleaned_query)
    
    # Define conversational response prompt
    conversational_response_prompt = PromptTemplate(
        input_variables=["question", "query", "result"],
        template="""Generate a professional, concise, and formal response to the database query.
        
        Original Question: {question}
        SQL Query: {query}
        Database Result: {result}
        
        Please provide a natural, human-readable explanation of the result. Make it sound like you're having a casual conversation:"""
    )
    
    # Create response generation chain
    conversational_chain = conversational_response_prompt | llm | StrOutputParser()
    
    # Generate and return response
    return conversational_chain.invoke({
        "question": question,
        "query": cleaned_query,
        "result": result
    })