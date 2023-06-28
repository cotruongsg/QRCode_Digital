import psycopg2

# Establish a connection to the database
connection = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="your_host", port="your_port")
cursor = connection.cursor()

# Read the binary data from the image file
with open('path_to_image_file.jpg', 'rb') as file:
    image_data = file.read()

# Insert the image data into the database using a parameterized query
cursor.execute("INSERT INTO your_table (image_column) VALUES (%s)", (psycopg2.Binary(image_data),))

# Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()
