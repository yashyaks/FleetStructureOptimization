import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

def initialize_components():
    """Initialize environment variables, LLM, and database connection."""
    load_dotenv()
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ.get("GOOGLE_API_KEY"))
    db = SQLDatabase.from_uri(os.environ.get("OUTPUT_STRING"), sample_rows_in_table_info=3)
    return llm, db

def generate_natural_language_response(llm, db, question):
    """Generate a human-readable response based on a database query."""
    try:
        # Generate SQL query
        sql_query_chain = create_sql_query_chain(llm, db)
        query = sql_query_chain.invoke({"question": question}).strip('sql\n').strip('\n')
        
        if not query:
            return "I'm sorry, but I cannot answer this question."
        
        # Execute query
        result = db.run(query)
        if not result:
            return "I'm sorry, but I cannot answer this question based on the available data."
        
        # Define conversational response prompt
        conversational_response_prompt = PromptTemplate(
            input_variables=["question", "query", "result"],
            template="""
            Generate a professional, concise, and formal response to the database query.
            
            Original Question: {question}
            SQL Query: {query}
            Database Result: {result}
            
            If the result is empty or irrelevant, respond with: 'I'm sorry, but I cannot answer this question based on the available data.'
            Incase the user says something random act like a normal chatbot in a formal and conversational tone.
            
            Provide a natural, human-readable explanation of the result:
            """
        )
        
        conversational_chain = conversational_response_prompt | llm | StrOutputParser()
        return conversational_chain.invoke({"question": question, "query": query, "result": result})
    except Exception as e:
        return query

def is_greeting(text):
    """Check if the input text is a greeting."""
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    return text.lower() in greetings