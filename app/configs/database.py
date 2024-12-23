from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

os.environ.clear()
load_dotenv()
db_url = os.getenv('DB_URL')
print(db_url)
class DatabaseConnection:
    def __init__(self):
        self.engine = create_engine(db_url, pool_recycle=500, echo=True)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def get_connection(self):
        connection = self.engine.connect()
        return connection