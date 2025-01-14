# db/process_query.py
from utils.logger import setup_logger

logger = setup_logger(__name__)

def process_query(chain, db, question: str):
    """將語音轉譯後的文本當作問題，生成 SQL 語句，並可選擇執行。"""
    try:
        generated_sql = chain.invoke(question)
        return generated_sql.strip()
    except Exception as e:
        logger.error(f"查詢處理出錯：{str(e)}")
        return None

