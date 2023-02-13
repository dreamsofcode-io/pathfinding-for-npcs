from npcwar import util

class AssetManager:
    def __init__(self):
        self.path = './assets'
        self.assets = {}
        self.animations = {}
        self.load_assets()

    def load_assets(self):
        animations = [
            'npc/green/rifle/idle',
        ]

        for animation in animations:
            self.animations[animation] = util.load_npc_animation(*animation.split('/'))

    def get_animation(self, key):
        return self.animations[key]

    def __getitem__(self, key):
        if key not in self.assets:
            self.assets[key] = pygame.image.load(os.path.join(self.path, key))
        return self.assets[key]
