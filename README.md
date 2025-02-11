# Solius Reader
Get temperatures from your Solius controller with a cam

Based on: https://github.com/jhhbe/hassio-addons/tree/master/meter_reader

## Config
upd_interval: interval between data refreshes in seconds

url: cam still image url 

user: cam basic authentication

password: cam basic authentication

aws_access_key_id, aws_secret_access_key
Link on how to set up an AWS account: https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)

region: Don't know your AWS region? Use "us-east-2"

mqtt_host, mqtt_port, mqtt_user, mqtt_pwd: MQTT server and credentials

mqtt_topic: topic to publish (device id)

verbose: show internal messages
