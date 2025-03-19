# view samples from diffusion in minecraft

## Running
1. Make sure the packages in requirements.txt are installed.
2. [Install](https://github.com/Niels-NTG/gdmc_http_interface?tab=readme-ov-file#automated-installation-recommended) the GDMC HTTPS interface for Minecraft.
3. Run Minecraft (I used 1.21.4) and load a superflat world.
4. run `python minecraft.py`


## Details
- minecraft.py
    - top level, places all 64 samples in the world using a given block pallette
- sendit.py
    - responsible for communicating with the HTTP client 
- erosion.py
    - contains `two_tone()` and `three_tone()`, which takes a [0,1] np 
    matrix and uses binary erosion to add highlights ([0,1,2] for two tone and [0,1,3,4] for three tone).
- samples.npy
    - contains 64 generated house samples from the diffusion model

