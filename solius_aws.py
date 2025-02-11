import boto3
import paho.mqtt.client as mqtt
import requests
import json
import time
import os
import threading


config_json = json.loads(open("/data/options.json").read())
path = "/root/.aws"

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

f = open("/root/.aws/credentials", "w")
f.write("[default]")
f.write("\n")
f.write("aws_access_key_id = " + config_json["aws_access_key_id"])
f.write("\n")
f.write("aws_secret_access_key = " + config_json["aws_secret_access_key"])
f.close()
f = open("/root/.aws/config", "w")
f.write("[default]")
f.write("\n")
f.write("region = " + config_json["region"])
f.close()

awsclient = boto3.client('rekognition')
#imagefile = "/config/www/meter.jpg"
imagefile = "/root/meter.jpg"

verbose = config_json["verbose"]  > 0

def processImage():
    # get image in binary format
    r = requests.get(config_json["url"], auth=(config_json["user"], config_json["password"]))

    # AWS detect text
    awsresponse = awsclient.detect_text(Image={'Bytes': r.content}, Filters={'WordFilter': {'MinConfidence': 90}})
#    awsresponse = awsclient.detect_text(Image={'Bytes': r.content})
    itemsfound = (awsresponse['TextDetections'])

    for item in itemsfound:
        text = item['DetectedText'].strip()

        if item['Type'] == 'LINE' and type(text) is str and len(text) > 3:
            if verbose:
                print("-----------")
                print("Id: ", item['Id'])
                print("Text: ", text)
                #print("Type: ", item['Type'])
                print("Confidence: ", item['Confidence'])
                #if item['Type'] != 'LINE':
                #    print("ParentId: ", item['ParentId'])

            t = text[:2]

            if t == "T1" or t == "T2" or t == "T3":
                text = text[2:].lstrip()
                dot = text.find(".")

                if dot == -1:
                    if verbose:
                        print("Text with no dot, discard")
                    continue

                if verbose:
                    print("Trying conversion to float of: ", text)

                value = 0.0;
                try:
                    value = float(text)
                    if verbose:
                        print(t, " Value: ", value)

                    try:
                        publishMQTT(t, value)
                    except:
                        print("MQTT Publishing failed")
                except:
                    print("Conversion to float failed")

    if verbose:
        print("-----------")

def connectMQTT():
    def on_connect(client, userdata, flags, rc):
        # For paho-mqtt 2.0.0, you need to add the properties parameter.
        # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            #print("Connected to MQTT Broker!")
            pass
        else:
            print("MQTT Failed to connect, return code %d\n", rc)

    try:
        mqttc = mqtt.Client("solius_reader")
    except:
        mqttc = mqtt.Client(client_id="solius_reader", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(username=config_json["mqtt_user"], password=config_json["mqtt_pwd"])
    mqttc.on_connect = on_connect
    mqttc.connect(config_json["mqtt_host"], config_json["mqtt_port"])
    return mqttc

def publishMQTT(sensor, value):
    mqttc = connectMQTT()

    topic = config_json["mqtt_topic"] + "/sensor/" + sensor + "/state"
    mqttc.publish(topic, value, retain=True)
    mqttc.disconnect()
    if verbose:
        print("MQTT Published: ", value)

def main():
    print("Starting...")

    mqttc = connectMQTT()
    id = '3d6105d309b9'
    topic = "homeassistant/sensor/" + config_json["mqtt_topic"] + "/T1/config"
    value = '{"dev_cla":"temperature","unit_of_meas":"°C","exp_aft":1920,"stat_cla":"measurement",'
    value += '"name":"T1","stat_t":"' + config_json["mqtt_topic"] + '/sensor/T1/state",'
    value += '"uniq_id":"' + config_json["mqtt_topic"] + '_T1","dev":{"ids":"' + id + '",'
    value += '"name":"' + config_json["mqtt_topic"] + '","sw":"solius","mdl":"Meter","mf":"Solius",'
    value += '"cns":[["mac","' + id + '"]]}}'
    mqttc.publish(topic, value, retain=True)

    topic = "homeassistant/sensor/" + config_json["mqtt_topic"] + "/T2/config"
    value = '{"dev_cla":"temperature","unit_of_meas":"°C","exp_aft":1920,"stat_cla":"measurement",'
    value += '"name":"T2","stat_t":"' + config_json["mqtt_topic"] + '/sensor/T2/state",'
    value += '"uniq_id":"' + config_json["mqtt_topic"] + '_T2","dev":{"ids":"' + id + '",'
    value += '"name":"' + config_json["mqtt_topic"] + '","sw":"solius","mdl":"Meter","mf":"Solius",'
    value += '"cns":[["mac","' + id + '"]]}}'
    mqttc.publish(topic, value, retain=True)

    topic = "homeassistant/sensor/" + config_json["mqtt_topic"] + "/T3/config"
    value = '{"dev_cla":"temperature","unit_of_meas":"°C","exp_aft":1920,"stat_cla":"measurement",'
    value += '"name":"T3","stat_t":"' + config_json["mqtt_topic"] + '/sensor/T3/state",'
    value += '"uniq_id":"' + config_json["mqtt_topic"] + '_T3","dev":{"ids":"' + id + '",'
    value += '"name":"' + config_json["mqtt_topic"] + '","sw":"solius","mdl":"Meter","mf":"Solius",'
    value += '"cns":[["mac","' + id + '"]]}}'
    mqttc.publish(topic, value, retain=True)

    mqttc.disconnect()

    while True:
        thread = threading.Thread(target=processImage)
        thread.start()
        #thread.join()
        time.sleep(config_json["upd_interval"])

if __name__ == '__main__':
    main()

