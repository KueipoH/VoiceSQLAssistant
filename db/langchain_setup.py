# db/langchain_setup.py
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import OpenAI as LangChainOpenAI
from utils.logger import setup_logger

logger = setup_logger(__name__)

def setup_langchain(db):
    """建立 LangChain 組件，用於將 SQL 查詢與 GPT 模型結合。"""
    try:
        prompt = PromptTemplate.from_template(
            """
            根據以下 SQL 表結構，請幫我用SQL語句回答問題:
            {schema}
            Question: {question}
            SQL Query: 讓我們一步一步思考:
            1) 我們需要從哪些表格獲取數據
            2) 我們需要哪些條件
            3) 如何組織和格式化結果
            僅需要輸出 SQL 查詢語句，不需要其他解釋：
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
        logger.error(f"設置 LangChain 時出錯：{str(e)}")
        raise

