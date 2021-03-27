import pika
import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ubuntu",
  database= "testdb"
)
def callback(ch, method, properties, body):
    info = json.loads(body)
    mycursor = mydb.cursor()
    mycursor.execute(info)
    result= mycursor.fetchall()
    
    d1={}
    for i in results:
        a = i[0]
        b = i[1]
        d[a] = b
    
    d2={}
    d2["query"] = d1
    d2["reason"] = "results"

    r=json.dumps(d2)
    channel.basic_publish(exchange='', routing_key='hello' , body=r)
    print("[x] Sent 'Hello World!'")
    

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='25.121.196.54',port=5672, credentials=credentials))
    
channel = connection.channel()

channel.queue_declare(queue='database')
channel.basic_consume('database', callback, auto_ack=True)
print("Listening on queue: Database")
channel.start_consuming()
