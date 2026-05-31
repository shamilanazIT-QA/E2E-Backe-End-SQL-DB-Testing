import pandas as pd
from sqlalchemy import create_engine, inspect
import urllib

# 1. Define connection parts clearly to prevent backslash parsing errors
server = 'Beelink\\SQLEXPRESS'
database = 'Bussiness_DB'  # ⚠️ NOTE: If it fails, change this to 'Business_DB' to match your SSMS spelling!
username = 'auto_user'
password = 'Password123!'
driver = '{ODBC Driver 17 for SQL Server}'

# 2. Build and safely encode the connection payload
raw_connection_string = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(raw_connection_string)
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"

# 3. Create a clean, single engine instance
engine = create_engine(connection_url)

# 4. Use SQLAlchemy Inspector to get all table names automatically
try:
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    print(f"🔍 Discovered {len(table_names)} tables in {database}!\n")
except Exception as e:
    print(f"💥 Master Connection failed! Check database spelling. Error: {e}")
    table_names = []

# Dictionary to store all your dataframes: {'table_name': dataframe}
all_my_tables = {}

# 5. Loop through every table name and read it into Pandas
for table in table_names:
    # Wrap table name in brackets to safely handle any spaces or SQL keywords
    query = f"SELECT * FROM [{table}]"

    try:
        # Pull the current table data
        df = pd.read_sql(query, con=engine)
        all_my_tables[table] = df
        print(f"✅ Successfully pulled table: [{table}] - Total Rows: {len(df)}")
    except Exception as e:
        print(f"❌ Failed to pull table: [{table}]. Error: {e}")

print("\n--- 🚀 Individual Table Data Sample ---")

# 6. Access your tables directly from your dictionary
if 'employees' in all_my_tables:
    print("\n[employees] Table Data:")
    print(all_my_tables['employees'].head())

if 'discounts' in all_my_tables:
    print("\n[discounts] Table Data:")
    print(all_my_tables['discounts'].head())