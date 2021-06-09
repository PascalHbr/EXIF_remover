from PIL import Image, ImageOps
import numpy as np
import argparse
import os
from tqdm import tqdm

def remove_exif(img):
    exif = img.getexif()
    # Remove all exif tags
    for k in exif.keys():
        if k != 0x0112:
            exif[k] = None # If I don't set it to None first (or print it) the del fails for some reason. 
            del exif[k]
    # Put the new exif object in the original image
    new_exif = exif.tobytes()
    img.info["exif"] = new_exif
    # Rotate the image
    img = ImageOps.exif_transpose(img)
    return img

def remove_all(arg):
    dir = arg.dir
    valid_images = [".jpg",".gif",".png",".tga"]
    imgs = []
    paths = []
    for f in os.listdir(dir):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        paths.append(os.path.join(dir,f))
    for path in tqdm(paths):
        img = Image.open(path)
        img = remove_exif(img)
        img.save(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True, help="Image Directory")
    arg = parser.parse_args()
    print("****Start removing exif****")
    remove_all(arg)
    print('****Done****')
