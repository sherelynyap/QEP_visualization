import json
import sys
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
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}")
            result = cursor.fetchall()[0][0][0]
    except(Exception, psycopg2.DatabaseError) as error:    
            # Check how to seperate errors
            print(error)
            return "error"
    
    root = build_tree(connection, result['Plan'], block_id_per_table)
    planning_time = result['Planning Time']
    execution_time = result['Execution Time']

    with connection.cursor() as cursor:
        cursor.execute(f"SHOW block_size")
        buffer_size = cursor.fetchall()[0][0]

    for key in block_id_per_table:
        block_id_per_table[key] = sorted(block_id_per_table[key])

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
    ## Support scanning same table for multiple times
    if (plan["Node Type"] in VALID_SCAN):
        table_name = plan["Relation Name"]
        
        if (table_name not in block_id_dict):
            block_id_dict[table_name] = set()

        if (plan["Node Type"] == "Index Only Scan"):
            pass
        elif (plan["Node Type"] == "Seq Scan"):
            block_id_dict[table_name].update(retrieve_block_id(connection, table_name))
        elif (plan["Node Type"] == "Index Scan"):
            ## need to do this? ==> check nl join, only inner
            block_id_dict[table_name].update(retrieve_block_id(connection, table_name, plan["Index Cond"] if ("Index Cond" in plan) else None))
        elif (plan["Node Type"] == "Bitmap Heap Scan"):
            block_id_dict[table_name].update(retrieve_block_id(connection, table_name, plan["Recheck Cond"] if ("Recheck Cond" in plan) else None))
        elif (plan["Node Type"] == "Tid Scan"):
            block_id_dict[table_name].update(retrieve_block_id(connection, table_name, plan["TID Cond"] if ("TID Cond" in plan) else None))
    
    ## Annotation here
    root.annotations = annotate_node(plan)

    ## If parallel aware, append Parallel to the front of Node Type
    if ("Parallel Aware" in plan and plan["Parallel Aware"]):
        plan["Node Type"] = "Parallel " + plan["Node Type"]

    ## Add table name to next line for scan
    if ("Relation Name" in plan):
        plan["Node Type"] = plan["Node Type"] + "\n(" + plan["Relation Name"] + ")"

    ## Add elements in plan to attributes   
    for key, val in plan.items():
        if (key != "Plans"):
            root.attributes[key] = val
    
    ## If not leaf node, recursively call the function to build the tree
    if "Plans" in plan:
        for child_plan in plan["Plans"]:
            # child_node = build_tree(child_plan)
            child_node = build_tree(connection, child_plan, block_id_dict)
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
 
    ## Explanation for join type
    if ("Join Type" in plan):
        annotations += "{} join is performed.".format(plan["Join Type"])

    ## Explanation for join condition
    if ("Hash Cond" in plan):
        annotations += " Hash condition is {}.\n".format(plan["Hash Cond"])
    elif ("Merge Cond" in plan):
        annotations += " Merge condition is {}.\n".format(plan["Merge Cond"])
    else:
        annotations += "\n"

    ## Explanation for est cost
    annotations += "The startup cost for this node is estimated to be {} while the total cost (including cost from children nodes) is estimated to be {}.\n"\
        .format(plan["Startup Cost"], plan["Total Cost"])
    
    ## Explanation for actual time
    annotations += "In the actual run, this node took {} ms to start up and took {} ms to finish (including time calculated in children nodes).\n"\
        .format(plan["Actual Startup Time"], plan["Actual Total Time"])

    ## Explanation for buffer ==> how many saved


    ## Explanation for rows returned, errors and how many removed by filter
    error = abs (plan["Actual Rows"] - plan["Plan Rows"]) / plan["Plan Rows"]
    annotations += "The rows to be produced is estimated to be {}, while in the actual run {} rows are produced. The error of estimation is {:.2f}%"\
        .format(plan["Plan Rows"], plan["Actual Rows"], error)

    if ("Rows Removed by Filter" in plan):
        annotations += "{} rows are removed by filtering. \n".format(plan["Rows Removed by Filter"])
    else:
        annotations += "\n"
                
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

    return block_id_set

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
