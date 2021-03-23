import pika
import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ubuntu",
  database= "testdb"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM test")

results=mycursor.fetchall()

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='25.121.196.54',port=5672, credentials=credentials))
    
channel = connection.channel()

channel.queue_declare(queue='hello')
d={}
for i in results:
    a = i[0]
    b = i[1]
    d[a] = b 
r=json.dumps(d)
channel.basic_publish(exchange='', routing_key='hello', body=r)
print(" [x] Sent 'Hello World!'")
connection.close()
