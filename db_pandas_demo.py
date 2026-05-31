import pandas as pd
from sqlalchemy import create_engine, text

# 1. Create the Database Engine
# This creates a physical file named 'automation.db' in your project folder.
engine = create_engine('sqlite:///automation.db')

print("--- Step 1: Creating Test Data in Pandas ---")
# Let's create a DataFrame simulating automated test results
test_results_data = {
    'test_id': [101, 102, 103, 104],
    'browser': ['Chrome', 'Firefox', 'Chrome', 'Safari'],
    'status': ['Passed', 'Failed', 'Passed', 'Passed'],
    'execution_time_sec': [4.5, 6.2, 3.8, 5.1]
}
df_to_save = pd.DataFrame(test_results_data)
print(df_to_save)


print("\n--- Step 2: Writing DataFrame to SQL Database ---")
# .to_sql() automatically creates the table 'ui_test_logs' and maps the columns!
# 'if_exists=replace' overwrites the table if it already exists
df_to_save.to_sql('ui_test_logs', con=engine, if_exists='replace', index=False)
print("Database table 'ui_test_logs' created and populated successfully!")


print("\n--- Step 3: Reading Data back using SQL Query ---")
# Write a clean, standard SQL query
my_query = "SELECT browser, status FROM ui_test_logs WHERE status = 'Passed'"

# .read_sql() combines the query and the engine to return a fresh DataFrame
df_passed_tests = pd.read_sql(my_query, con=engine)
print(df_passed_tests)


print("\n--- Step 4: Performing Pandas Analytics on SQL Data ---")
# Now that it's in Pandas, you can instantly run data calculations
avg_time = df_to_save['execution_time_sec'].mean()
print(f"Average Execution Time: {avg_time:.2f} seconds")