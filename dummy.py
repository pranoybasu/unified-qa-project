import databaseConnection

# Establish the database connection
cnxn = databaseConnection.create_connection()

# Create a cursor
cursor = cnxn.cursor()

# Execute the query
query = 'SELECT DISTINCT TEST_PRODUCT, TEST_VENDOR FROM k12intel_userdata.xtbl_tests'
cursor.execute(query)

# Fetch and process the results
while True:
    rows = cursor.fetchmany(1000)
    if not rows:
        break
    for row in rows:
        print(row)

# Close the cursor and connection
cursor.close()
cnxn.close()
