from __future__ import print_function
import datetime
import json
import paho.mqtt.client as paho
import ssl
import socket


def handler(event, context):
    print('Incoming Request: ' + json.dumps(event, separators=(',', ':')))
    if 'session' in event:
        if (event['session']['application']['applicationId'] !=
                "amzn1.ask.skill.fc3ef5d3-f56a-424f-970f-3dbe5f5c411c"):
            raise ValueError("Invalid Application ID")

        if 'request' in event:
            if event['request']['type'] == "LaunchRequest":
                return on_launch(event['request'], event['session'])
            elif event['request']['type'] == "IntentRequest":
                return on_intent(event['request'], event['session'])
            elif event['request']['type'] == "SessionEndedRequest":
                return on_session_ended(event['request'], event['session'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = launch_request
    return Welcome_response(intent, session)


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TVOn":
        return turn_on(intent, session)
    elif intent_name == "TVOff":
        return turn_off(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])


# --------------- Functions that control the skill's behavior ------------------

def turn_on(intent, session):
    card_title = "Welcome"
    should_end_session = True
    speech_output = "TV on"
    reprompt_text = ""

    #Add missing host name and key names
    awshost = "iot.us-east-1.amazonaws.com"
    awsport = 8883
    caPath = "aws-iot-rootCA.crt"
    certPath = "certificate.pem"
    keyPath = "private.pem"
    mqttc = paho.Client()
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
                  tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    mqttc.connect(awshost, awsport, keepalive=60)
    mqttc.loop_start()
    mqttc.publish("ON", None ,  qos=1)
    mqttc.loop_stop()
    mqttc.disconnect()
    # Send response back to the Alexa Voice Skill
    return build_response(build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def turn_off(intent, session):
    card_title = "Welcome"
    should_end_session = True
    speech_output = "TV off"
    reprompt_text = ""

    awshost = "iot.us-east-1.amazonaws.com"
    awsport = 8883
    caPath = "aws-iot-rootCA.crt"
    certPath = "certificate.pem"
    keyPath = "private.pem"
    mqttc = paho.Client()
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
                  tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    mqttc.connect(awshost, awsport, keepalive=60)
    mqttc.loop_start()
    mqttc.publish("OFF" , None, qos=1)

    mqttc.loop_stop()
    mqttc.disconnect()
    # Send response back to the Alexa Voice Skill
    return build_response(build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def Welcome_response(intent, session):
    card_title = "Welcome"
    should_end_session = True

    # Start the real task
    currentTime = datetime.datetime.now()
    if currentTime.hour < 12:
        printTime = "morning"
    elif 12 <= currentTime.hour < 18:
        printTime = "afternoon"
    else:
        printTime = "evening"
    speech_output = "Good " + printTime + ", Say TV on or TV off to turn the TV on or off"
    reprompt_text = ""

    # Send response back to the Alexa Voice Skill
    return build_response(build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': '',
        'response': speechlet_response
    }
