from flask import Flask, request
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

TOPIC_ID = "1" # Topic Id

cred = credentials.Certificate("mobcom-f1a53-firebase-adminsdk-2dkvm-45db9d6f3c.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/register-token', methods=["POST"])
def registerToken():
    global TOPIC_ID
    input_json = request.get_json(force=True)
    token = input_json["token"]
    subscribe = messaging.subscribe_to_topic(token, TOPIC_ID)
    print(subscribe)
    return {"response": "device successfully registered", "status": "success"}

@app.route('/send-message', methods=["POST"])
def sendMessage():
    input_json = request.get_json(force=True)
    messageInput = input_json["message"]
    timeInput = input_json["time"]
    image = input_json["imagebase64"]
    message = messaging.Message(
        notification = messaging.Notification(
            title = 'New Message Received',
            body = messageInput,
        ),
        data = {"time" : timeInput},
        topic= TOPIC_ID
    )
    send = messaging.send(message)
    print(send)
    return {"response": send, "status" : "success"}

if __name__ == "__main__":
    app.run(port=8080, debug=True)
