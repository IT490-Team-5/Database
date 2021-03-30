import pika
import mysql.connector
import json
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ubuntu",
  database= "testdb"
)
def callback(ch, method, properties, body):
    info = json.loads(body)
    q = info.get("create") or info.get("login")
    v = info.get("values")
    print(type(v))
    print(info)
    mycursor = mydb.cursor() # Create a cursor object
    results = None
    try:
        mycursor.execute(q, v) # Execute a query
        results = mycursor.fetchall() # Fetch all results from our query (a row). Return None on failure.
    except mysql.connector.errors.IntegrityError:
        print("Tried to insert row which already exists!")

    d2={}
    d2["reason"] = "results"    

    if results is not None:
        d2["query2"] = "success"
        mydb.commit()
    else:
        d2["query2"] = "failure"


    r=json.dumps(d2)
    channel.basic_publish(exchange='', routing_key='hello', body=r)
    print("Received! Relaying results to middle..")
    
try:
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='25.121.196.54',port=5672,virtual_host = "vh1", credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='database')
    channel.basic_consume('database', callback, auto_ack=True)
    print("Listening on queue: Database")
    channel.start_consuming()

except KeyboardInterrupt:
    mydb.close()
    sys.exit(0)
finally:
    try:
        mydb.close()
    except:
        pass
