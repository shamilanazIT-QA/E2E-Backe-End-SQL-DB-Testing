from behave import given, when, then
import pandas as pd
from sqlalchemy import text


@given('the database connection is active')
def step_impl(context):
    assert context.engine is not None, "Database engine was not initialized!"


@when('we query the total number of records in "{table_name}"')
def step_impl(context, table_name):
    query = f"SELECT COUNT(*) as total FROM [{table_name}]"
    with context.engine.connect() as conn:
        df = pd.read_sql(text(query), con=conn)
    context.row_count = int(df['total'].iloc[0])


@then('the total row count should be greater than {min_count:d}')
def step_impl(context, min_count):
    assert context.row_count > min_count, f"Expected > {min_count} rows, but found {context.row_count}"


@when('a new dummy sale is inserted into the discounts')
def step_impl(context):
    # 🌟 FIX: We use sale_id = 1 because it explicitly exists in your sales table!
    query = text("""
        INSERT INTO [discounts] (sale_id, discount_percent) 
        VALUES (1, 10.00)
    """)

    with context.engine.begin() as conn:
        conn.execute(query)


@then('the "{table_name}" table should automatically calculate the expected markdown value')
def step_impl(context, table_name):
    # Fetch the absolute newest calculated row from the discounts table
    query = text("SELECT TOP 1 discount_amount FROM discounts ORDER BY discount_id DESC")

    with context.engine.connect() as conn:
        df = pd.read_sql(query, con=conn)

    actual_discount = float(df['discount_amount'].iloc[0])

    # 🌟 MATH: 950.00 (iPhone price from sale_id 1) * 10% = 95.00
    expected_discount = 95.00

    assert actual_discount == expected_discount, (
        f"Trigger calculation mismatch! Expected {expected_discount}, got {actual_discount}"
    )