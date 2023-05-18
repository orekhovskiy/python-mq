import json
from dataclasses import asdict

import pika
import pika.exceptions
import config
from config import config
from schemas.epoch import Epoch
from schemas.metrics import Metrics
from schemas.status import Status


class MQService:
    def __init__(self, host: str, port: int, username: str, password: str):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host, port, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        try:
            self.command_channel = self.connection.channel()
            self.status_channel = self.connection.channel()
            self.epoch_channel = self.connection.channel()
            self.metrics_channel = self.connection.channel()
            self.command_channel.queue_declare(queue=config.COMMAND_QUEUE, durable=True)
            self.status_channel.queue_declare(queue=config.STATUS_QUEUE, durable=True)
            self.epoch_channel.queue_declare(queue=config.EPOCH_QUEUE, durable=True)
            self.metrics_channel.queue_declare(queue=config.METRICS_QUEUE, durable=True)
        except pika.exceptions.AMQPConnectionError as e:
            print("Failed to connect to RabbitMQ:", str(e))
        except pika.exceptions.ChannelClosedByBroker as e:
            print("Channel closed by broker:", str(e))
        except Exception as e:
            print("An error occurred:", str(e))

    def subscribe_command_queue(self, callback):
        print('Listening for COMMAND messages')
        # self.command_channel.basic_qos(prefetch_count=1)
        self.command_channel.basic_consume(queue=config.COMMAND_QUEUE, on_message_callback=callback)
        self.command_channel.start_consuming()

    def send_epoch_message(self, msg: Epoch):
        print(f'Sending EPOCH message: {msg}')
        self.epoch_channel.basic_publish(
            exchange='',
            routing_key=config.EPOCH_QUEUE,
            body=json.dumps(asdict(msg)).encode('utf-8')
        )

    def send_status_message(self, msg: Status):
        print(f'Sending STATUS message: {msg}')
        self.epoch_channel.basic_publish(
            exchange='',
            routing_key=config.STATUS_QUEUE,
            body=json.dumps(asdict(msg)).encode('utf-8')
        )

    def send_metrics_message(self, msg: Metrics):
        print(f'Sending METRICS message: {msg}')
        self.epoch_channel.basic_publish(
            exchange='',
            routing_key=config.METRICS_QUEUE,
            body=json.dumps(asdict(msg)).encode('utf-8')
        )

    def close_connections(self):
        self.connection.close()
