import os
import urllib
from sqlalchemy import create_engine

def before_all(context):
    # If running on GitHub, use localhost. Otherwise, use your local Beelink machine!
    if os.getenv('GITHUB_ACTIONS') == 'true':
        server = 'localhost\\SQLEXPRESS'
        username = 'sa'
        password = 'Malik_123'  # Default Windows Runner SA Password container password
    else:
        server = 'Beelink\\SQLEXPRESS'
        username = 'auto_user'
        password = 'Password123!'

    database = 'Bussiness_DB'
    driver = '{ODBC Driver 17 for SQL Server}'

    raw_string = (
        f"DRIVER={driver};SERVER={server};DATABASE={database};"
        f"UID={username};PWD={password};Encrypt=no;TrustServerCertificate=yes;"
    )
    params = urllib.parse.quote_plus(raw_string)
    context.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")