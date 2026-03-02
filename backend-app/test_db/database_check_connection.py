import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

load_dotenv()

db_user = os.getenv('DB_USER')
db_pwd = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')
db_host = os.getenv('DB_HOST')

DATABASE_URL = f"postgresql://{db_user}:{db_pwd}@{db_host}/{db_name}"

engine = create_engine(DATABASE_URL)

try:
    print("Attempting to connect to database...\n")
    
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Connection successful!")
        print("Test query result:", result.scalar())

except OperationalError as e:
    print("❌ Connection failed!")
    print("Error details:")
    print(e)

except Exception as e:
    print("⚠️ Unexpected error:")
    print(e)