from flask import Flask, request, url_for
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials
import os

TOPIC_ID = "1" # Topic Id
IMAGES_FOLDER = "images"

cred = credentials.Certificate("mobcom-f1a53-firebase-adminsdk-2dkvm-45db9d6f3c.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__, static_folder="images")

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
    senderUUID = input_json["senderUUID"]
    message = messaging.Message(
        notification = messaging.Notification(
            title = 'New Message Received',
            body = messageInput,
        ),
        data = {"time" : timeInput, "senderUUID" : senderUUID, "body": messageInput},
        topic= TOPIC_ID
    )
    send = messaging.send(message)
    print(send)
    return {"response": send, "status" : "success"}

@app.route('/send-image', methods=["POST"])
def sendImage():
    imageFile = request.files['image']
    path = os.path.join(IMAGES_FOLDER, imageFile.filename)
    imageUrl = "http://" + request.host + url_for('static', filename=imageFile.filename)
    print(imageUrl)
    imageFile.save(path)

    senderUUID = request.form.get('senderUUID')
    timeInput = request.form.get('time')
    message = messaging.Message(
        notification = messaging.Notification(
            title = 'New Message Received',
            image = imageUrl,
            body = "image"
        ),
        data = {"time" : timeInput, "senderUUID" : senderUUID, "body": "image", "image": imageUrl},
        topic= TOPIC_ID
    )

    send = messaging.send(message)
    print(send)
    return {"response": send, "status" : "success"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
