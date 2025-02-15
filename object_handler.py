from sprite_object import *
from npc import *

from sprite_object import *
from npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_positions = {}

        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'

        add_sprite = self.add_sprite
        add_npc = self.add_npc

        # sprite map
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))

        # npc map
        add_npc(NPC(game))
        add_npc(NPC(game, pos=(11.5, 4.5)))
        add_npc(NPC(game, pos=(8.5, 4.5)))
        add_npc(NPC(game, pos=(10.5, 6.5)))
        add_npc(NPC(game, pos=(5.5, 25.5)))
        add_npc(NPC(game, pos=(5.5, 23.5)))
        add_npc(NPC(game, pos=(5.5, 21.5)))
        add_npc(NPC(game, pos=(3.5, 19.5)))
        add_npc(NPC(game, pos=(1.5, 14.5)))
        add_npc(NPC(game, pos=(2.5, 9.5)))
        add_npc(NPC(game, pos=(3.5, 9.5)))
        add_npc(NPC(game, pos=(4.5, 9.5)))
        add_npc(NPC(game, pos=(5.5, 9.5)))
        add_npc(NPC(game, pos=(6.5, 9.5)))
        add_npc(NPC(game, pos=(7.5, 9.5)))
        add_npc(NPC(game, pos=(19.5, 4.5)))
        add_npc(NPC(game, pos=(18.5, 6.5)))
        add_npc(NPC(game, pos=(19.5, 6.5)))
        add_npc(NPC(game, pos=(21.5, 6.5)))
        add_npc(NPC(game, pos=(22.5, 6.5)))
        add_npc(NPC(game, pos=(16.5, 12.5)))
        add_npc(NPC(game, pos=(14.5, 16.5)))
        add_npc(NPC(game, pos=(8.5, 12.5)))
        add_npc(NPC(game, pos=(22.5, 13.5)))
        add_npc(NPC(game, pos=(32.5, 12.5)))
        add_npc(NPC(game, pos=(5.5, 22.5)))
        add_npc(NPC(game, pos=(27.5, 28.5)))

        add_npc(CacoDemonNPC(game, pos=(10.5, 5.5)))
        add_npc(CacoDemonNPC(game, pos=(14.5, 2.5)))
        add_npc(CacoDemonNPC(game, pos=(12.5, 12.5)))
        add_npc(CacoDemonNPC(game, pos=(12.5, 14.5)))

        add_npc(CacoDemonNPC(game, pos=(24.5, 12.5)))

        add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        if isinstance(npc, CacoDemonNPC):
            npc.health = self.game.enemy_health['CacoDemonNPC']
            npc.attack_damage = self.game.enemy_damage['CacoDemonNPC']
        elif isinstance(npc, CyberDemonNPC):
            npc.health = self.game.enemy_health['CyberDemonNPC']
            npc.attack_damage = self.game.enemy_damage['CyberDemonNPC']
        else:
            npc.health = self.game.enemy_health['NPC']
            npc.attack_damage = self.game.enemy_damage['NPC']
        print(f"Added NPC: {npc.__class__.__name__} with health {npc.health} and damage {npc.attack_damage}")
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def is_valid_position(self, x, y):
        tile_x, tile_y = int(x), int(y)
        try:
            return self.game.map.mini_map[tile_y][tile_x] == '_'
        except IndexError:
            return False

    def all_enemies_dead(self):
        all_dead = all(not npc.alive for npc in self.npc_list)
        print(f"All enemies dead check: {all_dead} (Total NPCs: {len(self.npc_list)})")
        for npc in self.npc_list:
            print(f"{npc.__class__.__name__} at ({npc.x}, {npc.y}) alive: {npc.alive}")
        return all_dead