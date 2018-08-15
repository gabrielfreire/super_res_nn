import rawpy
import torch
import torchvision
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def raw_to_pil(image_url):
    raw = rawpy.imread(image_url)
    rgb = raw.postprocess()
    return Image.fromarray(rgb) # Pillow image

def save_pil_image(img, output_url):
    img.save(output_url)
    print('output image saved to ', output_url)
  
# Predict for local images
def predict(model, image_url, plot=True):  
    inp = raw_to_pil(image_url) # Pillow image
    # img.show() # show on screen
    img_to_tensor = torchvision.transforms.ToTensor()
    # inp = Image.open('DSC_0506.NEF', mode='r')
    inp = inp.convert('YCbCr')
    y, cb, cr = inp.split()
    input = img_to_tensor(y).view(1, -1, y.size[1], y.size[0])
    if(plot):
        plt.figure(figsize=(20,20))
        plt.title('Input')
        plt.imshow(inp.convert('RGB'))
    out = model(input.cuda())
    out = out.cpu();
    out_img_y = out[0].detach().numpy()
    out_img_y *= 255.0
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')
    out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
    out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')
    if(plot):
        plt.figure(figsize=(20,20))
        plt.title('Output')
        plt.imshow(out_img)

    return out_img

def execute(image_url):
    # load model and predict
    model = torch.load('../../../assets/models/superres/model_epoch_50.pth')
    out_img = predict(model, image_url, plot=False)

