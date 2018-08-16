import zmq
import json
from src.networks.super_res.super_res import execute, save_pil_image

responder_url = 'tcp://*:5563'
publisher_url = 'tcp://*:5562'
context = zmq.Context()
# responder
socket = context.socket(zmq.REP)
socket.bind(responder_url)
# publisher
publisher = context.socket(zmq.PUB)
publisher.bind(publisher_url)
output_url = 'assets/outputImages/output.png'
try:
    while True:
        body = socket.recv()
        requestParams = json.loads(body.decode('utf-8'))
        print("Its connected")
        if requestParams['type'] == 'superres':
            print("Got the message")
            results = {}
            # predict
            output = execute(str(requestParams['data']))
            print("Got output")
            # save output
            save_pil_image(output, output_url)
            print("Saved image")
            # send result
            results['data'] = str(output_url)
        
        socket.send_string(json.dumps(results, ensure_ascii=False))

except Exception as e:
    print(str(e))

finally:
    socket.close()
    context.term()