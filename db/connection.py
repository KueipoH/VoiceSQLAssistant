# db/connection.py
from langchain_community.utilities import SQLDatabase
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_db_connection(username, password, host, database):
    """
    Creates a database connection using mysql-connector and manages it through SQLDatabase (LangChain).
    """
    try:
        db_uri = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
        db = SQLDatabase.from_uri(db_uri)
        logger.info("Database connection created successfully!")
        return db
    except Exception as e:
        logger.error(f"Error creating database connection: {str(e)}")
        raise

