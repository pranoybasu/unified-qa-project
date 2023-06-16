import pyodbc

def create_connection():
    # Set up the connection details
    server = '00uihp1smia001.public.fa2521a12da0.database.windows.net'
    database = 'K12INTEL_DW_MASONOHIOSCHOOLS_East'
    username = 'k12intel_etl'
    password = 'l6ETZOu5YeL0Hn4iprSxCjM6F'
    driver = '{ODBC Driver 18 for SQL Server}'

    # Define the connection string
    connection_string = f"DRIVER={driver};SERVER={server},3342;DATABASE={database};UID={username};PWD={password}"

    # Establish the database connection
    return pyodbc.connect(connection_string)
