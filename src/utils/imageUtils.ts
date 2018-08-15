import { FileMetadata64, writeFileToTemp, getFileFromBase64 } from './base64';

/**
* save image to Cloudinary from base64
* @param {string} url 
* @param {base64} base64 string 
*/
export async function saveImage (url: string, data: string): Promise<void> {
    try {
        const imageBuffer: FileMetadata64 = getFileFromBase64(data);
        await writeFileToTemp(url, imageBuffer.data);
    } catch(e) { throw e; }
}
export async function removeImage (id: string): Promise<any> {
}