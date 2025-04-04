import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Initialize the language model
llm = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ["GOOGLE_API_KEY"])

# Connect to the database
db = SQLDatabase.from_uri(
    "mysql+pymysql://root:mysqlrootpassword@127.0.0.1:3306/output?ssl_disabled=true", 
    sample_rows_in_table_info=3
)

# Create a custom conversational response prompt
conversational_response_prompt = PromptTemplate(
    input_variables=["question", "query", "result"],
    template="""Generate a professional, concise, and formal response to the database query. If you don't have an answer, say \"I don't have an answer to this question.\" If the input is a greeting, respond as a normal conversational chatbot.


Original Question: {question}
SQL Query: {query}
Database Result: {result}

Please provide a natural, human-readable explanation of the result. Make it sound like you're having a casual conversation:"""
)

# def get_natural_language_result(question):
#     # Create a chain to generate SQL query
#     sql_query_chain = create_sql_query_chain(llm, db)
    
#     # Generate SQL query dynamically based on the question
#     query = sql_query_chain.invoke({"question": question})
    
#     # Clean the query (remove any code block markers)
#     # cleaned_query = query.strip('sql\n').strip('\n')
#     cleaned_query = query.replace("```sql", "").replace("```", "").strip()
    
#     # Execute the query
#     result = db.run(cleaned_query)
    
#     # Create a chain to convert result to conversational language
#     conversational_chain = conversational_response_prompt | llm | StrOutputParser()
    
#     # Generate natural language response
#     natural_response = conversational_chain.invoke({
#         "question": question,
#         "query": cleaned_query,
#         "result": result
#     })
    
#     return natural_response

def get_natural_language_result(question):
    # Handle greetings separately
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    if question.lower() in greetings:
        return "Hello! How can I assist you today?"
    
    # Create a chain to generate SQL query
    sql_query_chain = create_sql_query_chain(llm, db)
    
    # Generate SQL query dynamically based on the question
    query = sql_query_chain.invoke({"question": question})
    
    # Clean the query (remove any code block markers)
    cleaned_query = query.replace("```sql", "").replace("```", "").strip()
    
    # Ensure the generated query starts with a valid SQL command
    valid_sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE"]
    if not any(cleaned_query.upper().startswith(keyword) for keyword in valid_sql_keywords):
        return "I couldn't generate a valid SQL query for your question."
    
    # Execute the query
    result = db.run(cleaned_query)
    
    # Create a chain to convert result to conversational language
    conversational_chain = conversational_response_prompt | llm | StrOutputParser()
    
    # Generate natural language response
    natural_response = conversational_chain.invoke({
        "question": question,
        "query": cleaned_query,
        "result": result
    })
    
    return natural_response