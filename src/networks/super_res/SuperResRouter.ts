import * as express from 'express';
export const superResRouter = express.Router();
import * as path from 'path';
import * as multer from 'multer';
import { SuperResolutionService } from './SuperResService';
import { CError } from '../../logger/logger';
import { saveImage } from '../../utils/imageUtils';
const inputUrl = path.join(__dirname, '../../../../assets/inputImages/');
const outputUrl = path.join(__dirname, '../../../assets/outputImages/output.png');
const storage = multer.memoryStorage()
const upload = multer({ storage: storage })
// const upload = multer({ dest: inputUrl });
const ssService = new SuperResolutionService();

superResRouter.route("/superres/b64/predict")
    .post(async (req, res, next) => {
        try {
            if(!req.body) throw new CError('No body found', 500);
            if(!req.body.base64) throw new CError('No image url was found', 500);
            const imageData = req.body.base64;
            await saveImage(inputUrl, imageData);
            const pred: any = await ssService.getPrediction(inputUrl);
            res.status(200).jsonp(pred);
        } catch (error) {
            next (error);
        }
    });

superResRouter.route("/superres/file/predict")
    .post(upload.single( 'inputImage' ), async (req, res, next) => {
        try {
            if(!req.file) throw new CError('No file sent', 500);
            const base64String: string = Buffer.from(req.file.buffer).toString('base64');
            await ssService.getPrediction(base64String);
            res.status(200).sendFile(outputUrl);
        } catch (error) {
            next (error);
        }
    })

    // commented utilities 
    
    // const url: string = req.file.path;
    // const today = new Date();
    // const imagePath: string = `${inputUrl}inputImage-${today.getTime()}.png`;
    // const src: fs.ReadStream = fs.createReadStream(url);
    // const dest: fs.WriteStream = fs.createWriteStream(imagePath);
    // let sum: number = 0;
    // src.pipe(dest);
    // src.on('error', (err) => {
    //     if(err) console.log(err);
    // });
    // src.on('readable', () => { 
    //     let chunk;
    //     while((chunk = src.read()) !== null) {
    //         sum += chunk.length;
    //         console.log(`Received: ${chunk.length} bytes of data`);
    //         console.log(`Total: [${((sum/req.file.size) * 100).toFixed(2)}%] ${sum} bytes of data`);
    //     }
    // });
    // src.on('end', async () => {
    //     try {
    //         console.log(`finished writing file on ${imagePath}`);
    //         //remove temp file
    //         fs.unlinkSync(url);
    //         console.log(`removed file ${url}`);
    //         await ssService.getPrediction(imagePath);
    //         fs.unlinkSync(imagePath);
    //         console.log(`removed input image ${imagePath}`);
    //         if(!fs.existsSync(outputUrl)) { throw new CError('output.png does not exist', 404); }
    //         res.status(200).sendFile(outputUrl);
    //     } catch (e) {
    //         if(fs.existsSync(imagePath)) { 
    //             fs.unlinkSync(imagePath); 
    //             console.log(`Removed input image ${imagePath}`);
    //             next (e);
    //         } else { next (e); }
    //     }
    // });