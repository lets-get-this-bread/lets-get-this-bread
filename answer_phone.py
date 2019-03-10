import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Dial, Say, Record
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
client = Client(account_sid, auth_token)

forbidden_states = ["CA", "CT", "FL", "IL", "MD", "MA", "MT", "NH", "PA", "WA"]

@app.route("/sms", methods=['GET','POST'])
def reply():
    if request.values.get("FromState", None) in forbidden_states:
        resp = MessagingResponse()
        resp.message("We're sorry, but we cannot bake any bread in your area!")
        return str(resp)
    else:
        number = request.values.get("From", None)
        call = client.calls.create(
                        url='http://hackru.plup.club:5000/call_xml',
                        to=number,
                        from_='+16092566938',
                        record=True,
                        recording_channels='dual',
                    )
        return ""

@app.route("/call_xml", methods=['GET','POST'])
def call_xml():
    resp = VoiceResponse()
    resp.say("Thank you for calling Ivylands Bakery. Please hold until" +
        "  the next representative is available.", voice='alice')
    resp.play('https://my.mixtape.moe/qhqkqa.mp3') # 4minhold
    return str(resp)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    call_sid = request.values.get("CallSid", None)
    """Respond to incoming phone calls and mention the caller's city"""
    if request.values.get("FromState", None) in forbidden_states:
        resp = VoiceResponse()
        resp.say("We're sorry, but we cannot bake any bread in your area.")
        resp.hangup()
        return str(resp)
    else:
        resp = VoiceResponse()
        resp.say("Thank you for calling Ivylands Bakery. Please hold until the next representative is available.")
        resp.record()
        return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
