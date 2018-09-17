import zmq
import json
import os
import threading
from multiprocessing import Process
import sys
import path
from src.networks.super_res.super_res import execute, save_pil_image, base64_to_pil_img

driver_processes = []

pusher_url = 'tcp://*:5562'
puller_url = 'tcp://*:5564'
output_url = 'assets/outputImages'

class Worker:
    def __init__(self):
        print("start")
        self.sender_context = zmq.Context()
        self.ventilator_send = self.sender_context.socket(zmq.PUSH)
        self.ventilator_send.bind(pusher_url)
        self.receiver_context = zmq.Context()
        self.work_receiver = self.receiver_context.socket(zmq.PULL)
        self.work_receiver.bind(puller_url)
        print("connected")
        while True:
            body = self.work_receiver.recv()
            requestParams = json.loads(body.decode('utf-8'))
            results = {}
            if (requestParams['type'] == 'superres'):
                results = get_prediction(str(requestParams['data']))
            
            self.ventilator_send.send_string(json.dumps(results, ensure_ascii=False))
    
    def close_connections(self):
        self.ventilator_send.close()
        self.work_receiver.close()
        self.sender_context.term()
        self.receiver_context.term()
    
def get_prediction (data):
    output_img = execute(data)
    if (not os.path.exists(output_url)): 
        os.mkdir(output_url)
    save_pil_image(output_img, output_url)
    return str(output_url)

def main(worker):
    Process(target=worker, args=()).start()

if __name__ == "__main__":
    worker = Worker()
    try:
        main(worker)
    except Exception as e:
        print(str(e))
    finally:
        worker.close_connections()