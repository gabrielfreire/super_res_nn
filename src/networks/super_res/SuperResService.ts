import { ZMQ } from '../../zeromq/zeromq';
import { CError } from '../../logger/logger';
const zmq = new ZMQ(null);
export class SuperResolutionService {
    constructor () { }

    async getPrediction(base64String: string) {
        let request = { type: 'superres', data: base64String };
        try {
            let result = await zmq.exec(request);
            return result;
        } catch(e) {
            throw new CError(e, 0);
        }
    }
}