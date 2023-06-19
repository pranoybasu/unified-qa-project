import pyodbc

# Set up the connection string
server = '00uihp1smia001.public.fa2521a12da0.database.windows.net'
database = 'K12INTEL_DW_MASONOHIOSCHOOLS_East'
username = 'k12intel_etl'
password = 'l6ETZOu5YeL0Hn4iprSxCjM6F'
driver = '{ODBC Driver 18 for SQL Server}'
connection_string = f"DRIVER={driver};SERVER={server},3342;DATABASE={database};UID={username};PWD={password}"

# Connect to the database
cnxn = pyodbc.connect(connection_string)

# Execute a query with specific columns and filtering
cursor = cnxn.cursor()
cursor.execute('SELECT DISTINCT TEST_PRODUCT, TEST_VENDOR FROM k12intel_userdata.xtbl_tests')

# Fetch the results with pagination
while True:
    rows = cursor.fetchmany(1000)
    if not rows:
        break
    for row in rows:
        print(row)
