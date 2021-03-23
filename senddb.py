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
    
    d={}
    for i in results:
    	a = i[0]
    	b = i[1]
    	d[a] = b
    	
    print(d)
    r=json.dumps(d)
    channel.basic_publish(exchange='', routing_key='right' , body=r)
    print("[x] Sent 'Hello World!'")
    

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='25.121.196.54',port=5672, credentials=credentials))
    
channel = connection.channel()

channel.queue_declare(queue='right')
channel.basic_consume('right', callback, auto_ack=True)
channel.start_consuming()
