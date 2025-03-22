import lib.grabcraft_to_schema as gts
import lib.blockmodel_avg_mapper as bam
import json
import PIL
from PIL import Image
import numpy as np
from pathlib import Path
import argparse
import hashlib
from tqdm import tqdm

'''
Script to automatically download image schematics from grabcraft given a list of urls
--urls: file with urls of the Grabcraft models, see data/houses.txt
--dir: directory to store the data, default is 'dataset'

Edit 2/25/25: Thanks Xiuyuan!
'''

# Load the block map
gts.load_block_map("data/blockmap.csv")

def batch_save(urls):
    for url in urls:
        get_and_save_slices(url)

def hash_str(s):
    return str(hashlib.md5(s.encode()).hexdigest())

def get_and_save_slices(url, save_dir, pfunc=print):
    schem = gts.url_to_render_object_data(url)
    url_hash = hash_str(url)[1:5] # to avoid name collisions
    pfunc(f"Done downloading")

    img, name, dims = gts.render_object_to_png_slice(schem, with_metadata=True)
    name = name.replace(" ", "_")
    width, height, length = dims
    save_dir = save_dir + "/" + name + "_" + url_hash
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    # check if directory is empty 
    if any(Path(save_dir).iterdir()):
        pfunc(f"Directory {save_dir} is already populated, skipping...")
        return

    for i in range(length):
        # crop pil image (left, up, right, down)
        left_border, right_border = i * width, (i + 1) * width
        img.crop((left_border, 0, right_border, height)).save(f"{save_dir}/{name}_{i}.png")
    pfunc(f"Done writing {length} ims for {name}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Downloader for Grabcraft',
                    description='Creates PNG slices from Grabcraft models',
                    epilog='Text at the bottom of help')
    parser.add_argument('-u', '--urls', help='file with urls of the Grabcraft models', required=True)
    parser.add_argument('-d', '--dir', help='directory to store the data', default='dataset')
    args = parser.parse_args()

    if not Path(args.dir).exists():
        Path(args.dir).mkdir(parents=True, exist_ok=True)

    with open(args.urls, 'r') as f:
        urls = f.readlines()
        pbar = tqdm(urls)
        for url in pbar:
            try:
                get_and_save_slices(url.strip(), args.dir, pbar.set_description)
            except Exception as e:
                print(f"Error with {url}: {e}")
