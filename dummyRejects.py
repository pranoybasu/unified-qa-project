# Start of the rejects analysis
import databaseConnection

# Establish the database connection
cnxn = databaseConnection.create_connection()

# Create a cursor
cursor = cnxn.cursor()

# Execute the query
query = """
    SELECT PROCESS_ID, PROCESS_NAME, REJECT_BASE_MESSAGE, COUNT(*) AS RejectCount
    FROM K12INTEL_AUDIT.FILE_PROCESS_REJECTS
    WHERE 1=1
        AND PROCESS_TYPE = 'Assessment'
        AND PROCESS_ID = ?
    GROUP BY PROCESS_ID, PROCESS_NAME, REJECT_BASE_MESSAGE
"""
process_id = input("Enter the process ID: ")  # Accept the process ID from the user
cursor.execute(query, (process_id,))  # Pass the process ID as a parameter to the query

# Fetch and process the results
rows = cursor.fetchall()  # Fetch all the rows matching the process ID
if len(rows) > 0:
    for row in rows:
        # Retrieve the values from the row
        process_id = row.PROCESS_ID
        process_name = row.PROCESS_NAME
        reject_message = row.REJECT_BASE_MESSAGE
        reject_count = row.RejectCount

        # Perform any further processing or display the retrieved values
        print(f"Process ID: {process_id}")
        print(f"Process Name: {process_name}")
        print(f"Reject Message: {reject_message}")
        print(f"Reject Count: {reject_count}")
        print("-----")
else:
    print("No rejects found for the specified process ID.")

# Close the cursor and connection
cursor.close()
cnxn.close()
