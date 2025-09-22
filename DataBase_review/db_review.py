import psycopg2
import os

# Replace with your actual credentials
connection = psycopg2.connect(
    host="localhost",     # or IP of your DB server
    port="5432",          # default port
    database="bony",      # name of your database
    user="postgres",      # your username
    password=""  # your password
)

tables_with_data = list()
cursor = connection.cursor()

# Test query
cursor.execute("SELECT version();")
record = cursor.fetchone()
# print("You are connected to:", record)

# Query to get all table names in the current database
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE';
""")

tables = [row[0] for row in cursor.fetchall()]
# print("Tables in the database:", tables)

for table in tables:
    query = f"select count(*) as registros from {table}"
    cursor.execute(query)
    data_table = cursor.fetchall()
    records = data_table[0][0]
    if (records != 0):
        tables_with_data.append(table)


#with open("tables_data.txt", "w") as file:
#    for table in tables_with_data:
#        file.write(f"{table}\n")

cursor.execute("""
    SELECT m.model AS table_name,
       f.name AS column_name,
       f.ttype AS field_type,
       f.field_description AS description
FROM ir_model_fields f
JOIN ir_model m ON f.model_id = m.id
ORDER BY m.model, f.name;
""")

table_info = cursor.fetchall()
table_info = table_info[0:10]
print(table_info)

cursor.close()
connection.close()

