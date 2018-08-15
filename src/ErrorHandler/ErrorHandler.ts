import { Logger, CError } from './../logger/logger';
const logger = new Logger();
export class ErrorHandler {
    constructor(){}
    async handleError (error: string|any): Promise<CError> {
        let code: number = error.code ? error.code: null;
        let message: string = error.message ? error.message : error;
        let err: CError = await logger.logError(message, code);
        return err;
    }
}