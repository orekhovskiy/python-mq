from schemas.command import Command
from schemas.epoch import Epoch
from schemas.metrics import Metrics
from schemas.status import Status
from mq_service import MQService
import json

if __name__ == "__main__":
    mq_service = MQService(host='localhost', port=5672, username='username', password='password')
    status = Status(type='info', message='Started')
    metrics = Metrics(fps=0.1, p=10.1, r=0.7, mAP_50=0.5, mAP_95=.95)
    epoch = Epoch(current=1, total=1)

    def execute_command(_ch, _method, _properties, body: bytes):
        command: dict = json.loads(body.decode('utf-8'))
        if command['type'] == 'start':
            print('Executing START command')
            mq_service.send_status_message(status)
            mq_service.send_metrics_message(metrics)
            mq_service.send_epoch_message(epoch)
        elif command['type'] == 'stop':
            print('Executing STOP command')
            abort_status = Status(message='abort', type='info')
            mq_service.send_status_message(abort_status)
            mq_service.close_connections()

    mq_service.subscribe_command_queue(execute_command)

    while():
        pass
