# db/langchain_setup.py
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import OpenAI as LangChainOpenAI
from utils.logger import setup_logger

logger = setup_logger(__name__)

def setup_langchain(db):
    """Sets up LangChain components to integrate SQL queries with GPT models."""
    try:
        prompt = PromptTemplate.from_template(
            """
            Based on the following SQL table structure, please answer the question using SQL statements:
            {schema}
            Question: {question}
            SQL Query: Let's think step by step:
            1) Which tables do we need to retrieve data from?
            2) What conditions do we need?
            3) How to organize and format the results?
            Only output the SQL query statement, no additional explanations:
            """
        )

        llm = LangChainOpenAI(temperature=0)

        def get_schema(_):
            return db.get_table_info()

        chain = (
            {"schema": get_schema, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain

    except Exception as e:
        logger.error(f"Error setting up LangChain: {str(e)}")
        raise

