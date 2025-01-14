# db/connection.py
from langchain_community.utilities import SQLDatabase
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_db_connection(username, password, host, database):
    """
    使用 mysql-connector 創建數據庫連接，並透過 SQLDatabase (LangChain) 進行管理。
    """
    try:
        db_uri = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
        db = SQLDatabase.from_uri(db_uri)
        logger.info("數據庫連接創建成功！")
        return db
    except Exception as e:
        logger.error(f"創建數據庫連接時出錯：{str(e)}")
        raise

