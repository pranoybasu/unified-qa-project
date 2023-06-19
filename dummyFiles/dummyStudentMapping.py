# Start of the medium matched/unmapped students analysis
import databaseConnection

# Establish the database connection
cnxn = databaseConnection.create_connection()

# Create a cursor
cursor = cnxn.cursor()

# Execute the query
query = """
    SELECT DISTINCT
        B.STUDENT_FIRST_NAME,
        B.STUDENT_MIDDLE_NAME,
        B.STUDENT_LAST_NAME,
        B.TEST_STUDENT_GRADE,
        CASE
            WHEN B.STUDENT_BIRTHDATE_STR LIKE '%null%' OR B.STUDENT_BIRTHDATE_STR LIKE '%nan%' THEN ''
            ELSE B.STUDENT_BIRTHDATE_STR
        END AS 'STUDENT_BIRTHDATE_STR',
        asi.SOURCE_SCHOOL_CODE,
        asi.SOURCE_STUDENT_ID,
        asi.SOURCE_STATE_STUDENT_ID,
        asi.MAPPED_STUDENT_ID,
        asi.MAPPED_STATE_STUDENT_ID,
        '' AS 'CORRECT_STUDENT_ID',
        '' AS 'CORRECT_STATE_STUDENT_ID',
        '' AS 'IGNORE_STUDENT',
        A.BATCH_NAME,
        asi.STUDENT_IDENTITY_UUID
    FROM K12INTEL_USERDATA.XTBL_TEST_BATCH_IDS A
    JOIN K12INTEL_USERDATA.XTBL_TEST_ADMIN B ON A.BATCH_ID = B.BATCH_ID AND B.SYS_PARTITION_VALUE = a.SYS_PARTITION_VALUE
    JOIN K12INTEL_assessment.ASSESSMENT_STUDENT_IDENTITY asi ON asi.STUDENT_IDENTITY_UUID = B.STUDENT_IDENTITY_UUID AND asi.SYS_PARTITION_VALUE = B.SYS_PARTITION_VALUE
    WHERE 1=1
        AND B.DELETE_TEST_ADMIN_IND <> 'Y'
        AND A.BATCH_ID = ?  -- Specify the batch ID here
        AND asi.IDENTITY_MAPPING_TYPE <> 'USER'
        AND B.SYS_RECORD_STAGE = 'NOT VALIDATED'
        AND (
            asi.MAPPED_STUDENT_ID IS NULL OR asi.MAPPED_STUDENT_ID = '' OR
            asi.IDENTITY_MAPPING_TYPE = 'NOT MAPPED' OR asi.IDENTITY_MATCH_QUALITY = 'medium'
        )
    ORDER BY 3, 1, 2
"""

batch_id = input("Enter the batch ID: ")  # Accept the batch ID from the user
cursor.execute(query, (batch_id,))  # Pass the batch ID as a parameter to the query

# Fetch and process the results
rows = cursor.fetchall()  # Fetch all the rows
if rows:
    for row in rows:
        # Retrieve the values from the row
        student_first_name = row.STUDENT_FIRST_NAME
        student_middle_name = row.STUDENT_MIDDLE_NAME
        student_last_name = row.STUDENT_LAST_NAME
        test_student_grade = row.TEST_STUDENT_GRADE
        student_birthdate_str = row.STUDENT_BIRTHDATE_STR
        source_school_code = row.SOURCE_SCHOOL_CODE
        source_student_id = row.SOURCE_STUDENT_ID
        source_state_student_id = row.SOURCE_STATE_STUDENT_ID
        mapped_student_id = row.MAPPED_STUDENT_ID
        mapped_state_student_id = row.MAPPED_STATE_STUDENT_ID
        correct_student_id = row.CORRECT_STUDENT_ID
        correct_state_student_id = row.CORRECT_STATE_STUDENT_ID
        ignore_student = row.IGNORE_STUDENT
        batch_name = row.BATCH_NAME
        student_identity_uuid = row.STUDENT_IDENTITY_UUID

        # Perform any further processing or display the retrieved values
        print(f"Student First Name: {student_first_name}")
        print(f"Student Middle Name: {student_middle_name}")
        print(f"Student Last Name: {student_last_name}")
        print(f"Test Student Grade: {test_student_grade}")
        print(f"Student Birthdate: {student_birthdate_str}")
        print(f"Source School Code: {source_school_code}")
        print(f"Source Student ID: {source_student_id}")
        print(f"Source State Student ID: {source_state_student_id}")
        print(f"Mapped Student ID: {mapped_student_id}")
        print(f"Mapped State Student ID: {mapped_state_student_id}")
        print(f"Correct Student ID: {correct_student_id}")
        print(f"Correct State Student ID: {correct_state_student_id}")
        print(f"Ignore Student: {ignore_student}")
        print(f"Batch Name: {batch_name}")
        print(f"Student Identity UUID: {student_identity_uuid}")
        print("---")
else:
    print("No medium matched/unmapped students found for the specified batch ID.")

# Close the cursor and connection
cursor.close()
cnxn.close()
