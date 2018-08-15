import * as fs from 'fs';

const INVALID_STRING: string = 'Invalid input base64 string';
const BASE64: string = 'base64';

// --------- Functions ---------

/**
 * get file from base64
 * @param {string} base64
 * @return Buffer
 */
export function getFileFromBase64(base64: string): FileMetadata64 {
    const matches = base64.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
    const response: FileMetadata64 = {};
    if (!matches || matches.length !== 3) { throw new Error(INVALID_STRING); }
    response['type'] = matches[1];
    response['data'] = new Buffer(matches[2], BASE64);
    return response;
}
/**
 * save image to disk [tmp/ folder]
 * @param {string} _path 
 * @param {Buffer} data 
 */
export async function writeFileToTemp(_path: string, data: any): Promise<void> {
    try {
        fs.writeFileSync(_path, data, BASE64);
    } catch (e) {
        throw e;
    }
}


// --------- Types ---------

export interface FileMetadata64 {
    type?: string;
    data?: Buffer;
}
