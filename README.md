# Solius Reader
Get temperatures from your Solius controller and let AWS push the readings over mqtt

Based on: https://github.com/jhhbe/hassio-addons/tree/master/meter_reader

## Config
upd_interval: value in seconds to be used as interval between data refreshes.

url: where to find the picture of your meter (webcam)

user: basic authentication for cam

password: basic authentication for cam

aws_access_key_id, aws_secret_access_key, region: see link on how to set up an AWS account. Did not really see how to get your region, I use "us-east-2" (https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)

mqtt_host, mqtt_port, mqtt_user, mqtt_pwd: find and get access to your MQTT server

mqtt_topic: topic on which meter reading gets published

verbose: show internal messages
