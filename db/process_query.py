# db/process_query.py
from utils.logger import setup_logger

logger = setup_logger(__name__)

def process_query(chain, db, question: str):
    """Processes the transcribed text as a question, generates SQL statements, and optionally executes them."""
    try:
        generated_sql = chain.invoke(question)
        return generated_sql.strip()
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return None

