# solius_reader
Put a webcam in front of your Solius controller and let AWS push the readings over mqtt

## Config
upd_interval: value in seconds to be used as interval between data refreshes.

url: where to find the picture of your meter (webcam) - it will be stored temporarily in folder /config/www

user: basic authentication for cam

password: password to obtain webcam picture

id1: id of the T1 text extraction

id2: id of the T2 text extraction

aws_access_key_id, aws_secret_access_key, region: see link on how to set up an AWS account. Did not really see how to get your region, I use "us-east-2" (https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)

mqtt_host, mqtt_port, mqtt_user, mqtt_pwd: find and get access to your MQTT server

mqtt_topic: topic on which meter reading gets published
