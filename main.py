import os
import random
import sched
import time

from paho.mqtt.client import MQTTMessage

from mqtt_controller import MqttController, MqttConfig
import requests


mqtt_c: MqttController | None = None
ltse_cache = dict()
with open('res/insert_ts.ru', 'r') as fp:
    sparql_insert_ts = fp.read()


def main():
    global mqtt_c

    def normalize_endpoint(endpoint: str) -> str:
        if endpoint.endswith('/'):
            return endpoint[:-1]
        return endpoint

    csc_endpoint_config = normalize_endpoint(os.getenv('GLUE_CSC_ENDPOINT_CONFIG'))
    csc_endpoint_workers = normalize_endpoint(os.getenv('GLUE_CSC_ENDPOINT_WORKERS'))
    ltse_postgrest_endpoint = normalize_endpoint(os.getenv('GLUE_LTSE_POSTGREST_ENDPOINT'))
    poll_interval = int(os.getenv('GLUE_POLL_INTERVAL'))
    print('Connecting to the MQTT broker')
    mqtt_config = MqttConfig(
        client_id='csc-glue-' + str(random.randint(0, 100000)),
        broker_address=os.getenv('GLUE_MQTT_HOST'),
        broker_port=int(os.getenv('GLUE_MQTT_PORT')),
        topics={
            'rq-worker': 'assist-iot/config/worker',
            'rq-worker-device': 'assist-iot/config/worker-device',
        }
    )
    print('Starting the scheduler')
    scheduler = sched.scheduler(time.time, time.sleep)

    def loop_workers():
        try:
            workers = get_ltse_table(ltse_postgrest_endpoint, 'worker')
            annotate_ltse_table('rq-worker', workers)
        except Exception as e:
            print('Error in loop_workers')
            print(e)
        scheduler.enter(poll_interval, 1, loop_workers)

    def loop_config():
        try:
            w_device = get_ltse_table(ltse_postgrest_endpoint, 'worker_device')
            annotate_ltse_table('rq-worker-device', w_device)
        except Exception as e:
            print('Error in loop_config')
            print(e)
        scheduler.enter(poll_interval, 1, loop_config)

    def on_message(client, userdata, m: MQTTMessage):
        if m.topic.endswith('/worker'):
            print('Received worker config')
            update_csc(csc_endpoint_workers, m.payload)
        elif m.topic.endswith('/worker-device'):
            print('Received worker-device config')
            update_csc(csc_endpoint_config, m.payload)
        else:
            print('Received unknown semantic config')
            print(m.topic)

    mqtt_c = MqttController(mqtt_config)
    mqtt_c.client.subscribe('assist-iot/semantic/config/+')
    mqtt_c.client.on_message = on_message

    scheduler.enter(0, 1, loop_workers)
    scheduler.enter(0, 1, loop_config)
    scheduler.run()


def get_ltse_table(endpoint: str, name: str) -> str | None:
    r = requests.get(endpoint + '/' + name)
    if r.status_code != 200:
        print(f'LTSE error: {r.status_code}')
        print(r.text)
        return None
    if name in ltse_cache and ltse_cache[name] == r.text:
        return None
    ltse_cache[name] = r.text
    return r.text


def annotate_ltse_table(topic_name: str, table: str | None):
    if table is None:
        return None
    print('Sending data to be annotated: ' + topic_name)
    mqtt_c.send_message(table, topic_name)


def update_csc(endpoint: str, data: bytes | None):
    if data is None:
        return
    r_delete = requests.delete(endpoint + '?default')
    if r_delete.status_code >= 300:
        print(f'CSC delete error for endpoint {endpoint}: {r_delete.status_code}')
        print(r_delete.text)
        return

    r_post = requests.post(
        endpoint + '?default',
        data=data,
        headers={'Content-Type': 'text/turtle'}
    )
    if r_post.status_code >= 300:
        print(f'CSC post error for endpoint {endpoint}: {r_post.status_code}')
        print(r_post.text)
        return
    r_post_ts = requests.post(
        endpoint,
        data=sparql_insert_ts,
        headers={'Content-Type': 'application/sparql-update'}
    )
    if r_post_ts.status_code >= 300:
        print(f'CSC ts insert error for endpoint {endpoint}: {r_post_ts.status_code}')
        print(r_post_ts.text)
        return
    print('Updated ' + endpoint)


if __name__ == "__main__":
    main()
