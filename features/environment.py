import os
import urllib
from sqlalchemy import create_engine

def before_all(context):
    # If running on GitHub, connect to localhost\SQLEXPRESS with Windows Auth.
    # Otherwise, connect to your Beelink machine!
    if os.getenv('GITHUB_ACTIONS') == 'true':
        server = 'localhost\\SQLEXPRESS'
        raw_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=Bussiness_DB;Trusted_Connection=yes;Encrypt=no;"
    else:
        server = 'Beelink\\SQLEXPRESS'
        username = 'auto_user'
        password = 'Password123!' # Your local auto_user password
        raw_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=Bussiness_DB;UID={username};PWD={password};Encrypt=no;TrustServerCertificate=yes;"

    params = urllib.parse.quote_plus(raw_string)
    context.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")