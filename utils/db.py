import os
import sqlite3
import pandas as pd

# Function to safely quote identifiers
def quote_identifier(identifier):
    return f'"{identifier}"'
    #return f"'{identifier}'" 

# Discover and Load CSV Files
def discover_csv_files_and_structure(directory):
    files_structure = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            table_name = filename.split('.')[0]
            df = pd.read_csv(os.path.join(directory, filename))
            files_structure[table_name] = {
                'columns': df.columns.tolist(),
                'data': df
            }
    return files_structure

# Discover csv schema
def read_csv_schema_from_excel(csv_schema_excel_path):
    """Read relationships and structure information from an Excel file."""
    relationships_df = pd.read_excel(csv_schema_excel_path)
    relationships = {}
    column_types = {}
    for _, row in relationships_df.iterrows():
        table_name = row['table_name']
        column_name = row['column']
        column_type = row['type']
        column_details = {
            'type': column_type,
            'target_table': row['target_table'] if 'FK' in column_type else None,
            'target_column': row['target_column'] if 'FK' in column_type else None
        }
        column_types.setdefault(table_name, {})[column_name] = column_details
        if 'FK' in column_type:
            relationships[(table_name, column_name)] = row['target_table']#(row['target_table'], row['target_column'])
    return relationships, column_types

# Analyze files and columns to map relationships
#def map_relationships(files_structure):
#    relationships = {}
#    for table_name, details in files_structure.items():
#        for column in details['columns']:
#            if column.endswith('_id') and column != 'id':
#                ref_table = column.rsplit('_id', 1)[0]
#                relationships[(table_name, column)] = ref_table
#    return relationships

def sort_tables_by_dependency(relationships):
    # Initialize containers for tracking table relationships
    all_tables = set()
    dependency_map = {}
    
    # Populate the dependency map and all_tables set
    for (table_name, column), ref_table in relationships.items():
        all_tables.add(table_name)
        all_tables.add(ref_table)
        if table_name not in dependency_map:
            dependency_map[table_name] = set()
        dependency_map[table_name].add(ref_table)
    
    # Identify independent tables (those not depending on other tables)
    independent_tables = {table for table in all_tables if table not in dependency_map}
    
    # The sorted list starts with independent tables
    sorted_tables = list(independent_tables)
    
    # Add dependent tables to the sorted list
    for table in dependency_map:
        if table not in sorted_tables:
            sorted_tables.append(table)
    
    return sorted_tables

def create_database_and_tables(files_structure, sorted_table_names, column_types, db_output_dir='example.db'):
    """Create a database and tables based on the defined CSV structure and relationships from the Excel file."""
    # Remove the existing database file if it exists
    if os.path.exists(db_output_dir):
        os.remove(db_output_dir)

    conn = sqlite3.connect(db_output_dir)
    cur = conn.cursor()

    # Enable foreign key support 
    cur.execute("PRAGMA foreign_keys = ON")
    
    # Create tables using schema information from the Excel file
    for table_name, details in files_structure.items():
        column_defs = []
        foreign_keys_sql = []

        for col in details['columns']:
            col_type_info = column_types.get(table_name, {}).get(col, {})
            col_type = col_type_info.get('type', 'TEXT')
            
            if col_type == 'PK':
                col_definition = f"{quote_identifier(col)} PRIMARY KEY"#f"{quote_identifier(col)} INTEGER PRIMARY KEY AUTOINCREMENT"
            elif col_type == 'DATETIME':
                col_definition = f"{quote_identifier(col)} DATETIME"
            elif col_type == 'FK':
                target_table = col_type_info['target_table']
                target_column = col_type_info['target_column']
                col_definition = f"{quote_identifier(col)} TEXT"
                foreign_keys_sql.append(
                    f"FOREIGN KEY ({quote_identifier(col)}) REFERENCES {quote_identifier(target_table)}({quote_identifier(target_column)})"
                )
            else:
                col_definition = f"{quote_identifier(col)} TEXT"

            column_defs.append(col_definition)

        create_table_sql = f"CREATE TABLE {quote_identifier(table_name)} ({', '.join(column_defs + foreign_keys_sql)})"
        print(create_table_sql)
        cur.execute(create_table_sql)
    
    # Insert data in sorted order
    for table_name in sorted_table_names:
        if table_name in files_structure:
            details = files_structure[table_name]
            details['data'].to_sql(table_name, conn, if_exists='append', index=False, method="multi")
            print(f"Data inserted into table {table_name}")

    conn.commit()
    conn.close()
    print('Database created: ' + db_output_dir)

