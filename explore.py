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

# idea: parse sql, add cid, then exec, then return
## how to split the returned result should be decided by interface side
## to check: is the header passed in as well

# idea: execute query WHERE cid = ... (id that passed in)
######## End of Functions for retrieving by blocks and return disk block accessed #######

######## Passing whole result related to QEP might be inefficient
########### Can consider to make it as a menu, and I can make changes accordingly on my side if yall want
########### Also can decide if yall want to add those explanation on my side or on interface side, i.e. transfer to Natural language
def get_qep_info(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(f"EXPLAIN ??? {query}")
        result = cursor.fetchall()[0][0][0]['Plan']

    return result