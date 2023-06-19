# Start of the school mappings analysis
import databaseConnection

# Establish the database connection
cnxn = databaseConnection.create_connection()

# Create a cursor
cursor = cnxn.cursor()

# Execute the query
query = """
    SELECT DISTINCT sc.*
    FROM K12INTEL_USERDATA.XTBL_TEST_BATCH_IDS A
    JOIN K12INTEL_USERDATA.XTBL_TEST_ADMIN B ON A.BATCH_ID = B.BATCH_ID AND a.SYS_PARTITION_VALUE = B.SYS_PARTITION_VALUE
    JOIN k12intel_assessment.ASSESSMENT_SCHOOL_IDENTITY sc ON sc.SCHOOL_IDENTITY_UUID = B.SCHOOL_IDENTITY_UUID AND sc.SYS_PARTITION_VALUE = B.SYS_PARTITION_VALUE
    WHERE 1=1
        AND B.DELETE_TEST_ADMIN_IND <> 'Y'
        AND A.BATCH_ID = ?  -- Specify the batch ID here
        AND sc.IDENTITY_MAPPING_TYPE = 'NOT MAPPED'
"""

batch_id = input("Enter the batch ID: ")  # Accept the batch ID from the user
cursor.execute(query, (batch_id,))  # Pass the batch ID as a parameter to the query

# Fetch and process the results
rows = cursor.fetchall()  # Fetch all the rows
if rows:
    for row in rows:
        # Retrieve the values from the row
        # Adjust the column names accordingly based on the actual columns in the result set
        school_id = row.SCHOOL_ID
        school_name = row.SCHOOL_NAME
        school_district_code = row.SCHOOL_DISTRICT_CODE
        school_state_code = row.SCHOOL_STATE_CODE

        # Perform any further processing or display the retrieved values
        print(f"School ID: {school_id}")
        print(f"School Name: {school_name}")
        print(f"School District Code: {school_district_code}")
        print(f"School State Code: {school_state_code}")
        print("---")
else:
    print("No school mappings found for the specified batch ID and identity mapping type.")

# Close the cursor and connection
cursor.close()
cnxn.close()
