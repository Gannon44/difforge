#!/usr/bin/env python3
import sys
import numpy as np
from nbt import nbt


def load_schematic(filename):
    schematic = nbt.NBTFile(filename, 'rb')
    width = schematic["Width"].value
    height = schematic["Height"].value
    length = schematic["Length"].value
    blocks = schematic["Blocks"].value
    arr = np.array(blocks).reshape((height, length, width))
    arr = np.transpose(arr, (2, 0, 1))
    return arr, (width, height, length)


def convert_ids_to_names(block_array):
    vectorized_map = np.vectorize(lambda bid: BLOCK_ID_TO_NAME.get(bid, f"ID_{bid}"))
    return vectorized_map(block_array)


def main():
    filename = sys.argv[1]
    arr, dims = load_schematic(filename)
    print(arr)


if __name__ == "__main__":
    main()
