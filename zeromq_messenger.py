import zmq
import json
import os
import threading
from multiprocessing import Process
import sys
import path
# from src.networks.super_res.super_res import execute, save_pil_image, base64_to_pil_img

driver_processes = []

responder_url = 'tcp://*:5564'
publisher_url = 'tcp://*:5562'
# context = zmq.Context()
# responder
# socket = context.socket(zmq.REP)
# socket.bind(responder_url)
# publisher
# publisher = context.socket(zmq.PUB)
# publisher.bind(publisher_url)
output_url = 'assets/outputImages'

def worker():
    sender_context = zmq.Context()
    ventilator_send = sender_context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://*:5562")
    receiver_context = zmq.Context()
    work_receiver = receiver_context.socket(zmq.PULL)
    work_receiver.bind("tcp://*:5564")
    print("connected")
    try:
        while True:
            body = work_receiver.recv()
            print("received")
            requestParams = json.loads(body.decode('utf-8'))
            results = {}
            if (requestParams['type'] == 'superres'):
                results = get_prediction(str(requestParams['data']))
            
            ventilator_send.send_string(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        print(str(e))
    finally:
        ventilator_send.close()
        work_receiver.close()
        sender_context.term()
        receiver_context.term()
    
print("start")
def get_prediction (data):
    output_img = execute(data)
    if (not os.path.exists(output_url)): 
        os.mkdir(output_url)
    save_pil_image(output_img, output_url)
    return str(output_url)

def main():
    Process(target=worker, args=()).start()

if __name__ == "__main__":
    main()