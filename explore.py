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

# !!!!!!!!!!!!!!!
# Error handling !!!
# !!!!!!!!!!!!!!!

######## Functions for retrieving by blocks and return disk block accessed #######

# Get the number of blocks accessed in each scan
## Return the sorted list of ctid
def retrieve_ctid(connection, table_name, scan_type, index_condition = None):

    ### bitmap index scan??
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

# Class representing QEP tree node
class Node():
    def __init__(self) -> None:
        self.children = []
        self.attributes = {}
        self.annotations = ""

# Function to build QEP tree
def build_tree(plan):
    root = Node()
    
    for key, val in plan.items():
        if key != "Plans":
            root.attributes[key] = val
    
    ### If not leaf node
    if "Plans" in plan:
        for child_plan in plan["Plans"]:
            child_node = build_tree(child_plan)
            root.children.append(child_node)

    return root

# Retrieve QEP from database
def get_qep_info(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}")
        result = cursor.fetchall()[0][0][0]

    root = build_tree(result['Plan'])
    ### possibly scan leaf node here?
    planning_time = result['Planning Time']
    execution_time = result['Execution Time']

    with connection.cursor() as cursor:
        cursor.execute(f"SHOW block_size")
        buffer_size = cursor.fetchall()[0][0]

    return root, planning_time, execution_time, buffer_size

NODE_EXPLANATION = {
    'Seq Scan': 'Scans the entire relation as stored on disk.',
    'Index Scan': 'Uses index to find all matching entries, and fetches the corresponding table data.',
    'Bitmap Index Scan': 'Instead of producing the rows directly, the bitmap index scan constructs a bitmap of potential row locations. It feeds this data to a parent Bitmap Heap Scan.',
    'Index Only Scan': 'Finds relevant records based on an Index. Performs a single read operation from the index and does not read from the corresponding table.',
    'Hash Join': 'Joins two record sets by hashing one of them.',
    'Aggregate': 'Groups records together based on a key or an aggregate function.',
    'Limit': 'Returns a specified number of rows from a record set.',
    'Sort': 'Sorts a record set based on the specified sort key.',
    'Nested Loop': 'Merges two record sets by looping through every record in the first set and trying to find a match in the second set.',
    'Merge Join': 'Merges two record sets by first sorting them on a join key.',
    'Hash': 'Generates a hash table from the records in the input recordset.',
    'CTE_Scan': 'Performs sequential scan of a Common Table Expression (CTE) query results.',
    'Bitmap Heap Scan': 'Searches through the pages returned by the Bitmap Index Scan for relevant rows.'
}