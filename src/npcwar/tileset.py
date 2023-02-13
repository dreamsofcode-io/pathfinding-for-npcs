class Tileset:
    def __init__(self, name, image, tile_height, tile_width, index):
        self.name = name
        self.index = index
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.image = image

    def get_tile(self, name):
        width = self.image.width
        height = self.image.height
        x = self.index[name] * self.tile_width % width
        y = self.index[name] * self.tile_width // width * self.tile_height
        return self.image.get_region(
            x,
            y,
            self.tile_width,
            self.tile_height
        )
