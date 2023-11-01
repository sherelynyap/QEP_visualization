import psycopg2
import sqlparse
import ast

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
    return parsed

# !!!!!!!!!!!!!!!
# Error handling !!!
# !!!!!!!!!!!!!!!

# Class representing QEP tree node
class Node():
    def __init__(self) -> None:
        self.children = []
        self.attributes = {}
        self.annotations = ""

# Retrieve QEP from database
def get_qep_info(connection, query):
    result_dict = {}

    block_id_per_table = {}

    with connection.cursor() as cursor:
        cursor.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}")
        result = cursor.fetchall()[0][0][0]

    root = build_tree(connection, result['Plan'], block_id_per_table)
    planning_time = result['Planning Time']
    execution_time = result['Execution Time']

    with connection.cursor() as cursor:
        cursor.execute(f"SHOW block_size")
        buffer_size = cursor.fetchall()[0][0]

    result_dict['root'] = root
    result_dict['planning_time'] = planning_time
    result_dict['execution_time'] = execution_time
    result_dict['buffer_size'] = buffer_size
    result_dict['block_id_per_table'] = block_id_per_table

    return result_dict

# Function to build QEP tree
def build_tree(connection, plan, block_id_dict):
    root = Node()

    ## Check if disk block access involved
    if (plan["Node Type"] in VALID_SCAN):
        table_name = plan["Relation Name"]

        if (plan["Node Type"] == "Index Only Scan"):
            block_id_dict[table_name] = []
        elif (plan["Node Type"] == "Seq Scan"):
            block_id_dict[table_name] = retrieve_block_id(connection, table_name)
        elif (plan["Node Type"] == "Index Scan"):
            block_id_dict[table_name] = retrieve_block_id(connection, table_name, plan["Index Cond"] if ("Index Cond" in plan) else None)
        elif (plan["Node Type"] == "Bitmap Heap Scan"):
            block_id_dict[table_name] = retrieve_block_id(connection, table_name, plan["Recheck Cond"] if ("Recheck Cond" in plan) else None)
        elif (plan["Node Type"] == "Tid Scan"):
            block_id_dict[table_name] = retrieve_block_id(connection, table_name, plan["TID Cond"] if ("TID Cond" in plan) else None)
    
    ## Annotation here
    root.annotations = annotate_node(plan)

    ## If parallel aware, append Parallel to the front of Node Type
    if ("Parallel Aware" in plan and plan["Parallel Aware"]):
        plan["Node Type"] = "Parallel " + plan["Node Type"]

    ## Add elements in plan to attributes   
    for key, val in plan.items():
        if (key != "Plans"):
            root.attributes[key] = val
    
    ## If not leaf node, recursively call the function to build the tree
    if "Plans" in plan:
        for child_plan in plan["Plans"]:
            child_node = build_tree(child_plan)
            root.children.append(child_node)

    return root

# Function to annotate node
def annotate_node(plan):
    annotations = ""

    ## Explanation for node type
    if (plan["Node Type"] in NODE_EXPLANATION):
        annotations += NODE_EXPLANATION[plan["Node Type"]] + "\n"
    else:
        annotations += "Performs \"" + plan["Node Type"] + "\"operation .\n"
 
    ## Explanation for join cond, join type
    ## Explanation for buffer ==> how many saved   
    ## Explanation for cost (est, actual, error); actual vs est ==> err
    ## Explanation for rows returned (only actual), how many removed by filter
                
    return annotations

# Get the number of blocks accessed in each scan
## Return the sorted list of block id
def retrieve_block_id(connection, table_name, condition = None):
    if (condition):
        query = f"SELECT ctid, * FROM {table_name} WHERE {condition}"
    else:
        query = f"SELECT ctid, * FROM {table_name}"

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    block_id_set = set()
    for tuple in result:
        ctid = ast.literal_eval(tuple[0])
        block_id = ctid[0]
        block_id_set.add(block_id)

    block_id_list = sorted(block_id_set)

    return block_id_list

# Get the block content based on block id
## Return the attribute name and the rows
def execute_block_query(connection, table_name, block_id):
    query = f"SELECT * FROM {table_name} WHERE (ctid::text::point)[0] = {block_id}"

    with connection.cursor() as cursor:
        cursor.execute(query)
        schema = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

    return schema, result

VALID_SCAN = {'Seq Scan', 'Index Scan', 'Bitmap Heap Scan', 'Index Only Scan', 'Tid Scan'}

VALID_SCAN_CONDITION = {}

NODE_EXPLANATION = {
    'Seq Scan': 'Scans the entire relation as stored on disk.',
    'Index Scan': 'Uses index to find all matching entries, and fetches the corresponding table data.',
    'Index Only Scan': 'Finds relevant records based on an Index. Performs a single read operation from the index and does not read from the corresponding table.',
    'Bitmap Index Scan': 'Instead of producing the rows directly, the bitmap index scan constructs a bitmap of potential row locations. It feeds this data to a parent Bitmap Heap Scan.',
    'Bitmap Heap Scan': 'Searches through the pages returned by the Bitmap Index Scan for relevant rows.',
    'CTE_Scan': 'Performs sequential scan of a Common Table Expression (CTE) query results.',
    'Tid Scan': 'Performs scan of a table by TID. This is fast, but unreliable long-term.',
    'Hash Join': 'Joins two record sets by hashing one of them.',
    'Aggregate': 'Groups records together based on a key or an aggregate function.',
    'Limit': 'Returns a specified number of rows from a record set.',
    'Sort': 'Sorts a record set based on the specified sort key.',
    'Nested Loop': 'Merges two record sets by looping through every record in the first set and trying to find a match in the second set.',
    'Merge Join': 'Merges two record sets by first sorting them on a join key.',
    'Hash': 'Generates a hash table from the records in the input recordset.',
    'Unique': 'Removes duplicates from the table.',
    'Gather': 'Combines the output of child nodes, which are executed by parallel workers. Does not make any guarantee about ordering.',
    'Gather Merge': 'Combines the output of child nodes, which are executed by parallel workers. Preserves sort order.',
    'Append': 'Combine the results of the child operations.',
    'Materialize': 'Stores the result of the child operation in memory, to allow fast, repeated access to it by parent operations.',
}