import { ZMQ } from '../../zeromq/zeromq';
import { CError } from '../../logger/logger';
const zmq = new ZMQ(null);
export class SuperResolutionService {
    constructor () { }

    async getPrediction(imageUrl) {
        let request = { type: 'superres', data: imageUrl };
        try {
            let result = await zmq.exec(request);
            return result;
        } catch(e) {
            throw new CError(e, 0);
        }
    }
}