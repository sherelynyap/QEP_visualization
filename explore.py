import psycopg2
import sqlparse

# Explanation for function
def connect_database(host = "localhost", database = "postgres", user = "postgres", password = "password"):
    connection = psycopg2.connect(
        host = host,
        database = database,
        user = user,
        password = password
    )

    return connection

# Explanation for function
def parse_sql(query):
    parsed = sqlparse.parse(query)

    # Process the query here
    # eg: parsed = parsed[0]
    return parsed

# !!!
# !!! Error handling
# !!!

######## Functions for retrieving by blocks and return disk block accessed #######

# Get the number of blocks accessed in each scan
## Return the sorted list of ctid
def retrieve_ctid(connection, table_name, scan_type, index_condition = None):
    if (scan_type.startswith("Index")):
        query = f"SELECT ctid, * FROM {table_name} WHERE {index_condition}"
    else:
        query = f"SELECT ctid, * FROM {table_name}"

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall

    ctid_set = set()
    for tuple in result:
        ctid_set.add(tuple[0])

    ctid_list = sorted(ctid_set)

    return ctid_list

# Fetch the block content based on ctid
## Return the list of column name and list of result, in tuple
def execute_block_query(connection, table_name, ctid):
    query = f"SELECT * FROM {table_name} WHERE (ctid::text::point)[0] = {ctid}"

    with connection.cursor() as cursor:
        cursor.execute(query)
        schema = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

    return schema, result

######## End of Functions for retrieving by blocks and return disk block accessed #######

#
def get_qep_info(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}")
        result = cursor.fetchall()[0][0][0]['Plan']
    
    #maybe get json, loop through, convert matched using dict, then return
    return result