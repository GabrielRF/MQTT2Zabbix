import paho.mqtt.client as mqtt
from pyzabbix import ZabbixMetric, ZabbixSender

ZabbixServer=
ZabbixPort=
MqttServer=
MqttPort=
MqttUser=
MqttPassword=

def on_connect(client, userdata, flags, rc):
    client.subscribe("+")

def on_message(client, userdata, msg):
    print(msg.topic+" -  "+str(msg.payload.decode('utf-8')))

    packet = [
        ZabbixMetric(str(msg.topic).split('.')[0], str(msg.topic).split('.')[1], str(msg.payload.decode('utf-8'))),
    ]

    result = ZabbixSender(zabbix_server=ZabbixServer, zabbix_port=ZabbixPort, use_config=None, chunk_size=250).send(packet)
    print(result)


mqttclient = mqtt.Client(client_id='ZabbixServer')
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message

mqttclient.username_pw_set(MqttUser, password=MqttPassword)

mqttclient.connect(MqttServer)

mqttclient.loop_forever()
