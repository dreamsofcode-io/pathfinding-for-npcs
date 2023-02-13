from npcwar import util
from npcwar import tileset
import os

class AssetManager:
    def __init__(self):
        self.path = './assets'
        self.assets = {}
        self.animations = {}
        self.tilesets = {}
        self.load_assets()
        self.load_tiles()

    def load_assets(self):
        animations = [
            'npc/green/rifle/idle',
        ]

        for animation in animations:
            self.animations[animation] = util.load_npc_animation(*animation.split('/'))

    def load_tileset(self, name):
        return util.load_tileset(os.path.join(self.path, 'tilesets', name))

    def load_tiles(self):
        img = self.load_tileset('scifitiles-sheet.png')
        scifitiles = tileset.Tileset('scifitiles', img, 32, 32, {
            'floor': 20,
            'wall': 42,
        })
        self.tilesets['scifitiles'] = scifitiles

    def get_animation(self, key):
        return self.animations[key]

    def __getitem__(self, key):
        if key not in self.assets:
            self.assets[key] = pygame.image.load(os.path.join(self.path, key))
        return self.assets[key]
