import zmq
import json
import os
from src.networks.super_res.super_res import execute, save_pil_image, base64_to_pil_img

responder_url = 'tcp://*:5563'
publisher_url = 'tcp://*:5562'
context = zmq.Context()
# responder
socket = context.socket(zmq.REP)
socket.bind(responder_url)
# publisher
publisher = context.socket(zmq.PUB)
publisher.bind(publisher_url)
output_url = 'assets/outputImages'
try:
    while True:
        body = socket.recv()
        requestParams = json.loads(body.decode('utf-8'))
        print("Its connected")
        if (requestParams['type'] == 'superres'):
            print("Its super resolution request")
            results = {}
            print("Got the message")
            # predict
            output_img = execute(str(requestParams['data']))
            print("Got output")
            # save output
            if (not os.path.exists(output_url)): 
                os.mkdir(output_url)
            save_pil_image(output_img, output_url)
            print("Saved image")
            # send result
            results['data'] = str(output_url)
        
        socket.send_string(json.dumps(results, ensure_ascii=False))

except Exception as e:
    print(str(e))

finally:
    socket.close()
    context.term()