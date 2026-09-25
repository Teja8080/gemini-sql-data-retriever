import streamlit as st
import sqlite3
from google import genai


# Get Gemini API key from Streamlit Secrets
API_KEY = st.secrets["gemini_api_key"]

# Provide the API key to the Gemini client
client = genai.Client(api_key=API_KEY)


# Function to get SQL query from Gemini
def get_gemini_response(prompt, question):
    inputs = (prompt, question)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=inputs
    )

    # Remove Markdown code fences from Gemini's response
    return response.text.replace("```sql", "").replace("```", "").strip()


# Function to execute SQL query
def read_sql_query(query, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    try:
        data = cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except sqlite3.Error as e:
        st.error(f"SQL Error: {e}")
        return []

    finally:
        connection.close()


# Prompt for Gemini
prompt = """
You are an expert in converting English questions into SQL queries.

The SQL database is named Naresh_it and has the following columns:
employee_name, employee_role, employee_salary

Example 1:
Question: How many entries of records are present?
SQL query:
SELECT COUNT(*) FROM Naresh_it

Example 2:
Question: Tell me all the employees working in Data Science role?
SQL query:
SELECT * FROM Naresh_it
WHERE employee_role = "Data Science"

Example 3:
Question: Show the top 3 employees based on salary.
SQL query:
SELECT * FROM Naresh_it
ORDER BY employee_salary DESC
LIMIT 3

Important instructions:
- Return ONLY the SQL query.
- Do not use Markdown code blocks.
- Do not include ```sql or ``` in the output.
- Do not include the word SQL in the output.
- Do not include explanations before or after the query.
- Do not add a semicolon at the beginning or end of the query.
- Use the table name Naresh_it exactly.
- Use only the columns employee_name, employee_role, and employee_salary.
"""


# Streamlit page configuration
st.set_page_config(
    page_title="I Can Retrieve Any SQL Query"
)

st.header("Gemini App to Retrieve SQL Data")


# User input
question = st.text_input(
    "Input:",
    key="input"
)

submit = st.button("Ask the Question")


# When the user clicks the button
if submit:

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:
        # Generate SQL query using Gemini
        response = get_gemini_response(prompt, question)

        print(response)

        # Display generated SQL query
        st.subheader("Generated SQL Query")
        st.code(response, language="sql")

        # Execute SQL query
        result = read_sql_query(
            response,
            "employee1.db"
        )

        # Display results
        st.subheader("The Response Is:")

        if result:
            for row in result:
                st.write(row)
        else:
            st.info("No results found.")

