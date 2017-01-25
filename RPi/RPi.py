
import paho.mqtt.client as paho
import os
import socket
import ssl


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    client.subscribe("#" , 1 )

def on_message(client, userdata, msg):
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))

    if(msg.topic == "ON"):
        os.system("echo on 0 | cec-client -s -d 1")
    elif(msg.topic == "OFF"):
        os.system("echo standby 0 | cec-client -s -d 1")


#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))
#Add Host and missing key names
awshost = ".iot.us-east-1.amazonaws.com"
awsport = 8883
caPath = "aws-iot-rootCA.crt"
certPath = "-certificate.pem"
keyPath = "-private.pem"

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_forever()
