import * as express from 'express';
export const superResRouter = express.Router();
import * as path from 'path';
import { SuperResolutionService } from './SuperResService';
import { CError } from '../../logger/logger';
import { saveImage } from '../../utils/imageUtils';
const inputUrl = path.join(__dirname, '../../../../assets/inputImages/inputImage.png');
const ssService = new SuperResolutionService();
superResRouter.route("/superres/predict")
    .post(async (req, res, next) => {
        try {
            if(!req.body) throw new CError('No body found', 404);
            if(!req.body.base64) throw new CError('No image url was found', 404);
            const imageData = req.body.base64;
            await saveImage(inputUrl, imageData);
            const pred: any = await ssService.getPrediction(inputUrl);
            res.status(200).jsonp(pred);
        } catch (error) {
            next (error);
        }
    })