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
def home():
    return render_template('base.html')

@app.route("/post-email",  methods=["POST"])
def post_email():
    emailToSend = request.get_json(force=True).get('email')

    #check that email is valid
    isValid = validate_email(emailToSend)
    if not isValid:
        response_obj = {
            "message": "not a valid email",
        }
        return Response(json.dumps(response_obj), status=400, mimetype='application/json')
        
    #check that email is not in list
    if emailToSend in emailArray:
        response_obj = {
            "message": "email already in use",
        }
        return Response(json.dumps(response_obj), status=400, mimetype='application/json')
        
    emailArray.append(emailToSend)
    '''
        #send emails to each element in emailArray
        for idx, email in enumerate(emailArray):
            
            t = Thread(target=send_email, args=(email,))
            t.start()
 '''
    response_obj = {
        "email": emailToSend,
    }
    return Response(json.dumps(response_obj), status=200, mimetype='application/json')

def send_email(email):
    print("In send email func")  
    sentEmails = 0
    sender = os.environ.get('MAIL_USERNAME')

    messageDict = {"1":"A", "2": "B", "3":"C", "4": "D", "5": "E", "6": "F", "7": "G", "8": "H", "9": "I", "10" : "J"}
    with app.app_context():
        while(sentEmails < 10):
            #grab random message
            message = random.choice(list(messageDict.items()))
        
            print("MESSAGE VALUE: " + message[1])
            msg = Message(f'Email from {sender}', sender = sender, recipients = [email])
            msg.body = message[1]
            mail.send(msg)
        
            # remove message from dictionary 
            del messageDict[message[0]]
            print("LENGTH OF MESSAGEDICT: " + str(len(messageDict)))
            sentEmails = sentEmails + 1
            time.sleep(60)
    print(f"DONE WITH EMAILS")
    return

# validating email string with regex
def validate_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(pat,email)

if __name__ == '__main__':
   app.run(debug = True)