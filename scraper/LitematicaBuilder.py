from amulet.level import load_level
from amulet.api.block import Block
import litemapy
import os


class LitematicaBuilder:
    def __init__(self, minecraft_world_path, litematic_file_path, cache_dir="/tmp/amulet_cache"):
        """
        Initializes the builder with paths to the Minecraft world and Litematica file.

        Args:
            minecraft_world_path (str): Path to the Minecraft world save.
            litematic_file_path (str): Path to the Litematica file.
            cache_dir (str): Path to the cache directory for Amulet (optional).
        """
        # Set the cache directory for Amulet
        os.environ["AMULET_LEVEL_CACHE_DIR"] = cache_dir

        self.minecraft_world_path = minecraft_world_path
        self.litematic_file_path = litematic_file_path
        self.world = None
        self.schematic = None
        self.region = None
        self.game_version = None

    def load_world(self):
        """Loads the Minecraft world using Amulet."""
        print("Loading Minecraft world...")
        self.world = load_level(self.minecraft_world_path)
        self.game_version = ("java", (1, 20, 5)) # (self.world.level_wrapper.platform, self.world.level_wrapper.version)
        print("Game version:", self.game_version)

    def load_schematic(self):
        """Loads the Litematica schematic."""
        print(f"Loading schematic: {self.litematic_file_path}")
        self.schematic = litemapy.Schematic.load(self.litematic_file_path)

        # Get the first region from the schematic
        self.region = list(self.schematic.regions.values())[0]

    def place_block(self, b_x, b_y, b_z, block_id, block):
        """
        Places a block in the world if it is not air.

        Args:
            b_x (int): X-coordinate of the block.
            b_y (int): Y-coordinate of the block.
            b_z (int): Z-coordinate of the block.
            block_id (str): ID of the block.
            block (Block): Block object to place.
        """
        if block and block_id != "minecraft:air":
            self.world.set_version_block(b_x, b_y, b_z, "minecraft:overworld", self.game_version, block)

    def place_blocks(self, start_x, start_y, start_z):
        """
        Places the blocks from the schematic into the Minecraft world.

        Args:
            start_x (int): X-coordinate to start placing the schematic.
            start_y (int): Y-coordinate to start placing the schematic.
            start_z (int): Z-coordinate to start placing the schematic.
        """
        print("Placing blocks into world...")
        for x in self.region.range_x():
            for y in self.region.range_y():
                for z in self.region.range_z():
                    block = self.region[x, y, z]
                    block_state_id = block.id
                    platform, blockname = block_state_id.split(":")
                    new_block = Block(platform, blockname)
                    self.place_block(start_x + x, start_y + y, start_z + z, block_state_id, new_block)



    def save_world(self):
        """Saves and closes the Minecraft world."""
        if self.world:
            print("Saving world...")
            self.world.save()
            self.world.close()
            print("Done! Open Minecraft and load the world to see your schematic.")


# Example usage (this would go in your main script):
if __name__ == "__main__":
    # Define paths to your Minecraft world and Litematica file
    MINECRAFT_WORLD_PATH = "/Users/dhern162/Library/Application Support/minecraft/saves/New World"
    LITEMATIC_FILE_PATH = "RibhlMzNAc-Pagoda.litematic"
    START_X, START_Y, START_Z = 40, -60, 40

    # Initialize and use the builder
    builder = LitematicaBuilder(MINECRAFT_WORLD_PATH, LITEMATIC_FILE_PATH)
    builder.load_world()
    builder.load_schematic()
    builder.place_blocks(START_X, START_Y, START_Z)
    builder.save_world()