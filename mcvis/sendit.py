import requests
import random

def places(np3d, offset_x=0, offset_y=0, clear_space=True, palette=["minecraft:air", "minecraft:cobblestone", "minecraft:oak_planks", "minecraft:oak_log"]):
    '''
    places the given np3d array at the given offset in the world
    - clear_space: if True, will place air blocks
    - palette: block ids for values 0, 1, 2, 3 in the np3d array; if a tuple, will randomly choose one of the block ids
    '''
    x, y, z, one = np3d.shape

    url = "http://localhost:9000/blocks?x=0&y=0&z=0"
    blocks = []
    for dx in range(x):
        for dy in range(y):
            for dz in range(z):
                block_id = palette[int(np3d[dx, dy, dz, 0])]
                if not clear_space and block_id == "minecraft:air":
                    continue
                if isinstance(block_id, tuple):
                    block_id = random.choice(block_id)
                block = {
                        "id": block_id,  # block id
                        "x": dx + offset_x,  
                        "y": dz - 61,   # y is up in minecraft 
                        "z": dy + offset_y,
                    }
                blocks.append(block)
                    
                
    print(blocks)
    response = requests.put(url, json=blocks)
    if response.status_code == 200:
        print("Successfully placed wood blocks!")
    else:
        print("Error placing blocks:", response.text)
