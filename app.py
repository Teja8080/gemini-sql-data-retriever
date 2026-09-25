import streamlit as st
import sqlite3
from google  import genai
API_KEY = st.secrets['gemini_api_key']

#provide the API key to the client

client=genai.Client(api_key=API_KEY)

def get_gemini_response(prompt,question):
    inputs=(prompt,question)
    response=client.models.generate_content(model='gemini-2.5-flash',contents=inputs)
    return response.text


def read_sql_query(query,db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    data=cursor.execute(query)
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return(rows)

prompt="""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Naresh_it and has the following columns- employee_name, employee_role, employee_salary
    For example,
    
        Example 1 How many entries of records are present?,
        the SQL command will be something like this SELECT COUNT(*) FROM Naresh_it
        
        Example 2 Tell me all the employees working in Data Science role?,
        the SQL command will be something like this SELECT FROM Naresh_it
                                                    where employee_role="Data Science";
    
    also the sql code should not have and; in beginning or end and sql word in output"""



st.set_page_config(page_title="i can retrive any sql query")
st.header("Gemini app to retrive sql data")

question=st.text_input("input:",key="input")
submit=st.button("ask the question")

if submit:
    response=get_gemini_response(prompt,question)
    print(response)
    st.subheader("Generated SQL Query")
    st.code(response, language="sql")
    response=read_sql_query(response,'employee1.db')
    st.subheader("The response is:")
    for row in response:
        print(row)
        st.header(row)


