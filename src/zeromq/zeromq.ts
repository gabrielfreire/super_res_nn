declare var process;
import * as zmq from 'zeromq';
const pusher = zmq.socket('push'); // data-io
const puller = zmq.socket('pull'); // data-io
const subscriber = zmq.socket('sub'); // real-time

const Status = {
    ERROR: 'error',
    SUCCESS: 'success',
    UNINITIALIZED: 'notReady'
}
export class ZMQ {
    requesterUrl: string;
    pullerUrl: string;
    status: string;
    error: any;
    constructor(_url?: string) {
        const url = process.env.URL || 'tcp://localhost';
        this.requesterUrl = _url || `${url}:5564`;
        this.pullerUrl = _url || `${url}:5562`;
        this.status = Status.UNINITIALIZED;
    }

    /**
     * 
     * @param input { type: '', data: '' }
     */
    async exec(input) {
        const self = this;
        this.status = Status.UNINITIALIZED;
        return new Promise((resolve, reject) => {
            let result;
            let timeLimit = 1000 * 60;
            let startTime = new Date().getTime();
            try {
                puller.connect(this.pullerUrl);
                pusher.connect(this.requesterUrl);
                pusher.send(JSON.stringify(input));
                puller.on("message", function(reply) {
                    result = JSON.parse(reply.toString());
                    self.status = Status.SUCCESS;
                });
            } catch(e) {
                self.status = Status.ERROR;
                self.error = e;
            }
            
            // try until its ready
            function finnish() {
                let now = new Date().getTime();
                let elapsedTime = now - startTime;
                if(timeLimit && elapsedTime > timeLimit) { // timeout
                    reject({ error: `Connection timeout! maximum wait time is ${timeLimit / 1000}s, you probably forgot to start your Worker run 'python zeromq_messenger.py'` });
                } else if(self.status == Status.SUCCESS){ // success
                    resolve(result);
                } else if (self.status == Status.ERROR){ // error
                    reject({ error: `An error ocurred: ${self.error}` });
                } else {
                    setTimeout(finnish, 10);
                    return;
                }
                // setTimeout(()=> {
                //     requester.close();
                // }, 500);
            }
            finnish();
        });
    }
}