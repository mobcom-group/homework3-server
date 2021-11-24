from flask import Flask, request
import requests

import json
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("mobcom-f1a53-firebase-adminsdk-2dkvm-45db9d6f3c.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
tokenPhone2 = ""
tokenPhone1 = ""
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/phone1/registration-message', methods=["POST"])
def registerTokenPhone1():
    global tokenPhone1
    input_json = request.get_json(force=True)
    tokenPhone1 = input_json["token"]
    return {"status": "Success"}

@app.route('/phone2/registration-message', methods=["POST"])
def registerTokenPhone2():
    global tokenPhone2
    input_json = request.get_json(force=True)
    tokenPhone2 = input_json["token"]
    return {"status": "Success"}

@app.route('/phone1/send-message', methods=["POST"])
def sendMessagePhone1():
    global tokenPhone2
    input_json = request.get_json(force=True)
    messageInput = input_json["message"]
    timeInput = input_json["time"]
    image = input_json["imagebase64"]
    message = messaging.Message(
    data={
        'message': messageInput,
        'time': timeInput,
    },
    token= tokenPhone2,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
    return {"response": response, "status" : "success"}  

@app.route('/phone2/send-message', methods=["POST"])
def sendMessagePhone2():
    global tokenPhone1
    input_json = request.get_json(force=True)
    messageInput = input_json["message"]
    timeInput = input_json["time"]
    image = input_json["imagebase64"]
    message = messaging.Message(
    data={
        'message': messageInput,
        'time': timeInput,
    },
    token= tokenPhone1,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
    return {"response": response, "status" : "success"}

if __name__ == "__main__":
    app.run(port=8080, debug=True)