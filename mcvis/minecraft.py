import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from erosion import two_tone, three_tone
from sendit import places
import random

sample_houses = np.load('samples.npy')
print(sample_houses.shape)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

def visualize_house(vox, ids=False):
    '''
    expect x, y, z, c
    '''
    rgba = np.repeat(vox, 4, axis=-1)
    thresh = 0.01
    solid = rgba[:, :, :, -1] > thresh
    rgba[:, :, :, 1:2] *= 0.8
    rgba[:, :, :, -1] = 0.9 * (rgba[:, :, :, -1] > thresh)

    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(solid,
              facecolors=rgba)
    plt.show()
    plt.close()


houses_np = sample_houses > 0.8
print(np.unique(houses_np, return_counts=True))
ds = torch.from_numpy(np.float32(houses_np)).to(device)
print(ds.shape)

normal = ["minecraft:air", "minecraft:cobblestone", "minecraft:oak_planks", "minecraft:oak_log"]
ruins = ["minecraft:air", 
        ("minecraft:cobblestone", "minecraft:mossy_cobblestone"), 
        "minecraft:spruce_log", 
        ("minecraft:cracked_stone_bricks", "minecraft:stone_bricks", "minecraft:chiseled_stone_bricks", "minecraft:mossy_stone_bricks")]
desert_oasis = [
    "minecraft:air", 
    ("minecraft:sandstone", "minecraft:cut_sandstone"),
    ("minecraft:cut_red_sandstone", "minecraft:red_sandstone"),
    "minecraft:chiseled_sandstone"
]
modern = [
            "minecraft:air", 
            "minecraft:quartz_block",
            "minecraft:glass",
            "minecraft:stone_bricks"
        ]
    
palette = modern

for i in range(8):
    for j in range(8):
        # random_house = random.choice(ds)
        random_house = ds[i*8 + j]
        res = three_tone(random_house).permute(1,2,3,0)
        places(res.cpu().numpy(), i*32, j*32, True, palette)

# three_tone_res = three_tone(random_house).permute(1,2,3,0)
# places(three_tone_res.cpu().numpy(), 0, 32, False, palette)

# for i in range(ds.shape[0]):
#     data = ds[i]
#     two_tone_res = two_tone(data).permute(1,2,3,0)
#     places(two_tone_res.cpu().numpy(), i*32, 0)

#     three_tone_res = three_tone(data).permute(1,2,3,0)
#     places(three_tone_res.cpu().numpy(), i*32, 32)
    