# Create Database and Tables
#def create_database_and_tables(files_structure, relationships, sorted_table_names, db_output_dir = 'example.db'):
#    # Remove the example.db file if it exists
#    if os.path.exists(db_output_dir):
#        os.remove(db_output_dir)
#    conn = sqlite3.connect(db_output_dir)
#    cur = conn.cursor()
#    
#    # Enable foreign key support 
#    cur.execute("PRAGMA foreign_keys = ON")
#    
#    # Create tables without inserting data yet
#    for table_name, details in files_structure.items():
#        cols = details['columns']
#        columns_sql = [f"{quote_identifier(col)} TEXT" if col != 'id' else f"{quote_identifier(col)} PRIMARY KEY" for col in cols]
#        
#        foreign_keys_sql = []
#        for (src_table, column), ref_table in relationships.items():
#            if src_table == table_name and column.endswith('_id'):
#                foreign_keys_sql.append(f"FOREIGN KEY ({quote_identifier(column)}) REFERENCES {quote_identifier(ref_table)}({quote_identifier('id')})")
#        
#        create_table_sql = f"CREATE TABLE {quote_identifier(table_name)} ({', '.join(columns_sql + foreign_keys_sql)})"
#        #create_table_sql = f"CREATE TABLE IF NOT EXISTS {quote_identifier(table_name)} ({', '.join(columns_sql + foreign_keys_sql)})"
#
#        print(create_table_sql)
#        cur.execute(create_table_sql)
#    
#    # Insert data in sorted order
#    for table_name in sorted_table_names:
#        if table_name in files_structure:
#            details = files_structure[table_name]
#            details['data'].to_sql(table_name, conn, if_exists='append', index=False, method="multi")
#            print(f"Data inserted into table {table_name}")
#    
#    conn.commit()
#    conn.close()
#    print('Database created: ' + db_output_dir)
#    #return conn

def get_database_schema(path_to_db):
    conn = sqlite3.connect(path_to_db)
    schema = []
    cur = conn.cursor()
    for row in cur.execute("SELECT type, name, sql FROM sqlite_master WHERE type='table' ORDER BY name"):
        schema.append(f"{row[0].upper()} {row[1]}:\n{row[2]};\n")
    conn.close()  
    return "\n".join(schema)

def get_list_tables(path_to_db):
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    return [table[0] for table in tables]  # Extract table names from tuples

def inspect_table(path_to_db, table_name, limit=5):
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    query = f'SELECT * FROM "{table_name}" LIMIT {limit};'
    #query = f"SELECT * FROM '{table_name}' LIMIT {limit};"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def run_query_and_return_df(path_to_db, query, params=None):
    """
    Executes a SQL query and returns the results as a pandas DataFrame.
    
    :param path_to_db: The path to the SQLite database file.
    :param query: The SQL query string to be executed.
    :param params: Optional parameters to be bound to the query. Defaults to None.
    :return: A pandas DataFrame containing the results of the query.
    """
    # Connect to the SQLite database
    with sqlite3.connect(path_to_db) as conn:
        # If params is None, pandas will execute the query without parameters
        df = pd.read_sql_query(query, conn, params=params)
    return df

def get_database_schema_execute_all(path_to_csv_files,path_to_csv_schema_file, db_output_dir):
    # Main execution flow
    files_structure = discover_csv_files_and_structure(path_to_csv_files)
    relationships, column_types = read_csv_schema_from_excel(path_to_csv_schema_file)
    sorted_table_names = sort_tables_by_dependency(relationships)
    create_database_and_tables(files_structure, sorted_table_names,column_types, db_output_dir = db_output_dir)
    return get_database_schema(path_to_db=db_output_dir)
    