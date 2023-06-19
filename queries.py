import databaseConnection

# Function to execute a query and return the results
def execute_query(query, parameters=None):
    # Establish the database connection
    cnxn = databaseConnection.create_connection()

    # Create a cursor
    cursor = cnxn.cursor()

    # Execute the query
    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)

    # Fetch and return the results
    rows = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return rows

# Function to retrieve batches
def get_batches(batch_id):
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
    return execute_query(query, (batch_id,))

# Function to retrieve rejects
def get_rejects(process_id):
    query = """
        SELECT PROCESS_ID, PROCESS_NAME, REJECT_BASE_MESSAGE, COUNT(*) AS RejectCount
        FROM K12INTEL_AUDIT.FILE_PROCESS_REJECTS
        WHERE 1=1
            AND PROCESS_TYPE = 'Assessment'
            AND PROCESS_ID = ?
        GROUP BY PROCESS_ID, PROCESS_NAME, REJECT_BASE_MESSAGE
    """
    return execute_query(query, (process_id,))

# Function to retrieve medium matches
def get_medium_matches(batch_id):
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
            AND A.BATCH_ID = ?
            AND asi.IDENTITY_MAPPING_TYPE <> 'USER'
            AND B.SYS_RECORD_STAGE = 'NOT VALIDATED'
            AND (
                asi.MAPPED_STUDENT_ID IS NULL OR asi.MAPPED_STUDENT_ID = '' OR
                asi.IDENTITY_MAPPING_TYPE = 'NOT MAPPED' OR asi.IDENTITY_MATCH_QUALITY = 'medium'
            )
        ORDER BY 3, 1, 2
    """
    return execute_query(query, (batch_id,))

# Function to retrieve unmapped schools
def get_unmapped_schools(batch_id):
    query = """
        SELECT DISTINCT sc.*
        FROM K12INTEL_USERDATA.XTBL_TEST_BATCH_IDS A
        JOIN K12INTEL_USERDATA.XTBL_TEST_ADMIN B ON A.BATCH_ID = B.BATCH_ID AND a.SYS_PARTITION_VALUE = B.SYS_PARTITION_VALUE
        JOIN k12intel_assessment.ASSESSMENT_SCHOOL_IDENTITY sc ON sc.SCHOOL_IDENTITY_UUID = B.SCHOOL_IDENTITY_UUID AND sc.SYS_PARTITION_VALUE = B.SYS_PARTITION_VALUE
        WHERE 1=1
            AND B.DELETE_TEST_ADMIN_IND <> 'Y'
            AND A.BATCH_ID = ?
            AND sc.IDENTITY_MAPPING_TYPE = 'NOT MAPPED'
    """
    return execute_query(query, (batch_id,))
