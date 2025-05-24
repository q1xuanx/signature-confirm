import os
from dotenv import load_dotenv

load_dotenv()

class Setting: 

    USERNAME = os.getenv('username_db')
    PASSWORD = os.getenv('password')
    DATABASE_NAME = os.getenv('db_name')
    SERVER = os.getenv('server')
    PORT = os.getenv('port')
    DATABASE_URL : str = f"postgresql://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE_NAME}"

setting = Setting