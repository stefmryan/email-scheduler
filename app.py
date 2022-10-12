from flask import Flask, request, Response, render_template
from flask_mail import Mail, Message
from flask_cors import CORS
from threading import Thread
import time
import random
import re
import os
import json


app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

env = os.environ.get('env')

emailArray = []

CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return Response(status=500, mimetype='application/json') 

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/post-email",  methods=["POST"])
def post_email():
    emailToSend = request.get_json(force=True).get('email')

    #check that email is valid
    isValid = validate_email(emailToSend)
    if not isValid:
        response_obj = {
            "message": "Not a valid email",
        }
        return Response(json.dumps(response_obj), status=400, mimetype='application/json')
        
    #check that email is not in list
    if emailToSend in emailArray:
        response_obj = {
            "message": "Email already in use",
        }
        return Response(json.dumps(response_obj), status=400, mimetype='application/json')
        
    emailArray.append(emailToSend)
    
    #send emails to each element in emailArray
    for idx, email in enumerate(emailArray):
        
        t = Thread(target=send_email, args=(email,))
        t.start()

        del emailArray[idx]
        
 
    response_obj = {
        "email": emailToSend,
    }

    return Response(json.dumps(response_obj), status=200, mimetype='application/json')

def send_email(email):
    sentEmails = 0
    sender = os.environ.get('MAIL_USERNAME')

    messageDict = {"1":"Apples are Red", "2": "Bananas are yellow", "3":"Carrots are orange", "4": "Dogs are canines", "5": "Elephants travel in packs", "6": "Flask is a python framework", "7": "Grapes grow on vines", "8": "Have a good day!", "9": "I have chosen each first character in this list to be different.", "10" : "Just in time"}
    
    #while sentEmails is less than 10, send new email with unique message
    with app.app_context():
        while(sentEmails < 10):
            message = random.choice(list(messageDict.items()))
        
            msg = Message(f'Email from {sender}', sender = sender, recipients = [email])
            msg.body = message[1]
            mail.send(msg)
        
            # remove message from dictionary 
            del messageDict[message[0]]

            sentEmails = sentEmails + 1
            time.sleep(60)
    return

# validating email string with regex
def validate_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(pat,email)

if __name__ == '__main__':
   app.run(debug = True)