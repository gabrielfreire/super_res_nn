import * as express from 'express';
import * as cors from 'cors';
import * as bodyParser from 'body-parser';
import { ErrorHandler } from './src/ErrorHandler/ErrorHandler';
import { CError } from './src/logger/logger';
import { superResRouter } from './src/networks/super_res/SuperResRouter';
const errorHandler: ErrorHandler = new ErrorHandler();
const app = express();
//options for cors midddleware
const options: cors.CorsOptions = {
    credentials: true,
    origin: "*",
    preflightContinue: false
};
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser({ limit: '50mb' }));
app.use(bodyParser.json());

app.use(cors(options));
app.use('/api', superResRouter);
app.use(async (err, req, res, next) => {
    console.log("got error", err);
    if(!err) next();
    const error: CError = await errorHandler.handleError(err);
    const status: any = error.code;
    if(status && typeof status == 'number') { res.status(status).jsonp(error); }
    else { res.jsonp(error); }
    next();
});

const server = app.listen(process.env.PORT || 8000, function() {
    console.log(`App listening at http://${process.env.URL || server.address().address}:${process.env.PORT || server.address().port}`);
});