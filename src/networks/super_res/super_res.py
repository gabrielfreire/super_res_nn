import rawpy
import torch
import torchvision
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
import io
from model import SRNet


def raw_to_pil(image_url):
    raw = rawpy.imread(image_url)
    rgb = raw.postprocess()
    return Image.fromarray(rgb) # Pillow image

def save_pil_image(img, output_url):
    img.save("{}/output.png".format(output_url))
    print('output image saved to ', output_url)
  
# Predict for local images
def predict(model, image, plot=True):  
    # inp = raw_to_pil(image_url) # Pillow image
    inp = image
    # inp = Image.open(image_url, mode='r')
    # img.show() # show on screen
    img_to_tensor = torchvision.transforms.ToTensor()
    # inp = Image.open('DSC_0506.NEF', mode='r')
    inp = inp.convert('YCbCr')
    y, cb, cr = inp.split()
    input = img_to_tensor(y).view(1, -1, y.size[1], y.size[0]) # view is like reshape
    print('Predicting...')
    with torch.no_grad():
        out = model(input.cuda())
        out = out.cpu();
        print('Done...')
        out_img_y = out[0].detach().numpy()
        out_img_y *= 255.0
        out_img_y = out_img_y.clip(0, 255)
        out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')
        out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
        out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
        out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')
        if (plot):
            plt.figure(figsize=(20,20))
            plt.title('Input')
            plt.imshow(inp.convert('RGB'))

            plt.figure(figsize=(20,20))
            plt.title('Output')
            plt.imshow(out_img)
            plt.show()

    return out_img

def execute(base64):
    # load model and predict
    upscale_factor = 3
    model = SRNet(upscale_factor=upscale_factor)
    model.load_state_dict(torch.load(os.getcwd() + '/assets/models/superres/model_epoch_150.pth'))
    model.cuda()
    model.eval()
    image = base64_to_pil_img(base64)
    out_img = predict(model, image, plot=False)
    return out_img

def base64_to_pil_img(buff, plot=False):
    print('Getting b64')
    imgdata = base64.b64decode(buff)
    image = Image.open(io.BytesIO(imgdata))
    print('Got b64 to img')
    if (plot):
        plt.figure(figsize=(20, 20))
        plt.title('Buffer')
        plt.imshow(image)
        plt.show()
    return image

