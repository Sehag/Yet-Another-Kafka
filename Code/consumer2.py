import pika
import sys
from pika.exchange_type import ExchangeType
from flask import Flask, request,render_template,url_for,redirect
import  subprocess
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
data = client.flask_db
topic_name = sys.argv[1]
collection = data[topic_name]

def message(ch, method, properties, body):
    body  =  body.decode('utf-8')
    print(body)


if(sys.argv[2]=="--from_beginning"):
    results = collection.find({})
    for x in results:
        print (x['message'])


con = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

chan = con.channel()

chan.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

queue = chan.queue_declare(queue='', exclusive=True)

chan.queue_bind(exchange='topic', queue=queue.method.queue, routing_key="topic1")

chan.basic_consume(queue=queue.method.queue, auto_ack=True,
    on_message_callback=message)

chan.start_consuming()