export class Logger {
    constructor() {}
    async logError(error: string, code: number): Promise<CError> {
        let err: CError = { message: error, code: code };
        console.log(`***********\nLOGGER:\n***********\nError: \n${JSON.stringify(err, null, 2)}`);
        return err;
    }
}
export class CError {
    message?:string;
    code?: number;
    constructor(message, code) {
        this.message = message;
        this.code = code;
    }
}