import pika
from pika.exchange_type import ExchangeType
from flask import Flask, request, jsonify,render_template,url_for,redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.flask_db

port = 3000

@app.route('/')
def home():
    return "home"

@app.route('/<cmd>', methods=["GET","POST"])

def process(cmd):
    cmd = cmd.split(":")
    title = cmd[0]
    message = cmd[1]
    print(title, message)
    collection = db[title]
    post = {'message':message}
    collection.insert_one(post)
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='request-queue')
    channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

    channel.basic_publish(exchange='topic', routing_key=title,body=message)

    print(f'sent message: {message}')
    connection.close()
    
    return "Published"


if __name__ == '__main__':
    app.run(port=port,
            debug=True)