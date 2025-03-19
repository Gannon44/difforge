import torch
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def selective_keep(data, include_kernels=[], exclude_kernels=[]):
    '''
    include blocks that are highlighted by the include kernels
    but not highlighted by the exclude kernels. 
    '''
    def erode_with_kernel(data, kernel):
        # Ensure kernel is 5D (batch, channels, D, H, W)
        if kernel.dim() == 3:
            kernel = kernel.unsqueeze(0).unsqueeze(0)
        elif kernel.dim() == 4:
            kernel = kernel.unsqueeze(0)

        # Perform 3D erosion: check where the entire kernel fits
        return (F.conv3d(data, kernel, padding=1) == kernel.sum()).float()

    # Apply inclusion kernels (logical OR across multiple kernels)
    include_mask = torch.zeros_like(data)
    for kernel in include_kernels:
        include_mask += erode_with_kernel(data, kernel)

    # Apply exclusion kernels (logical OR across multiple kernels)
    exclude_mask = torch.zeros_like(data)
    for kernel in exclude_kernels:
        exclude_mask += erode_with_kernel(data, kernel)

    # Keep regions that match inclusion but NOT exclusion
    result = (include_mask > 0) & (exclude_mask == 0)

    return result.float()

def merge_arrays(arrays):
    '''merge list of arrays such that the initial array's non-zero values are overwritten by later array non zero values'''
    # Ensure input is a list of tensors and clone the first array to preserve it
    merged = arrays[0].clone()

    # Iterate over the remaining arrays
    for arr in arrays[1:]:
        # Overwrite non-zero values from the current array
        merged[arr != 0] = arr[arr != 0]

    return merged


## KERNELS ##

def pillars(data):
    '''
    data: torch.tensor of shape (batch, channels, D, H, W)
    '''
    # a kernel for pillars
    kernel1 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], 
        [0,1,1], 
        [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, 3, 3, 3)
    # exclude from set if the exkernel matches
    exkernel1 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], 
        [1,1,0], 
        [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)
    exkernel2 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,1,0], 
        [0,1,1], 
        [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)
    exkernel3 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], 
        [0,1,1], 
        [0,1,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)
    pillar_k = [kernel1]
    pillar_kx = [exkernel1, exkernel2, exkernel3]
    # Ensure kernels are on the same device as data
    pillar_k = [k.to(device) for k in pillar_k]
    pillar_kx = [k.to(device) for k in pillar_kx]

    pillars = []
    for i in range(4):
        '''
        permute(0,1,3,4,2) because we were treating the kernels as z,x,y 
        (where z is the row), but our data is actually (x,y,z).

        rotate because each pillar can be in 4 directions
        '''
        new_pillar_k = [torch.rot90(k, i, [3, 4]).permute(0,1,3,4,2) for k in pillar_k]
        new_pillar_kx = [torch.rot90(k, i, [3, 4]).permute(0,1,3,4,2) for k in pillar_kx]
        # print(torch.rot90(pillar_kx[0], i, [3, 4]))
        # print(torch.rot90(pillar_k[0], i, [3, 4]))
        pillars.append(selective_keep(data, new_pillar_k, new_pillar_kx))


    # Merge the results (logical OR operation to combine the '1's)
    pillars = merge_arrays(pillars)
    return pillars

def pillars2(data):
    # alternative pillar detector
    kernel1 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,1,0], 
        [0,1,1], 
        [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, 3, 3, 3)
    exkernel1 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], 
        [1,1,0], 
        [0,0,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)
    exkernel2 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], 
        [0,1,0], 
        [0,1,0]],
        [[0,0,0], [0,0,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)

    pillar_k = [kernel1]
    pillar_kx = [exkernel1, exkernel2]
    # Ensure kernels are on the same device as data
    pillar_k = [k.to(device) for k in pillar_k]
    pillar_kx = [k.to(device) for k in pillar_kx]

    pillars2 = []
    for i in range(4):
        '''
        permute(0,1,3,4,2) because we were treating the kernels as z,x,y 
        (where z is the row), but our data is actually (x,y,z).

        rotate because each pillar can be in 4 directions
        '''
        new_pillar_k = [torch.rot90(k, i, [3, 4]).permute(0,1,3,4,2) for k in pillar_k]
        new_pillar_kx = [torch.rot90(k, i, [3, 4]).permute(0,1,3,4,2) for k in pillar_kx]
        # print(torch.rot90(pillar_kx[0], i, [3, 4]))
        # print(torch.rot90(pillar_k[0], i, [3, 4]))
        pillars2.append(selective_keep(data, new_pillar_k, new_pillar_kx))

    # Merge the results (logical OR operation to combine the '1's)
    pillars2 = merge_arrays(pillars2)
    return pillars2

def walls(data):
    kernel1 = torch.tensor([
        [[0,0,0], [0,0,0], [0,0,0]],
        [[0,0,0], [0,1,0], [0,0,0]],
        [[0,0,0], [0,1,0], [0,0,0]]
    ]).float().unsqueeze(0).unsqueeze(0)

    wall_k = [kernel1.permute(0,1,3,4,2).to(device)]
    walls = selective_keep(data, wall_k)
    return walls

def two_tone(data):
    wall_blocks = walls(data)
    merged = merge_arrays([data, wall_blocks * 2])
    return merged

def three_tone(data):
    pillar1 = pillars(data)
    pillar2 = pillars2(data)
    pillar_merged = merge_arrays([pillar1, pillar2])
    wall_blocks = walls(data)
    merged = merge_arrays([data, wall_blocks * 2, pillar_merged * 3])
    return merged