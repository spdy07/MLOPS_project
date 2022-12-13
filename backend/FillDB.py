import pandas as pd
import mysql.connector

# Read the CSV file
df = pd.read_csv('/Users/youennloie/PycharmProjects/MLOPS_project/datas/Country-data.csv')

# Extract the data from the DataFrame
data = df.to_dict('records')

# Connect to the database
cnx = mysql.connector.connect(
    host='db',
    user='root',
    password='password',
    database='mydb'
)

# Insert the data into the database
cursor = cnx.cursor()
for row in data:
    cursor.execute(
        "INSERT INTO mytable (field1, field2, field3) VALUES (%s, %s, %s)",
        (row['field1'], row['field2'], row['field3'])
    )

# Close the connection
cnx.close()
