import * as zmq from 'zeromq';
const requester = zmq.socket('req'); // data-io
const subscriber = zmq.socket('sub'); // real-time

const Status = {
    ERROR: 'error',
    SUCCESS: 'success',
    UNINITIALIZED: 'notReady'
}
export class ZMQ {
    requesterUrl: string;
    status: string;
    constructor(url) {
        const local = 'tcp://localhost';
        this.requesterUrl = url || `${process.env.URL || local}:5563`;
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
            let timeLimit = 1000 * 5;
            let startTime = new Date().getTime();
        
            requester.send(JSON.stringify(input));
            requester.on("message", function(reply) {
                result = JSON.parse(reply.toString());
                self.status = Status.SUCCESS;
            });
            requester.connect(this.requesterUrl);
            
            // try until its ready
            function finnish() {
                let now = new Date().getTime();
                let elapsedTime = now - startTime;
                if(timeLimit && elapsedTime > timeLimit) { // timeout
                    reject({ error: `Connection timeout! maximum wait time is ${timeLimit / 1000}s, you probably forgot to start your Worker run 'python zeromq_messenger.py'` });
                } else if(self.status == Status.SUCCESS){ // success
                    resolve(result);
                } else if (self.status == Status.ERROR){ // error
                    reject({ error: 'An error ocurred!' });
                } else {
                    setTimeout(finnish, 10);
                    return;
                }
                setTimeout(()=> {
                    requester.close();
                }, 500);
            }
            finnish();
        });
    }
}