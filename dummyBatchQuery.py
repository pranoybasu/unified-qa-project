# Start of the batch q analysis
import databaseConnection

# Establish the database connection
cnxn = databaseConnection.create_connection()

# Create a cursor
cursor = cnxn.cursor()

# Execute the query
query = """
    SELECT A.BATCH_ID, A.BATCH_NAME, A.LOAD_STATUS, B.SYS_RECORD_STAGE, COUNT(DISTINCT B.TEST_ADMIN_KEY) "AdminCnt", COUNT(*) "ScoreCnt"
    FROM K12INTEL_USERDATA.XTBL_TEST_BATCH_IDS A
    JOIN K12INTEL_USERDATA.XTBL_TEST_ADMIN B ON A.BATCH_ID = B.BATCH_ID 
    JOIN K12INTEL_USERDATA.XTBL_TEST_SCORES C ON B.TEST_ADMIN_KEY = C.TEST_ADMIN_KEY 
    WHERE 1=1
        AND A.BATCH_ID > 0 
        AND B.DELETE_TEST_ADMIN_IND <> 'Y'
        AND A.BATCH_ID = ?
    GROUP BY A.BATCH_ID, A.BATCH_NAME, A.LOAD_STATUS, B.SYS_RECORD_STAGE
    ORDER BY A.BATCH_NAME, A.LOAD_STATUS, B.SYS_RECORD_STAGE
"""
batch_id = input("Enter the batch ID: ")  # Accept the batch ID from the user
cursor.execute(query, (batch_id,))  # Pass the batch ID as a parameter to the query

# Fetch and process the results
row = cursor.fetchone()  # Fetch the first row matching the batch ID
if row:
    # Retrieve the values from the row
    batch_id = row.BATCH_ID
    batch_name = row.BATCH_NAME
    load_status = row.LOAD_STATUS
    sys_record_stage = row.SYS_RECORD_STAGE
    admin_count = row.AdminCnt
    score_count = row.ScoreCnt

    # Perform any further processing or display the retrieved values
    print(f"Batch ID: {batch_id}")
    print(f"Batch Name: {batch_name}")
    print(f"Load Status: {load_status}")
    print(f"Sys Record Stage: {sys_record_stage}")
    print(f"Admin Count: {admin_count}")
    print(f"Score Count: {score_count}")
else:
    print("No rows found for the specified batch ID.")

# Close the cursor and connection
cursor.close()
cnxn.close()
